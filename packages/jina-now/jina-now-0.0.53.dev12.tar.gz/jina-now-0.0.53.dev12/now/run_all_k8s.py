import json
import os.path

import cowsay
import requests
from docarray import DocumentArray
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Column, Table

from now import run_backend
from now.compare.compare_flows import compare_flows_for_queries
from now.constants import DEMO_NS, FLOW_STATUS
from now.deployment import deployment
from now.dialog import configure_user_input, maybe_prompt_user


def stop_now(**kwargs):
    _result, flow_id, cluster = get_flow_status(action='delete', **kwargs)
    if _result is not None and _result['status']['phase'] == FLOW_STATUS:
        deployment.terminate_wolf(flow_id)
        from hubble import Client

        cookies = {'st': Client().token}
        requests.delete(
            f'https://storefrontapi.nowrun.jina.ai/api/v1/schedule_sync/{flow_id}',
            cookies=cookies,
        )
    cowsay.cow(f'remote Flow `{cluster}` removed')


def start_now(**kwargs):
    user_input = configure_user_input(**kwargs)
    app_instance = user_input.app_instance
    # Only if the deployment is remote and the demo examples is available for the selected app
    # Should not be triggered for CI tests
    if app_instance.is_demo_available(user_input):
        gateway_host_http = f'https://{DEMO_NS.format(user_input.dataset_name.split("/")[-1])}.dev.jina.ai'
    else:
        gateway_host_http = run_backend.run(app_instance, user_input, **kwargs)
    bff_url = f'{gateway_host_http}/api/v1/search-app/docs'
    playground_url = f'{gateway_host_http}/playground'

    _generate_info_table(gateway_host_http, bff_url, playground_url, user_input)
    return {
        'bff': bff_url,
        'playground': playground_url,
        'host_http': gateway_host_http,
        'secured': user_input.secured,
    }


def get_docarray(dataset):
    if os.path.exists(dataset):
        print(f'Loading queries from {dataset}')
        return DocumentArray.load_binary(dataset)
    print(f'Pulling queries from {dataset}')
    da = DocumentArray.pull(name=dataset, show_progress=True)
    if 'NOW_CI_RUN' in os.environ:
        da = da[:21]
    return da


def compare_flows(**kwargs):
    if not 'flow_ids' in kwargs:
        path_req_params = maybe_prompt_user(
            [
                {
                    'type': 'input',
                    'name': 'path_req_params',
                    'message': 'Path to json file mapping flow ID to key-value pairs for '
                    'the search request parameters (optional):',
                }
            ],
            'path_req_params',
            **kwargs,
        )
        if path_req_params:
            with open(path_req_params) as fp:
                cluster_ids_2_req_params = json.load(fp)
            flow_ids = list(cluster_ids_2_req_params.keys())
            flow_ids_http_req_params = [
                (flow_id, f'https://{flow_id}-http.wolf.jina.ai', req_params)
                for flow_id in flow_ids
                for req_params in cluster_ids_2_req_params[flow_id]
            ]
    if 'flow_ids' in kwargs or not path_req_params:
        flow_ids = maybe_prompt_user(
            [
                {
                    'type': 'input',
                    'name': 'flow_ids',
                    'message': 'Enter comma-separated the flow names to compare:',
                }
            ],
            'flow_ids',
            **kwargs,
        )
        flow_ids_http_req_params = [
            (cluster_id, f'https://{cluster_id}-http.wolf.jina.ai', {})
            for cluster_id in flow_ids.split(',')
        ]

    dataset = maybe_prompt_user(
        [
            {
                'type': 'input',
                'name': 'dataset',
                'message': 'Path to the DocArray with the queries in multi-modal format',
            }
        ],
        'dataset',
        **kwargs,
    )
    da = get_docarray(dataset)
    if not da[0].is_multimodal:
        raise ValueError(
            f'The DocArray {dataset} is not a multimodal DocumentArray.'
            f'Please check documentation https://docarray.jina.ai/fundamentals/dataclass/construct/'
        )

    limit = maybe_prompt_user(
        [
            {
                'type': 'input',
                'name': 'limit',
                'message': 'Enter the number of results to compare:',
            }
        ],
        'limit',
        **kwargs,
    )
    limit = int(limit)

    disable_to_datauri = maybe_prompt_user(
        [
            {
                'type': 'list',
                'choices': [
                    {'name': '⛔ no', 'value': False},
                    {'name': '✅ yes', 'value': True},
                ],
                'name': 'disable_to_datauri',
                'message': 'Disable loading to DataURI (makes the files smaller but also not self-contained)?',
            }
        ],
        'disable_to_datauri',
        **kwargs,
    )

    results_per_table = maybe_prompt_user(
        [
            {
                'type': 'input',
                'name': 'results_per_table',
                'message': 'Enter the number of results shown per table (default is 20):',
            }
        ],
        'results_per_table',
        **kwargs,
    )
    results_per_table = int(results_per_table) if results_per_table else 20

    compare_flows_for_queries(
        da=da,
        flow_ids_http_req_params=flow_ids_http_req_params,
        limit=limit,
        results_per_table=results_per_table,
        disable_to_datauri=disable_to_datauri,
    )


def get_flow_status(action, **kwargs):
    choices = []
    # Add all remote Flows that exists with the namespace `nowapi`
    alive_flows = deployment.list_all_wolf()
    for flow_details in alive_flows:
        choices.append(flow_details['name'])
    if len(choices) == 0:
        cowsay.cow(f'nothing to {action}')
        return
    else:
        questions = [
            {
                'type': 'list',
                'name': 'cluster',
                'message': f'Which cluster do you want to {action}?',
                'choices': choices,
            }
        ]
        cluster = maybe_prompt_user(questions, 'cluster', **kwargs)

    flow = [x for x in alive_flows if x['name'] == cluster][0]
    flow_id = flow['id']
    _result = deployment.status_wolf(flow_id)
    if _result is None:
        print(f'❎ Flow not found in JCloud. Likely, it has been deleted already')
    return _result, flow_id, cluster


def _generate_info_table(gateway_host_http, bff_url, playground_url, user_input):
    info_table = Table(
        'Attribute',
        Column(header="Value", overflow="fold"),
        show_header=False,
        box=box.SIMPLE,
        highlight=True,
    )
    info_table.add_row('Host (HTTPS)', gateway_host_http)
    info_table.add_row('API docs', bff_url)
    if user_input.secured and user_input.api_key:
        info_table.add_row('API Key', user_input.api_key)
    info_table.add_row('Playground', playground_url)
    console = Console()
    console.print(
        Panel(
            info_table,
            title=f':tada: Search app is NOW ready!',
            expand=False,
        )
    )

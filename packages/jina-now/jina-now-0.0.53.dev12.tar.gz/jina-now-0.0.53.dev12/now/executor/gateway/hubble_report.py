import datetime
import json
import os

from hubble.payment.client import PaymentClient
from jina.logging.logger import JinaLogger

from now.constants import (
    NOWGATEWAY_SEARCH_FEE_PRO_QUANTITY,
    NOWGATEWAY_SEARCH_FEE_QUANTITY,
)

logger = JinaLogger(__file__)
payment_client = None
authorized_jwt = None
old_user_token = None


def current_time():
    return datetime.datetime.utcnow().isoformat() + 'Z'


def save_cred(storage_dir):
    if storage_dir and os.path.exists(storage_dir):
        with open(f'{storage_dir}/cred.json', 'w+') as f:
            json.dump({'authorized_jwt': authorized_jwt}, f)
    else:
        logger.info('No storage dir found. Not saving cred.json')


def init_payment_params(user_token, inf_token, storage_dir):
    logger.info('Starting base fee thread')
    global old_user_token, authorized_jwt
    old_user_token = user_token  # incase no token is passed with search request
    if inf_token:  # if inf_token is passed, use it mostly in case of gateway restart
        authorized_jwt = inf_token
    init_payment_client(user_token)
    save_cred(storage_dir)


def report_search_usage(user_token):
    logger.info('** Entered report_search_usage() **')
    init_payment_client(user_token)
    report(
        quantity_basic=NOWGATEWAY_SEARCH_FEE_QUANTITY,
        quantity_pro=NOWGATEWAY_SEARCH_FEE_PRO_QUANTITY,
    )


def init_payment_client(user_token):
    global payment_client
    global authorized_jwt
    try:
        if payment_client is None:
            m2m_token = os.environ.get('M2M')
            if not m2m_token:
                raise ValueError('M2M not set in the environment')
            logger.info(f'M2M_TOKEN: {m2m_token[:10]}...{m2m_token[-10:]}')
            payment_client = PaymentClient(m2m_token=m2m_token)
        if authorized_jwt is None:
            logger.info('No authorized JWT found. Getting one...')
            # Try with the new token provided. If not then use the old one
            jwt = payment_client.get_authorized_jwt(
                user_token=user_token or old_user_token
            )['data']
            authorized_jwt = jwt  # store it as a global variable to avoid re-auth
    except Exception as e:
        import traceback

        traceback.print_exc()
        # Do not continue with request if initialization fails
        raise e


def report(quantity_basic, quantity_pro, auth_jwt=None):
    global authorized_jwt
    global payment_client
    m2m_token = os.environ.get('M2M')
    payment_client = payment_client or PaymentClient(m2m_token=m2m_token)
    authorized_jwt = authorized_jwt or auth_jwt
    logger.info('Time of reporting for credits usage: {}'.format(current_time()))
    app_id = 'search'
    try:
        logger.info(f'Authorized JWT: {authorized_jwt[:10]}...{authorized_jwt[-10:]}')
        summary = get_summary(auth_jwt=authorized_jwt)
        product_id = summary['internal_product_id']
        logger.info(f'Credits before: {summary["credits"]} & product_id: {product_id}')
        if product_id == 'free-plan':
            quantity = quantity_basic
        else:
            quantity = quantity_pro
        if can_charge(summary):
            payment_client.report_usage(authorized_jwt, app_id, product_id, quantity)  # type: ignore
            logger.info(f'**** `{round(quantity, 3)}` credits charged ****')
            summary = get_summary(auth_jwt=authorized_jwt)
            logger.info(f'Credits after: {summary["credits"]}')
        else:
            logger.info(f'**** Could not charge. Check payment summary ****')
        logger.info(f'Payment summary: {summary}')
    except Exception as e:
        import traceback

        traceback.print_exc()
        # Do not continue with request if payment fails
        raise e


def get_summary(auth_jwt=None):
    global authorized_jwt
    global payment_client
    m2m_token = os.environ.get('M2M')
    payment_client = payment_client or PaymentClient(m2m_token=m2m_token)
    authorized_jwt = authorized_jwt or auth_jwt
    resp = payment_client.get_summary(token=authorized_jwt, app_id='search')  # type: ignore
    has_payment_method = resp['data'].get('hasPaymentMethod', False)
    user_credits = resp['data'].get('credits', None)
    internal_product_id = resp['data'].get('internalProductId', None)
    user_account_status = resp['data'].get('userAccountStatus', None)
    return {
        'has_payment_method': has_payment_method,
        'credits': user_credits,
        'internal_product_id': internal_product_id,
        'user_account_status': user_account_status,
    }


def can_charge(summary):
    return (
        (summary['credits'] is not None and summary['credits'] > 0)
        or summary['has_payment_method']
    ) and summary['user_account_status'] == 'active'

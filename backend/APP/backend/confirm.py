import json
import os
import logging
from linepay import LinePayApi
from common import utils
from line_pay.order_info import LinePayOrderInfo  # noqa501

# 環境変数
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
# LINE Pay API
LINE_PAY_CHANNEL_ID = os.environ.get("LINE_PAY_CHANNEL_ID")
LINE_PAY_CHANNEL_SECRET = os.environ.get("LINE_PAY_CHANNEL_SECRET")
if (os.environ.get("LINE_PAY_IS_SANDBOX") == 'True'
        or os.environ.get("LINE_PAY_IS_SANDBOX") == 'true'):
    LINE_PAY_IS_SANDBOX = True
else:
    LINE_PAY_IS_SANDBOX = False
api = LinePayApi(LINE_PAY_CHANNEL_ID,
                 LINE_PAY_CHANNEL_SECRET, is_sandbox=LINE_PAY_IS_SANDBOX)
# ログ出力の設定
logger = logging.getLogger()
if LOGGER_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
# テーブル操作クラスの初期化
order_info_table_controller = LinePayOrderInfo()


def lambda_handler(event, context):
    """
    LINE Pay API(confirm)の通信結果を返す
    Parameters
    ----------
        event : dict
            POST時に渡されたパラメータ
        context : dict
            コンテキスト内容。
    Returns
    -------
        response : dict
            LINE Pay APIの通信結果
    """
    logger.info(event)
    req_body = json.loads(event['body'])
    order_id = req_body['orderId']
    # 注文履歴から決済金額を取得
    order_info = order_info_table_controller.get_order_info(order_id)
    amount = float(order_info['amount'])
    transaction_id = int(req_body['transactionId'])
    currency = 'JPY'

    try:
        api_response = api.confirm(transaction_id, amount, currency)
    except Exception as e:
        logger.exception('Occur Exception: %s', e)
        return utils.create_error_response('Error')

    response = utils.create_success_response(
        json.dumps(api_response))
    return response

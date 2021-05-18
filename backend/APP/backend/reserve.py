import json
import os
import logging
import uuid
from linepay import LinePayApi
from common import utils
from line_pay.order_info import LinePayOrderInfo  # noqa501

# 環境変数
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
PAYMENT_IMG_URL = os.environ.get("PAYMENT_IMG_URL")
CONFIRM_URL = os.environ.get("CONFIRM_URL")
CANCEL_URL = os.environ.get("CANCEL_URL")
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
    LINE Pay API(reserve)の通信結果を返す
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
    user_id = req_body['userId']
    amount = 400
    order_id = str(uuid.uuid4())
    body = {
        "amount": amount,
        "currency": "JPY",
        "orderId": order_id,
        "packages": [{
            "id": "1",
            "amount": amount,
            "name": "Use Caseストア新宿店",
            "products": [{
                    "name": "購入商品",
                    "imageUrl": PAYMENT_IMG_URL,
                    "quantity": "1",
                    "price": amount
            }
            ]
        }],
        "redirectUrls": {
            "confirmUrl": CONFIRM_URL,
            "cancelUrl": CANCEL_URL
        },
        "options": {
            "payment": {
                "capture": "True"
            },
            "display": {
                "locale": "ja"
            }
        }
    }

    try:
        api_response = api.request(body)

        # DynamoDBに注文情報登録
        transaction_Id = api_response['info']['transactionId']
        order_info_table_controller.put_orderinfo(
            order_id, user_id, transaction_Id, amount)
    except Exception as e:
        logger.exception('Occur Exception: %s', e)
        return utils.create_error_response('Error')

    response = utils.create_success_response(
        json.dumps(api_response))
    return response

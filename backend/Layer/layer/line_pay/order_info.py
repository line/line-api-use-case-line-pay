"""
LinePayOrderInfo操作用モジュール

"""
import os
from datetime import datetime
from dateutil.tz import gettz

from aws.dynamodb.base import DynamoDB
from common import utils


class LinePayOrderInfo(DynamoDB):
    """LinePayOrderInfo操作用クラス"""
    __slots__ = ['_table']

    def __init__(self):
        """初期化メソッド"""
        table_name = os.environ.get("LINE_PAY_ORDER_INFO_DB")
        super().__init__(table_name)
        self._table = self._db.Table(table_name)

    def get_order_info(self, order_id):
        """
        order_idをもとに注文テーブルから注文情報を取得する
        Parameters
        ----------
            order_id : string
                注文番号(ConfirmURLのパラメータ)
        Returns
        -------
            order_info : dict
                注文情報
        """
        key = {'orderId': order_id}

        try:
            item = self._get_item(key)
        except Exception as e:
            raise e
        return item

    def put_orderinfo(self, order_id, user_id, transaction_id, amount):
        """
        DynamoDBに注文情報を新規登録する
        Parameters
        ----------
            order_id:string
                注文番号
            user_id:string
                LINEのユーザーID
            transaction_id:string
                決済用トランザクションID(reserveAPIの戻り値)
            amount:int
                決済金額
        Returns
        -------
            なし
        """
        now = datetime.now()
        datetime_now = str(now)
        item = {
            "orderId": order_id,
            "userId": user_id,
            "transactionId": transaction_id,
            "amount": amount,
            "orderTime": datetime_now,
            "expirationDate": utils.get_ttl_time(now),
            'createdTime': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S"),
            'updatedTime': datetime.now(
                gettz('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S"),

        }
        try:
            response = self._put_item(item)
        except Exception as e:
            raise e
        return response

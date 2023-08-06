# Basana
#
# Copyright 2022-2023 Gabriel Martin Becedillas Ruiz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from decimal import Decimal
from typing import Any, Dict, List, Optional

from . import client, common, helpers, spot_requests
from basana.core.enums import OrderOperation
from basana.core.pair import Pair


Balance = common.Balance
CanceledOCOOrder = common.CanceledOCOOrder
CanceledOrder = common.CanceledOrder
CreatedOCOOrder = common.CreatedOCOOrder
OCOOrderInfo = common.OCOOrderInfo
OrderInfo = common.OrderInfo


class Trade(common.Trade):
    @property
    def order_list_id(self) -> Optional[str]:
        ret = self.json.get("orderListId")
        ret = None if ret in [None, -1] else str(ret)
        return ret


class Fill(common.Fill):
    @property
    def trade_id(self) -> str:
        return str(self.json["tradeId"])


class CreatedOrder(common.CreatedOrder):
    @property
    def order_list_id(self) -> Optional[str]:
        ret = self.json["orderListId"]
        ret = None if ret == -1 else str(ret)
        return ret

    @property
    def fills(self) -> List[Fill]:
        # Only available for FULL responses.
        return [Fill(fill) for fill in self.json.get("fills", [])]


class OpenOrder(common.OpenOrder):
    @property
    def order_list_id(self) -> Optional[str]:
        ret = self.json.get("orderListId")
        ret = None if ret in [None, -1] else str(ret)
        return ret

    @property
    def quote_amount(self) -> Optional[Decimal]:
        return helpers.get_optional_decimal(self.json, "origQuoteOrderQty", True)


class Account:
    def __init__(self, cli: client.SpotAccount):
        self._cli = cli

    async def get_balances(self) -> Dict[str, Balance]:
        account_info = await self._cli.get_account_information()
        return {balance["asset"].upper(): Balance(balance) for balance in account_info["balances"]}

    async def create_order(self, order_request: spot_requests.ExchangeOrder) -> CreatedOrder:
        created_order = await order_request.create_order(self._cli)
        return CreatedOrder(created_order)

    async def create_market_order(
            self, operation: OrderOperation, pair: Pair, amount: Optional[Decimal] = None,
            quote_amount: Optional[Decimal] = None, client_order_id: Optional[str] = None, **kwargs: Dict[str, Any]
    ) -> CreatedOrder:
        return await self.create_order(spot_requests.MarketOrder(
            operation, pair, amount=amount, quote_amount=quote_amount, client_order_id=client_order_id, **kwargs
        ))

    async def create_limit_order(
            self, operation: OrderOperation, pair: Pair, amount: Decimal, limit_price: Decimal,
            time_in_force: str = "GTC", client_order_id: Optional[str] = None, **kwargs: Dict[str, Any]
    ) -> CreatedOrder:
        return await self.create_order(spot_requests.LimitOrder(
            operation, pair, amount, limit_price, time_in_force=time_in_force, client_order_id=client_order_id,
            **kwargs
        ))

    async def create_stop_limit_order(
            self, operation: OrderOperation, pair: Pair, amount: Decimal, stop_price: Decimal, limit_price: Decimal,
            time_in_force: str = "GTC", client_order_id: Optional[str] = None, **kwargs: Dict[str, Any]
    ) -> CreatedOrder:
        return await self.create_order(spot_requests.StopLimitOrder(
            operation, pair, amount, stop_price, limit_price, time_in_force=time_in_force,
            client_order_id=client_order_id, **kwargs
        ))

    async def get_order_info(
            self, pair: Pair, order_id: Optional[str] = None, client_order_id: Optional[str] = None,
            include_trades: bool = True
    ) -> OrderInfo:
        """ Returns information about an order.

        @param pair:
        @param order_id:
        @param client_order_id:
        @return:

        This requires making 2 requests to Binance.
        """
        order_book_symbol = helpers.pair_to_order_book_symbol(pair)
        order_info = await self._cli.query_order(
            order_book_symbol, order_id=None if order_id is None else int(order_id),
            orig_client_order_id=client_order_id
        )
        trades = []
        if include_trades:
            trades = [
                Trade(trade) for trade in await self._cli.get_trades(order_book_symbol, order_id=order_info["orderId"])
            ]
        return OrderInfo(order_info, trades)

    async def get_open_orders(self, pair: Optional[Pair] = None) -> List[OpenOrder]:
        order_book_symbol = None
        if pair:
            order_book_symbol = helpers.pair_to_order_book_symbol(pair)
        return [
            OpenOrder(open_order) for open_order in await self._cli.get_open_orders(order_book_symbol)
        ]

    async def cancel_order(
            self, pair: Pair, order_id: Optional[str] = None, client_order_id: Optional[str] = None,
    ) -> CanceledOrder:
        canceled_order = await self._cli.cancel_order(
            helpers.pair_to_order_book_symbol(pair), order_id=None if order_id is None else int(order_id),
            orig_client_order_id=client_order_id
        )
        return CanceledOrder(canceled_order)

    async def create_oco_order(
            self, operation: OrderOperation, pair: Pair, amount: Decimal, limit_price: Decimal, stop_price: Decimal,
            stop_limit_price: Optional[Decimal] = None, stop_limit_time_in_force: str = "GTC",
            list_client_order_id: Optional[str] = None, limit_client_order_id: Optional[str] = None,
            stop_client_order_id: Optional[str] = None, **kwargs: Dict[str, Any]
    ) -> CreatedOCOOrder:
        order_req = spot_requests.OCOOrder(
            operation, pair, amount, limit_price, stop_price, stop_limit_price=stop_limit_price,
            stop_limit_time_in_force=stop_limit_time_in_force, list_client_order_id=list_client_order_id,
            limit_client_order_id=limit_client_order_id, stop_client_order_id=stop_client_order_id,
            **kwargs
        )
        created_order = await order_req.create_order(self._cli)
        return CreatedOCOOrder(created_order)

    async def get_oco_order_info(
            self, order_list_id: Optional[str] = None, client_order_list_id: Optional[str] = None,
    ) -> OCOOrderInfo:
        order_info = await self._cli.query_oco_order(
            order_list_id=None if order_list_id is None else int(order_list_id),
            client_order_list_id=client_order_list_id
        )
        return OCOOrderInfo(order_info)

    async def cancel_oco_order(
            self, pair: Pair, order_list_id: Optional[str] = None, client_order_list_id: Optional[str] = None,
    ) -> CanceledOCOOrder:
        canceled_order = await self._cli.cancel_oco_order(
            helpers.pair_to_order_book_symbol(pair),
            order_list_id=None if order_list_id is None else int(order_list_id),
            client_order_list_id=client_order_list_id
        )
        return CanceledOCOOrder(canceled_order)

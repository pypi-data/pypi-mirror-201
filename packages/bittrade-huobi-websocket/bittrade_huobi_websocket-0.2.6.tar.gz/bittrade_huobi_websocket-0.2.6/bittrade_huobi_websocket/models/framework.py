from dataclasses import dataclass
from typing import Any, Callable, Literal, NamedTuple, Optional

from ccxt import huobi
from elm_framework_helpers.ccxt.models.orderbook import Orderbook
from reactivex import Observable
from reactivex.observable import ConnectableObservable
from reactivex.disposable import CompositeDisposable
from reactivex.scheduler import ThreadPoolScheduler
from elm_framework_helpers.websockets import models
from bittrade_huobi_websocket.models.enhanced_websocket import EnhancedWebsocket
from bittrade_huobi_websocket.models.response_message import ResponseMessage
from bittrade_huobi_websocket.models.rest import (
    market_depth,
    get_all_open_orders,
    order_details,
)
from bittrade_huobi_websocket.models import UserFeedMessage, HttpResponse

from bittrade_huobi_websocket.models.rest.cancel_orders_batch import (
    CancelOrdersBatchData,
    CancelOrdersBatchParams,
)
from bittrade_huobi_websocket.models.rest.create_order import (
    OrderCreateParams,
    OrderCreateResponse,
)
from bittrade_huobi_websocket.models.rest.cancel_order import CancelOrderParams


class BookConfig(NamedTuple):
    pair: str
    depth: int


@dataclass
class FrameworkContext:
    all_subscriptions: CompositeDisposable
    authenticated_sockets: Observable[EnhancedWebsocket]
    books: dict[str, Observable[Orderbook]]
    cancel_all_http: Callable[
        [Optional[CancelOrdersBatchParams]], Observable[CancelOrdersBatchData]
    ]
    cancel_order_http: Callable[[CancelOrderParams], Observable[bool]]
    create_order_http: Callable[
        [OrderCreateParams],
        Observable[OrderCreateResponse],
    ]
    get_book_http: Callable[
        [market_depth.MarketDepthParams], Observable[HttpResponse]
    ]
    get_account_balance_http: Callable[
        [str], Observable[HttpResponse]
    ]
    exchange: huobi
    load_all_open_orders: Callable[
        [get_all_open_orders.AllOpenOrdersParams],
        Observable[list[get_all_open_orders.AllOpenOrder]],
    ]
    public_socket_connection: ConnectableObservable[models.WebsocketBundle]
    private_socket_connection: ConnectableObservable[models.WebsocketBundle]
    private_messages: Observable[ResponseMessage]
    scheduler: ThreadPoolScheduler
    websocket_bs: models.EnhancedWebsocketBehaviorSubject
    open_orders_http: Callable[
        [get_all_open_orders.AllOpenOrdersParams],
        Observable[HttpResponse],
    ]
    order_details_http: Callable[[str], Observable[HttpResponse]]

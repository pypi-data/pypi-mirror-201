import functools
from typing import Any, Callable
from reactivex import Observable, operators

from logging import getLogger
from typing import Callable, Optional, cast, TYPE_CHECKING

import requests
from ccxt import huobi
from reactivex import Observable, operators
from reactivex.disposable import CompositeDisposable
from reactivex.operators import flat_map, share
from reactivex.scheduler import ThreadPoolScheduler
from reactivex.subject import BehaviorSubject
from bittrade_huobi_websocket import models
from elm_framework_helpers.websockets.operators import connection_operators
from bittrade_huobi_websocket.connection import (
    private_websocket_connection,
    public_websocket_connection,
)
from bittrade_huobi_websocket.rest.cancel_order import cancel_order_http_factory
from bittrade_huobi_websocket.rest.create_order import create_order_http_factory
from bittrade_huobi_websocket.rest.order_details import order_details_http_factory
from bittrade_huobi_websocket.rest.get_account_balance import get_account_balance_http_factory
from bittrade_huobi_websocket.rest.get_book import get_book_http
from bittrade_huobi_websocket.rest.cancel_orders_batch import (
    cancel_orders_batch_http_factory,
)
from bittrade_huobi_websocket.rest.get_all_open_orders import (
    get_all_open_orders_http_factory,
    load_all_open_orders
)

from bittrade_huobi_websocket.models.framework import FrameworkContext
from elm_framework_helpers.output import debug_operator


logger = getLogger(__name__)


def get_framework(
    add_token: Callable[
        [Observable[models.ResponseMessage]],
        Callable[
            [Observable[models.EnhancedWebsocket]], Observable[models.ResponseMessage]
        ],
    ],
    add_token_http: Callable[[requests.models.Request], requests.models.Request],
    books: Optional[tuple[Any]] = None,
    load_markets=True,
) -> FrameworkContext:
    # books = books or cast(tuple[BookConfig], ())
    exchange = huobi()
    if load_markets:
        exchange.load_markets()
    pool_scheduler = ThreadPoolScheduler(200)
    all_subscriptions = CompositeDisposable()
    # Set up sockets
    # public_sockets = public_websocket_connection()
    private_sockets = private_websocket_connection()
    public_sockets = None

    # public_messages = public_sockets.pipe(connection_operators.keep_messages_only(), share())
    private_messages = private_sockets.pipe(
        connection_operators.keep_messages_only(), share()
    )

    authenticated_sockets = private_sockets.pipe(
        connection_operators.keep_new_socket_only(),
        add_token(private_messages),
        share(),
    )

    socket_bs = BehaviorSubject(cast(models.EnhancedWebsocket, None))
    authenticated_sockets.subscribe(socket_bs)
    guaranteed_socket = socket_bs.pipe(
        operators.filter(lambda x: bool(x)),
    )
    get_all_open_orders_http = get_all_open_orders_http_factory(add_token_http)

    return FrameworkContext(
        all_subscriptions=all_subscriptions,
        authenticated_sockets=authenticated_sockets,
        books={},
        cancel_all_http=cancel_orders_batch_http_factory(add_token_http),
        cancel_order_http=cancel_order_http_factory(add_token_http),
        create_order_http=create_order_http_factory(add_token_http),
        get_book_http=get_book_http,
        get_account_balance_http=get_account_balance_http_factory(add_token_http),
        exchange=exchange,
        load_all_open_orders=functools.partial(load_all_open_orders, get_all_open_orders_http),
        open_orders_http=get_all_open_orders_http,
        order_details_http=order_details_http_factory(add_token_http),
        public_socket_connection=public_sockets,
        private_socket_connection=private_sockets,
        private_messages=private_messages,
        scheduler=pool_scheduler,
        websocket_bs=socket_bs,
    )

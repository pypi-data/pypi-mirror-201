from datetime import datetime
from typing import Any, Callable
from uuid import uuid4
from elm_framework_helpers.websockets import models
import orjson
from bittrade_binance_websocket.sign import (
    del_none,
    encode_query_string,
    get_signature,
    to_sorted_qs,
)
from expression.core import pipe


class EnhancedWebsocket(models.EnhancedWebsocket):
    key: str
    secret: str

    def get_timestamp(self) -> str:
        return str(int(datetime.now().timestamp() * 1e3))

    def send_message(self, message: Any) -> int | str:
        return self.send_json(message)

    def prepare_request(self, original_message: dict) -> tuple[str, bytes]:
        signer, get_timestamp = get_signature(self.secret), self.get_timestamp
        message = original_message.copy()
        id = message.get("id", str(uuid4()))
        message["id"] = id
        # TODO accept a function to sign the request rather than hardcoding the credentials
        params = pipe(
            message.get("params", {}).copy(),
            del_none,
            lambda x: {**x, "apiKey": self.key, "timestamp": get_timestamp()},
            lambda x: {
                **x,
                "signature": pipe(x, to_sorted_qs, encode_query_string, signer),
            },
        )
        message["params"] = params
        return message["id"], orjson.dumps(message)

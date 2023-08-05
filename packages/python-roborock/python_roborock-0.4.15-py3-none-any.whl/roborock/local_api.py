from __future__ import annotations

import asyncio
import logging
import socket
from asyncio import Lock
from typing import Callable, Coroutine, Any

import async_timeout

from roborock.api import RoborockClient, SPECIAL_COMMANDS
from roborock.containers import RoborockLocalDeviceInfo
from roborock.exceptions import RoborockTimeout, CommandVacuumError, RoborockConnectionException
from roborock.typing import RoborockCommand
from roborock.util import get_running_loop_or_create_one

secured_prefix = 199
get_prefix = 119
app_prefix = 135
set_prefix = 151
nop_prefix = 21

_LOGGER = logging.getLogger(__name__)

APP_COMMANDS = (
    RoborockCommand.GET_MULTI_MAPS_LIST,
    RoborockCommand.GET_CLEAN_RECORD,
    RoborockCommand.GET_DUST_COLLECTION_MODE,
    RoborockCommand.GET_WASH_TOWEL_MODE,
    RoborockCommand.GET_SMART_WASH_PARAMS,
    "app_"
)

SET_COMMANDS = (
    "set_"
)


class RoborockLocalClient(RoborockClient):

    def __init__(self, devices_info: dict[str, RoborockLocalDeviceInfo]):
        super().__init__("abc", devices_info)
        self.loop = get_running_loop_or_create_one()
        self.device_listener: dict[str, RoborockSocketListener] = {
            device_id: RoborockSocketListener(device_info.network_info.ip, device_id, self.on_message)
            for device_id, device_info in devices_info.items()
        }
        self._mutex = Lock()

    async def async_connect(self):
        await asyncio.gather(*[
            listener.connect()
            for listener in self.device_listener.values()
        ])

    async def async_disconnect(self) -> Any:
        await asyncio.gather(*[listener.disconnect() for listener in self.device_listener.values()])

    # async def test(
    #         self, device_id: str
    # ):
    #     request_id, timestamp, payload = self._get_payload(RoborockCommand.NOP)
    #     prefix = 21
    #     request_protocol = 0
    #     msg = self._encode_msg(device_id, request_id, request_protocol, timestamp, payload, prefix)
    #     # Send the command to the Roborock device
    #     listener = self.device_listener.get(device_id)
    #     await listener.send_message(msg)
    #     response_protocol = 1
    #     (response, err) = await self._async_response(request_id, response_protocol)
    #     if err:
    #         raise CommandVacuumError('NOP', err) from err
    #     _LOGGER.debug(f"id={request_id} Response from NOP: {response}")
    #     return response

    async def send_command(
            self, device_id: str, method: RoborockCommand, params: list = None
    ):
        secured = True if method in SPECIAL_COMMANDS else False
        request_id, timestamp, payload = self._get_payload(method, params, secured)
        _LOGGER.debug(f"id={request_id} Requesting method {method} with {params}")
        prefix = secured_prefix if method in SPECIAL_COMMANDS \
            else app_prefix if method.startswith(APP_COMMANDS) \
            else set_prefix if method.startswith(SET_COMMANDS) \
            else get_prefix
        request_protocol = 4
        msg = self._encode_msg(device_id, request_id, request_protocol, timestamp, payload, prefix)
        # Send the command to the Roborock device
        listener = self.device_listener.get(device_id)
        await listener.send_message(msg)
        response_protocol = 5 if prefix == secured_prefix else 4
        (response, err) = await self._async_response(request_id, response_protocol)
        if err:
            raise CommandVacuumError(method, err) from err
        _LOGGER.debug(f"id={request_id} Response from {method}: {response}")
        return response


class RoborockSocket(socket.socket):
    _closed = None

    @property
    def is_closed(self):
        return self._closed


class RoborockSocketListener:
    roborock_port = 58867

    def __init__(self, ip: str, device_id: str, on_message: Callable[[str, bytes], Coroutine[None] | None],
                 timeout: float | int = 4):
        self.ip = ip
        self.device_id = device_id
        self.socket = RoborockSocket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)
        self.loop = get_running_loop_or_create_one()
        self.on_message = on_message
        self.timeout = timeout
        self.is_connected = False
        self._mutex = Lock()

    async def _main_coro(self):
        while not self.socket.is_closed:
            try:
                message = await self.loop.sock_recv(self.socket, 4096)
                try:
                    await self.on_message(self.device_id, message)
                except Exception as e:
                    _LOGGER.exception(e)
            except BrokenPipeError as e:
                _LOGGER.exception(e)
                await self.disconnect()

    async def connect(self):
        async with self._mutex:
            if not self.is_connected or self.socket.is_closed:
                self.socket = RoborockSocket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.setblocking(False)
                try:
                    async with async_timeout.timeout(self.timeout):
                        _LOGGER.info(f"Connecting to {self.ip}")
                        await self.loop.sock_connect(self.socket, (self.ip, 58867))
                        self.is_connected = True
                except Exception as e:
                    await self.disconnect()
                    raise RoborockConnectionException(f"Failed connecting to {self.ip}") from e
                self.loop.create_task(self._main_coro())

    async def disconnect(self):
        self.socket.close()
        self.is_connected = False

    async def send_message(self, data: bytes):
        response = {}
        await self.connect()
        try:
            async with self._mutex:
                async with async_timeout.timeout(self.timeout):
                    await self.loop.sock_sendall(self.socket, data)
        except (asyncio.TimeoutError, asyncio.CancelledError):
            raise RoborockTimeout(
                f"Timeout after {self.timeout} seconds waiting for response"
            ) from None
        except BrokenPipeError as e:
            _LOGGER.exception(e)
            await self.disconnect()
        return response

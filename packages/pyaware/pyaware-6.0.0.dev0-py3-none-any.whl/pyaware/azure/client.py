import asyncio
import functools
import time
import typing
import logging
import datetime
import random
from dataclasses import dataclass

import ifaddr
import pydantic

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import MethodRequest, MethodResponse, Message
from azure.iot.device import exceptions
import pyaware
from pyaware import events, store
from pyaware.azure.config import DeviceCredentials, PARSERS
from pyaware.mqtt import models
from pyaware.mqtt import factories

log = logging.getLogger(__file__)
logging.getLogger("azure.iot").setLevel(logging.WARNING)
logging.getLogger("azure.iot.device.common.handle_exceptions").setLevel(logging.ERROR)


def handle_exceptions(f):
    last_error = None
    last_error_cnt = 0

    @functools.wraps(f)
    async def _wrapped(*args, **kwargs):
        nonlocal last_error_cnt
        nonlocal last_error
        try:
            ret_val = await f(*args, **kwargs)
            last_error = None
            last_error_cnt = 0
            return ret_val
        except exceptions.ConnectionDroppedError as e:
            current_error = e
        except exceptions.ConnectionFailedError as e:
            current_error = e
        except exceptions.NoConnectionError as e:
            current_error = e
        except exceptions.CredentialError as e:
            current_error = e
        except exceptions.ClientError as e:
            current_error = e
        except exceptions.OperationCancelled as e:
            current_error = e
        except exceptions.OperationTimeout as e:
            current_error = e
        if last_error == type(current_error):
            last_error_cnt += 1
        else:
            last_error = type(current_error)
            last_error_cnt = 1
        if last_error_cnt < 5:
            log.error(current_error)
        if last_error_cnt == 5:
            log.warning(current_error)
            log.info(f"Suppressing further '{str(current_error)}' until change")

    return _wrapped


@events.enable
class AzureIotGateway:
    def __init__(self, name: str, credentials: str, parsers: str):
        self.name = name
        self.credentials = credentials
        self.client = IoTHubDeviceClient.create_from_connection_string(credentials)
        self.evt_connected: asyncio.Event = asyncio.Event()
        self.client.on_connection_state_change = self.connection_state_changed
        # Patch methods to capture exceptions
        self.client.send_message = handle_exceptions(self.client.send_message)
        self.client.get_twin = handle_exceptions(self.client.get_twin)
        self.client.connect = handle_exceptions(self.client.connect)
        self.client.send_method_response = handle_exceptions(
            self.client.send_method_response
        )
        self.config_received: asyncio.Event = asyncio.Event()
        self.twin = {}
        self.config: dict = {}
        self.devices: typing.Dict[str, AzureIotDevice] = {}
        self.device_config: typing.List[DeviceCredentials] = []
        self.parsers = PARSERS[parsers]
        self.message_manager = MessageManager(self.parsers())
        self.backlog_manager = BacklogManager(self)
        self.gateway_heartbeat = GatewayHeartbeat()
        asyncio.create_task(self.gateway_heartbeat.run())
        asyncio.create_task(self.backlog_manager.run())
        self.loop = asyncio.get_event_loop()

    def connection_state_changed(self):
        if self.client.connected:
            log.info("Connected to Azure IOT")
            # This cbf is set when connected as it attempts to connect when the cbf is set
            self.client.on_method_request_received = self.handle_method_request_received
            self.evt_connected.set()
            asyncio.run_coroutine_threadsafe(self.sync_twin(), self.loop)
        else:
            log.info("Lost connection to Azure IOT")
            self.evt_connected.clear()

    async def connect(self):
        """
        The connect method needs to be called in a loop as the azure client will only attempt connection once if it
        hasn't been connected in the past. Once connected it will properly maintain connection logic.
        Any additional device operations will also attempt to connect to the client.
        """
        try:
            while True:
                await self.client.connect()
                if self.client.connected:
                    log.info("Connected to Azure IOT")
                    # This cbf is set when connected as it attempts to connect when the cbf is set
                    self.client.on_method_request_received = (
                        self.handle_method_request_received
                    )
                    asyncio.create_task(self.sync_twin())
                    self.evt_connected.set()
                    return
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            pass
        except pyaware.exceptions.StopException:
            pass
        except Exception:
            raise

    async def sync_twin(self):
        self.twin = await self.client.get_twin()
        log.info("Synchronised digital twin")
        self.handle_config()

    async def handle_method_request_received(self, request: MethodRequest):
        if request.name == "stop":
            await self.handle_pyaware_stop(request)
        elif request.name == "debug":
            await self.handle_debug(request, request.payload)

    async def handle_pyaware_stop(self, request: MethodRequest):
        await self.client.send_method_response(MethodResponse(request.request_id, 200))
        pyaware.stop()

    async def handle_debug(self, request: MethodRequest, payload):
        try:
            log.info("Debug command received: {}".format(payload))
            pyaware.logger.runtime_logger.load(payload)
        except asyncio.CancelledError:
            pass
        except Exception:
            await self.client.send_method_response(
                MethodResponse(request.request_id, 500)
            )
            return
        await self.client.send_method_response(MethodResponse(request.request_id, 200))

    def handle_config(self):
        """
        Callback when a new configuration is sent via mqtt.
        If the gateway handle config to update devices and set up remaining pyaware config
        :return:
        """
        config = self.twin.get("desired", {}).get("configuration", {})
        if config:
            try:
                old_config = pyaware.config.load_yaml_config(
                    pyaware.config.config_main_path
                )
            except OSError:
                old_config = {}
            if old_config != config:
                pyaware.config.save_yaml_config(pyaware.config.config_main_path, config)
                if self.config_received.is_set():
                    log.warning("New gateway configuration detected. Stopping process")
                    pyaware.stop()
            if not self.config_received.is_set():
                self.config_received.set()
                self.config = config
                self.device_config = [
                    DeviceCredentials(**x)
                    for x in self.config.get("device_credentials", [])
                ]
                asyncio.create_task(self.setup_devices())
            asyncio.create_task(
                self.client.patch_twin_reported_properties({"configuration": config})
            )
        else:
            log.info("Gateway configuration received was empty")

    def load_config_from_disk(self):
        try:
            self.config = pyaware.config.load_yaml_config(
                pyaware.config.config_main_path
            )
            self.config_received.set()
        except FileNotFoundError:
            log.warning("No valid gateway configuration detected. Stopping process")
            pyaware.stop()

    async def setup_devices(self):
        for device_credentials in self.device_config:
            self.devices[device_credentials.name] = AzureIotDevice(device_credentials)
            asyncio.create_task(self.devices[device_credentials.name].connect())

    @events.subscribe(topic="trigger_send")
    @handle_exceptions
    async def send(self, *, data: dict, topic_type: str, device_id: str = "", **kwargs):
        if topic_type == "telemetry":
            msg = self.message_manager.form_payload(data, topic_type, **kwargs)
            try:
                await self.send_message(device_id, topic_type, msg)
            except (
                exceptions.ConnectionFailedError,
                exceptions.ConnectionDroppedError,
                exceptions.NoConnectionError,
            ) as e:
                await self.backlog_manager.insert(
                    payload=msg, topic_type=topic_type, device_id=device_id
                )
                raise e
        elif topic_type == "state":
            msg = data.copy()
            msg.pop("timestamp", None)
            await self.client.patch_twin_reported_properties(msg)

    async def send_message(self, device_id: str, topic_type: str, payload: str):
        msg = Message(f'{{"topic-type": {topic_type}, "payload": {payload}}}')
        if device_id:
            await self.devices[device_id].client.send_message(msg)
        else:
            await self.client.send_message(msg)


@events.enable
class AzureIotDevice:
    def __init__(self, device_credentials: DeviceCredentials):
        self.name = device_credentials.name
        self.connection_string = device_credentials.primary_connection_string
        self.client = IoTHubDeviceClient.create_from_connection_string(
            self.connection_string
        )
        self.twin = {}
        self.cmds_active = set()

    async def connect(self):
        """
        The connect method needs to be called in a loop as the azure client will only attempt connection once if it
        hasn't been connected in the past. Once connected it will properly maintain connection logic.
        Any additional device operations will also attempt to connect to the client.
        """
        try:
            while True:
                await self.client.connect()
                if self.client.connected:
                    log.info(f"Connected to Azure IOT for device {self.name}")
                    # This cbf is set when connected as it attempts to connect when the cbf is set
                    self.client.on_method_request_received = (
                        self.handle_method_request_received
                    )
                    asyncio.create_task(self.sync_twin())
                    return
                await asyncio.sleep(5)
        except asyncio.CancelledError:
            pass
        except pyaware.exceptions.StopException:
            pass
        except Exception:
            raise

    async def sync_twin(self):
        self.twin = await self.client.get_twin()
        log.info(f"Synchronised digital twin for device {self.name}")
        self.handle_config()

    def handle_method_request_received(self, request: MethodRequest):
        self.handle_commands(request)

    def handle_config(self):
        """
        Callback when a new configuration is sent via mqtt.
        If the gateway handle config to update devices and set up remaining pyaware config
        :return:
        """

    def handle_commands(self, request: MethodRequest):
        model = models.get_model({"name": "CommandRequestV2"})
        try:
            msg = model.parse_obj(
                {"name": request.name, "id": request.request_id, **request.payload}
            ).dict(exclude_none=True)
        except pydantic.ValidationError as e:
            log.error(repr(e))
            resp = {
                "id": request.request_id,
                "type": 3,
                "timestamp": datetime.datetime.utcnow(),
                "message": e.json(),
            }
            self.cmds_active.add(request.request_id)
            events.publish(
                "mqtt_command_response",
                data=resp,
                timestamp=datetime.datetime.utcnow(),
                device_id=self.name,
            )
            return

        self.cmds_active.add(request.request_id)
        pyaware.events.publish(
            f"mqtt_command/{self.name}",
            data=msg,
            timestamp=datetime.datetime.utcnow(),
        )

    @events.subscribe(topic=f"mqtt_command_response")
    async def publish_command_response(
        self, data: dict, timestamp: datetime.datetime, device_id: str
    ):
        if device_id == self.name and data.get("type", 0) > 1:
            model = models.get_model({"name": "CommandResponse"})
            msg = model.parse_obj(data).json(exclude_none=True)
            if data["type"] == 2:
                await self.client.send_method_response(
                    MethodResponse(data["id"], 200, msg)
                )
            else:
                await self.client.send_method_response(
                    MethodResponse(data["id"], 500, msg)
                )
            self.cmds_active.discard(data["id"])


class MessageManager:
    def __init__(self, parsers):
        self.parsers = parsers

    def form_payload(self, data: dict, topic_type: str, **kwargs) -> str:
        parser = self.parsers.get(topic_type, {})
        factory = factories.get_factory(parser.get("factory"))
        msg = factory(data=data, **kwargs)
        msg = models.model_to_json(parser.get("model", {}), msg)
        return msg


@dataclass
class BacklogManager:
    gateway: AzureIotGateway
    # The message frequency range will choose a random amount of seconds within the range between each message
    message_frequency_range: tuple = (5, 10)

    @staticmethod
    async def insert(device_id: str, payload: str, topic_type: str):
        await store.disk_storage_setup_evt.wait()
        await store.disk_storage.azure.insert(
            payload=payload, topic_type=f"{topic_type}_backlog", device_id=device_id
        )

    async def run(self):
        """
        Continually add messages the queue from the disk storage if they are not currently in flight
        :param a_callback: Callback to the message manager.
        Will block adding messages if the manager queue is full
        :return:
        """
        await store.disk_storage_setup_evt.wait()
        log.info(f"Backlog now starting")
        while True:
            start = None
            if pyaware.evt_stop.is_set():
                log.info("Shutting down azure backlog manager")
                return
            msg_cnt = 0
            try:
                async for batched_messages in store.disk_storage.azure.get_batched_unsent(
                    1000
                ):
                    if start is None:
                        start = time.time()
                    try:
                        await self.gateway.send_message(
                            batched_messages.device_id,
                            batched_messages.topic_type,
                            batched_messages.payload,
                        )
                    except KeyError:
                        log.info(
                            f"Backlog device id {batched_messages.device_id} not found"
                        )
                        continue
                    except (
                        exceptions.ConnectionFailedError,
                        exceptions.ConnectionDroppedError,
                        exceptions.NoConnectionError,
                    ):
                        continue
                    except ValueError as e:
                        log.error(e)
                    except Exception as e:
                        log.exception(e)
                        continue
                    await store.disk_storage_setup_evt.wait()
                    await store.disk_storage.azure.ack(*batched_messages.uids)
                    msg_cnt += len(batched_messages.uids)
                    await asyncio.sleep(random.randrange(*self.message_frequency_range))
                if msg_cnt > 0:
                    log.info(
                        f"Finished adding azure backlog for {msg_cnt} in {time.time() - start}s"
                    )
            except asyncio.CancelledError:
                if pyaware.evt_stop.is_set():
                    log.info("Shutting down azure backlog manager")
                    return
            except asyncio.InvalidStateError:
                log.info(
                    "This error shouldn't occur as it was fixed in https://github.com/omnilib/aiosqlite/issues/80"
                )
            except BaseException as e:
                log.error(repr(e))
            await asyncio.sleep(60)


class GatewayHeartbeat:
    def __init__(self):
        self.state_sent = False

    async def run(self):
        log.info("Starting Gateway Heartbeat")
        connections_save_state = []
        # Get all adapter static info and setup array
        adapter_info = [
            {
                "macAddress": await pyaware.config.get_mac_address(adapter.name),
                "adapter": adapter.name,
            }
            for adapter in ifaddr.get_adapters()
        ]
        while True:
            if pyaware.evt_stop.is_set():
                log.info("Closing gateway heartbeat")
                return
            try:
                connections = []
                # Collects network adapters, ip addresses and mac addresses
                for adapter in ifaddr.get_adapters():
                    for ip_address in adapter.ips:
                        if ip_address.is_IPv4:
                            connections = connections + [
                                {
                                    "adapter": ip_address.nice_name,
                                    "macAddress": info.get("macAddress"),
                                    "ipAddress": ip_address.ip,
                                }
                                for info in adapter_info
                                if adapter.name == info.get("adapter")
                            ]
                timestamp = datetime.datetime.now()
                data = {"network": connections, "timestamp": timestamp}
                # Send gateway heartbeat to mqtt
                events.publish(
                    f"trigger_send",
                    data=data,
                    timestamp=timestamp,
                    topic_type="gateway",
                )
                if connections != connections_save_state or not self.state_sent:
                    # Update the state of the gateway
                    asyncio.create_task(self.update_gateway_state(data))
                    connections_save_state = connections
                    self.state_sent = True
            except Exception as e:
                if not pyaware.evt_stop.is_set():
                    log.exception(e)
            try:
                await asyncio.sleep(30)
            except asyncio.CancelledError:
                if not pyaware.evt_stop.is_set():
                    log.warning("Gateway heartbeat cancelled without stop signal")
                    break

    async def update_gateway_state(self, data: dict):
        log.info("Gateway state change detected. Sending new state.")
        timestamp = datetime.datetime.now()
        state = {"network": data.get("network", {}), "timestamp": timestamp}
        events.publish(
            f"trigger_send",
            topic_type="state",
            data=state,
            timestamp=datetime.datetime.utcnow(),
        )
        # Update the gateway network topology
        events.publish(f"update_gateway_network/{id(self)}", data=data["network"])

import asyncio
import random
import uuid
import datetime
import logging
import json

from amqtt.client import MQTTClient, ConnectException
from amqtt.errors import MQTTException


TELEMETRY_TOPIC = "devices/00:90:e8:8d:95:***macid***/imac-***fieldbus***/***serial***/events/backfill"

payload_master_template = """{"version": 2, "type": "imac-controller-master", "timestamp": "***timestamp***", "values": [{"name": "address-resistance", "samples": 2, "latest": [0, 80, 82, 80, 80, 80, 0, 0, 0, 0, 85, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 79, 82, 81, 79, 79, 0, 0, 0, 0, 0, 85, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0, 0, 93, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 94, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 91, 0, 0, 93, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 76, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 76, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 76, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, {"name": "address-offline-count", "samples": 1, "latest": [0, 0, 6, 9, 13, 21, 0, 0, 0, 0, 63, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 5, 6, 10, 19, 0, 0, 0, 0, 0, 62, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}], "serial": "***serial***"}"""
payload_gg2_template1 = """{"version": 2, "type": "imac-module-gg2", "timestamp": "***timestamp***", "values": [{"name": "detector-under-range", "samples": 1, "latest": false}, {"name": "detector-low-warm-up", "samples": 1, "latest": false}, {"name": "detector-over-range", "samples": 1, "latest": false}, {"name": "detector-high-warm-up", "samples": 1, "latest": false}, {"name": "detector-high-soft-fault", "samples": 1, "latest": false}, {"name": "detector-low-soft-fault", "samples": 1, "latest": false}], "serial": "***imacserial***"}"""
payload_gg2_template2 = """{"version": 2, "type": "imac-module-gg2", "timestamp": "***timestamp***", "values": [{"name": "address-analog", "samples": 1, "latest": 42}, {"name": "set-point-1", "samples": 1, "latest": 7200}, {"name": "set-point-3", "samples": 1, "latest": 12000}, {"name": "set-point-2", "samples": 1, "latest": 8000}], "serial": "***imacserial***"}"""

logger = logging.getLogger(__name__)


def _gen_client_id():
    import os
    import socket

    pid = os.getpid()
    hostname = socket.gethostname()
    return "amqtt_sub/%d-%s" % (pid, hostname)


async def main():
    await publish_data(
        "mqtt://192.168.18.22",
        TELEMETRY_TOPIC,
        macid=1,
        fieldbus=21,
        serial=1000000001,
        imac_serial_start=1,
        imac_serial_end=41,
    )
    # await publish_data("mqtt://127.0.0.1", TELEMETRY_TOPIC, macid=1, fieldbus=21, serial=1000000001, imac_serial_start=1, imac_serial_end=41)


async def publish_data(
    url,
    topic: str,
    macid: int,
    fieldbus: int,
    serial: int,
    imac_serial_start: int,
    imac_serial_end: int,
):
    local_topic = (
        topic.replace("***macid***", f"{macid:02X}")
        .replace("***fieldbus***", f"{fieldbus}")
        .replace("***serial***", f"{serial}")
    )
    client_id = _gen_client_id()
    print("Connecting")
    client = MQTTClient(client_id=client_id)
    await client.connect(uri=url, cleansession=True)
    print("Connected")
    local_master = (
        payload_master_template.replace("***macid***", f"{macid:02X}")
        .replace("***fieldbus***", f"{fieldbus}")
        .replace("***serial***", f"{serial}")
    )
    local_gg2_template_1 = (
        payload_gg2_template1.replace("***macid***", f"{macid:02X}")
        .replace("***fieldbus***", f"{fieldbus}")
        .replace("***serial***", f"{serial}")
    )
    local_gg2_template_2 = (
        payload_gg2_template2.replace("***macid***", f"{macid:02X}")
        .replace("***fieldbus***", f"{fieldbus}")
        .replace("***serial***", f"{serial}")
    )
    try:
        while True:
            payloads = [
                random.choice(
                    (
                        local_master,
                        local_gg2_template_1,
                        local_gg2_template_2,
                    )
                )
                .replace("***timestamp***", datetime.datetime.now().isoformat())
                .replace(
                    "***imacserial***",
                    f"{random.randint(imac_serial_start,imac_serial_end)}-G4",
                )
                for _ in range(1000)
            ]
            payload = f"[{','.join(payloads)}]".encode("utf-8")
            try:
                await client.publish(local_topic, payload, qos=1)
            except Exception as e:
                print("Failed to publish")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

import datetime
import logging
import asyncio
import statistics

from amqtt.client import MQTTClient, ConnectException
from amqtt.errors import MQTTException

logger = logging.getLogger(__name__)


def _gen_client_id():
    import os
    import socket

    pid = os.getpid()
    hostname = socket.gethostname()
    return "amqtt_sub/%d-%s" % (pid, hostname)


async def do_sub(url, topic):
    client_id = _gen_client_id()
    client = MQTTClient(client_id=client_id)
    timestamps = []
    diffs = []
    try:
        await client.connect(uri=url, cleansession=True)
        prev = None
        await client.subscribe([(topic, 1)])
        while True:
            for x in range(50):
                try:
                    message = await client.deliver_message()
                    if message:
                        now = datetime.datetime.now()
                        timestamps.append(now)
                        if prev:
                            diff = (now - prev).total_seconds()
                            diffs.append(diff)
                            print(f"Time between messages: {diff}: {now.isoformat()}")
                        prev = now
                except MQTTException:
                    logger.debug("Error reading packet")
            print(f"Min time: {min(diffs)}")
            print(f"Max time: {max(diffs)}")
            print(f"Std Dev: {statistics.stdev(diffs)}")
            print(f"Mean: {statistics.mean(diffs)}")
            print(f"Median: {statistics.median(diffs)}")
            print(f"Median Low: {statistics.median_low(diffs)}")
            print(f"Median High: {statistics.median_high(diffs)}")
    except ConnectException as ce:
        logger.fatal("connection to '%s' failed: %r" % (url, ce))
    except asyncio.CancelledError:
        logger.fatal("Publish canceled due to previous error")
    except BaseException:
        await client.disconnect()


def main(*args, **kwargs):
    asyncio.run(
        do_sub("mqtt://192.168.18.22", "gateways/00:90:e8:8d:95:2f/imac-2/safe-gas")
    )


if __name__ == "__main__":
    main()

import asyncio
import os
import random
import uuid
import datetime
import sqlite3

import pyaware.store
import pyaware.config

TELEMETRY_TOPIC = "devices/00:90:e8:8d:95:aa/imac-0/1234567890/events/backfill"

payload_master_template = """{"version": 2, "type": "imac-controller-master", "timestamp": "***timestamp***", "values": [{"name": "address-resistance", "samples": 2, "latest": [0, 80, 82, 80, 80, 80, 0, 0, 0, 0, 85, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 79, 82, 81, 79, 79, 0, 0, 0, 0, 0, 85, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0, 0, 93, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 94, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 91, 0, 0, 93, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 76, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 76, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 76, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}, {"name": "address-offline-count", "samples": 1, "latest": [0, 0, 6, 9, 13, 21, 0, 0, 0, 0, 63, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 5, 6, 10, 19, 0, 0, 0, 0, 0, 62, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}], "serial": "1234567890"}"""
payload_gg2_template1 = """{"version": 2, "type": "imac-module-gg2", "timestamp": "***timestamp***", "values": [{"name": "detector-under-range", "samples": 1, "latest": false}, {"name": "detector-low-warm-up", "samples": 1, "latest": false}, {"name": "detector-over-range", "samples": 1, "latest": false}, {"name": "detector-high-warm-up", "samples": 1, "latest": false}, {"name": "detector-high-soft-fault", "samples": 1, "latest": false}, {"name": "detector-low-soft-fault", "samples": 1, "latest": false}], "serial": "***imacserial***"}"""
payload_gg2_template2 = """{"version": 2, "type": "imac-module-gg2", "timestamp": "***timestamp***", "values": [{"name": "address-analog", "samples": 1, "latest": 42}, {"name": "set-point-1", "samples": 1, "latest": 7200}, {"name": "set-point-3", "samples": 1, "latest": 12000}, {"name": "set-point-2", "samples": 1, "latest": 8000}], "serial": "***imacserial***"}"""


async def main():
    print("Setting up database")
    await pyaware.store.disk.init_db(
        **{"max_size": "500MB", "absolute_directory": os.getcwd()}
    )
    await asyncio.wait_for(pyaware.store.disk_storage.close(), 3)
    conn = sqlite3.connect("cache.db")
    page_size = 4096
    mb = 500

    int(mb * 1024 * 1024 / page_size)
    conn.execute(f"PRAGMA page_size=4096;")
    conn.execute(f"PRAGMA max_page_count={int(mb * 1024 * 1024 / page_size)};")
    conn.execute("PRAGMA journal_mode=WAL;")

    try:
        while True:
            many = [
                [
                    TELEMETRY_TOPIC,
                    random.choice(
                        (
                            payload_master_template,
                            payload_gg2_template1,
                            payload_gg2_template2,
                        )
                    )
                    .replace("***timestamp***", datetime.datetime.now().isoformat())
                    .replace("***imacserial***", f"{random.randint(1,41)}-G4"),
                    1,
                    str(uuid.uuid4()),
                    "test",
                    "telemetry",
                ]
                for _ in range(10000)
            ]
            try:
                conn.executemany(
                    "INSERT INTO mqtt (topic, payload, qos, uid, client, topic_type) values (?,?,?,?,?,?)",
                    many,
                )
                conn.commit()
                print("*", end="")
            except Exception as e:
                print("Filled database")
                break
    finally:
        print("Closing database connection")
        conn.close()


if __name__ == "__main__":
    asyncio.run(main())

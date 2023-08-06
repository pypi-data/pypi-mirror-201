import asyncio
import typing
import logging
from pathlib import Path
from uuid import uuid4
import aiosqlite
import pyaware.store
from dataclasses import dataclass

log = logging.getLogger(__file__)


async def init_db(
    relative_directory: str = "", absolute_directory: str = "", memory=False, **kwargs
):
    """
    Initialises the SQLite database with the path. Invalid paths supplied will default the cache to aware path
    :param relative_directory: Directory for the cache.db file relative to the aware path, will create directory if
    it doesn't exist
    :param absolute_directory: Directory for the cache.db file as an absolute directory, will create directory if
    it doesn't exist
    :param memory: Set this to true to use in memory SQLite, this will allow it to run without using disk access but
    will lose data in power loss. May want to limit database size in that case so that you don't run out of memory.
    :return:
    """
    if memory:
        path = Path(":memory:")
    elif absolute_directory:
        path_dir = Path(absolute_directory)
        try:
            path_dir.mkdir(exist_ok=True)
        except asyncio.CancelledError:
            raise
        except BaseException as e:
            log.error(repr(e))
            log.info(
                f"Failed to use config path {path_dir}, using default location for db {pyaware.config.aware_path}"
            )
            path_dir = pyaware.config.aware_path
        path = path_dir / "cache.db"
    elif relative_directory:
        path_dir = pyaware.config.aware_path / relative_directory
        try:
            path_dir.mkdir(exist_ok=True)
        except asyncio.CancelledError:
            raise
        except BaseException as e:
            log.error(repr(e))
            log.info(
                f"Failed to use config path {path_dir}, using default location for db {pyaware.config.aware_path}"
            )
            path_dir = pyaware.config.aware_path
        path = path_dir / "cache.db"
    else:
        path = pyaware.config.aware_path / "cache.db"
    log.info(f"Initialising database @ {path}")
    pyaware.store.disk_storage = DiskStorage(path, **kwargs)
    await pyaware.store.disk_storage.init()
    pyaware.store.disk_storage_setup_evt.set()
    log.info(f"Initialised database @ {path}")


@dataclass
class BatchedQueryReturn:
    qos: int
    topic: str
    topic_type: str
    payload: str
    uids: typing.List[str]


@dataclass
class BatchedAzureQueryReturn:
    topic_type: str
    payload: str
    device_id: str
    uids: typing.List[str]


class DiskStorage:
    def __init__(self, path: Path, **kwargs):
        self.path = path
        self.config = kwargs
        self.conn = None
        self.db_size_manager = DbSizeManager(**kwargs)
        self.mqtt: MqttStorage = MqttStorage(self.db_size_manager.clean_up)
        self.azure: AzureStorage = AzureStorage(
            self.db_size_manager.clean_up, 1024 * 240
        )
        self.versioning = DbVersionManager(**kwargs)

    async def init(self):
        """
        Initialises the database with WAL journaling mode for faster write access.
        DB size manager will limit the space of the SQLite file on disk and clean up old messages
        The MqttStorage will manage the mqtt persistence
        :return:
        """
        await self.versioning.init(self.path)
        self.conn = await aiosqlite.connect(self.path, isolation_level=None)
        self.db_size_manager.conn = self.conn
        await self.conn.execute("PRAGMA optimize;")
        await self.conn.execute("PRAGMA journal_mode=WAL;")
        await self.conn.execute("PRAGMA automatic_index=OFF;")
        await self.conn.execute("PRAGMA case_sensitive_like=OFF;")
        await self.conn.execute("PRAGMA synchronous=NORMAL;")
        await self.conn.execute("PRAGMA SQLITE_ENABLE_DBSTAT_VTAB;")
        await self.db_size_manager.init(self.conn)
        await self.mqtt.init(self.conn)
        await self.azure.init(self.conn)

    async def close(self):
        if self.conn:
            await self.conn.close()


def get_id(itm) -> int:
    return itm.inserted_primary_key[0]


def generator_of_dicts(itm):
    return (dict(x) for x in itm)


class MqttStorage:
    def __init__(self, cleanup_cbf):
        self.conn = None
        self.cleanup_cbf = cleanup_cbf
        self.conn_established: asyncio.Event = asyncio.Event()

    async def init(self, conn):
        self.conn = conn
        self.conn_established.set()

        await self.conn.execute(
            "CREATE TABLE IF NOT EXISTS mqtt (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "uid STRING, "
            "qos INTEGER, "
            "topic STRING, "
            "payload STRING, "
            "client STRING, "
            "topic_type STRING, "
            "CONSTRAINT mqtt_uid UNIQUE (uid)"
            ") "
        )
        await self.conn.execute("CREATE INDEX IF NOT EXISTS uids on mqtt (uid)")
        # Suppress the logging integrity error as we abuse it for recommitting entries on pulling from cache
        logging.getLogger("aiosqlite").disabled = True

    async def insert(
        self, topic: str, payload: str, qos: int, uid: str, client: str, topic_type: str
    ):
        """
        Insert a mqtt message into the db with the UUID.
        If the UUID exists it will raise an IntegrityError.
        This is when we are trying to cache a value for commit when it already exists
        The error is suppressed because we are using it as control flow in order to prevent
        each consecutive attempt to write a message to mqtt being committed to disk
        :param topic: Mqtt topic as string
        :param payload: String encoded JSON payload
        :param qos: QOS of the published message
        """
        for _ in range(2):
            try:
                await self.conn.execute(
                    "INSERT INTO mqtt (topic, payload, qos, uid, client, topic_type) values (?,?,?,?,?,?)",
                    (topic, payload, qos, uid, client, topic_type),
                )
                return
            except aiosqlite.IntegrityError:
                return
            except aiosqlite.OperationalError as e:
                if "disk is full" in str(e):
                    await self.cleanup_cbf()
                    continue
                else:
                    log.error(repr(e))

    async def _insert_delayed(
        self,
        topic: str,
        payload: str,
        qos: int,
        uid: str,
        delay: float,
        client: str,
        topic_type: str,
    ):
        await asyncio.sleep(delay)
        return await self.insert(topic, payload, qos, uid, client, topic_type)

    def insert_delayed(
        self,
        topic: str,
        payload: str,
        qos: int,
        uid: str,
        client: str,
        topic_type: str,
        delay: float = 2,
    ) -> asyncio.Future:
        assert qos in range(3)
        return asyncio.create_task(
            self._insert_delayed(topic, payload, qos, uid, delay, client, topic_type)
        )

    async def ack(self, *uids: str):
        await self.conn_established.wait()
        for i in range(0, len(uids), 500):
            batch = uids[i : i + 500]
            await self.conn.execute(
                f"DELETE FROM mqtt WHERE uid in ({','.join(['?'] * len(batch))})",
                batch[i : i + 500],
            )

    async def get_all_unsent(self, query_batch: int = 100) -> typing.AsyncGenerator:
        _id = 0
        while True:
            results_q = await self.conn.execute(
                "SELECT * from mqtt WHERE mqtt.id > ? ORDER BY id LIMIT ?",
                (_id, query_batch),
            )
            headings = [desc[0] for desc in results_q.description]
            results = await results_q.fetchall()
            if not results:
                break
            for res in results:
                res = {key: value for key, value in zip(headings, res)}
                _id = res.pop("id")
                yield res

    async def get_batched_unsent(
        self, query_batch: int = 100
    ) -> typing.AsyncGenerator[BatchedQueryReturn, None]:
        _id = 0
        while True:
            results_q = await self.conn.execute(
                "SELECT * from mqtt WHERE mqtt.id > ? ORDER BY id LIMIT ?",
                (_id, query_batch),
            )
            headings = [desc[0] for desc in results_q.description]
            results = await results_q.fetchall()
            if not results:
                break
            queries = await asyncio.get_event_loop().run_in_executor(
                None, self.process_batched_query, headings, results
            )
            for query in queries:
                yield query
            _id = results[-1][headings.index("id")]

    @staticmethod
    def process_batched_query(headings, results) -> typing.List[BatchedQueryReturn]:
        topic_index = headings.index("topic")
        topics = set(res[topic_index] for res in results)
        query = []
        for topic in topics:
            batched = {}
            # Common fields
            for res in results:
                if res[topic_index] == topic:
                    batched["qos"] = res[headings.index("qos")]
                    batched["topic"] = topic
                    batched["topic_type"] = res[headings.index("topic_type")]
                    break

            # Unique fields

            payloads = [
                res[headings.index("payload")]
                for res in results
                if res[topic_index] == topic
            ]
            batched[
                "payload"
            ] = f"[{','.join(payloads)}]"  # Assume payload is valid json
            batched["uids"] = [
                res[headings.index("uid")]
                for res in results
                if res[topic_index] == topic
            ]
            query.append(BatchedQueryReturn(**batched))
        return query


class AzureStorage:
    def __init__(self, cleanup_cbf, message_size_chr_maximum: int = 1024 * 300):
        self.conn = None
        self.cleanup_cbf = cleanup_cbf
        self.conn_established: asyncio.Event = asyncio.Event()
        # Maximum for azure is 256KB for device to cloud message.
        self.message_size_chr_maximum: int = message_size_chr_maximum

    async def init(self, conn):
        self.conn = conn
        self.conn_established.set()

        await self.conn.execute(
            "CREATE TABLE IF NOT EXISTS azure (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "device_id STRING, "
            "topic_type STRING, "
            "uid STRING, "
            "payload STRING, "
            "CONSTRAINT azure_uid UNIQUE (uid)"
            ") "
        )
        await self.conn.execute("CREATE INDEX IF NOT EXISTS uids on azure (uid)")
        # Suppress the logging integrity error as we abuse it for recommitting entries on pulling from cache
        logging.getLogger("aiosqlite").disabled = True

    async def insert(self, device_id: str, topic_type: str, payload: str):
        """
        Insert a mqtt message into the db with the UUID.
        If the UUID exists it will raise an IntegrityError.
        This is when we are trying to cache a value for commit when it already exists
        The error is suppressed because we are using it as control flow in order to prevent
        each consecutive attempt to write a message to mqtt being committed to disk
        """
        for _ in range(2):
            try:
                await self.conn.execute(
                    "INSERT INTO azure (device_id, topic_type, uid, payload) values (?,?,?,?)",
                    (device_id, topic_type, str(uuid4()), payload),
                )
                return
            except aiosqlite.IntegrityError:
                return
            except aiosqlite.OperationalError as e:
                if "disk is full" in str(e):
                    await self.cleanup_cbf()
                    continue
                else:
                    log.error(repr(e))

    async def ack(self, *uids: str):
        await self.conn_established.wait()
        for i in range(0, len(uids), 500):
            batch = uids[i : i + 500]
            await self.conn.execute(
                f"DELETE FROM azure WHERE uid in ({','.join(['?'] * len(batch))})",
                batch[i : i + 500],
            )

    async def get_batched_unsent(
        self, query_batch: int = 100
    ) -> typing.AsyncGenerator[BatchedAzureQueryReturn, None]:
        _id = 0
        while True:
            results_q = await self.conn.execute(
                "SELECT * from azure WHERE azure.id > ? ORDER BY id LIMIT ?",
                (_id, query_batch),
            )
            headings = [desc[0] for desc in results_q.description]
            results = await results_q.fetchall()
            if not results:
                break
            queries = await asyncio.get_event_loop().run_in_executor(
                None, self.process_batched_query, headings, results
            )
            for query in queries:
                yield query
            _id = results[-1][headings.index("id")]

    def process_batched_query(
        self, headings, results
    ) -> typing.List[BatchedAzureQueryReturn]:
        device_id_index = headings.index("device_id")
        devices = set(res[device_id_index] for res in results)
        queries = []
        for device in devices:
            topic_type = ""
            # Common fields
            for res in results:
                if res[device_id_index] == device:
                    topic_type = res[headings.index("topic_type")]
                    break

            # Unique fields
            payloads = [
                res[headings.index("payload")]
                for res in results
                if res[device_id_index] == device
            ]
            uids_all = [
                res[headings.index("uid")]
                for res in results
                if res[device_id_index] == device
            ]
            queries.extend(self.batch_payloads(device, topic_type, payloads, uids_all))
        return queries

    def batch_payloads(
        self,
        device_id: str,
        topic_type: str,
        payloads: typing.List[str],
        uids: typing.List[str],
    ) -> typing.List[BatchedAzureQueryReturn]:
        """
        Batch the payloads together and ensure that they do not exceed the maximum message size
        Approximates the message size to save CPU.
        """
        payload = f"[{','.join(payloads)}]"  # Assume payload is valid json
        if len(payload) < self.message_size_chr_maximum:
            return [BatchedAzureQueryReturn(topic_type, payload, device_id, uids)]
        else:
            returns = []
            log.debug("Batched message size too great. Splitting message")
            split_num = len(payloads) // 2
            returns.extend(
                self.batch_payloads(
                    device_id, topic_type, payloads[:split_num], uids[:split_num]
                )
            )
            returns.extend(
                self.batch_payloads(
                    device_id, topic_type, payloads[split_num:], uids[split_num:]
                )
            )
            return returns


class DbSizeManager:
    """
    Limits the SQLite database size by limiting the max page count with the page size of 4096 bytes.
    :param max_size: A string representation of the size of the database eg. 10GB, 512MB, 123456B.
    Will round down to the nearest 4096B. If 0, will not limit the size of the database.
    """

    def __init__(
        self, max_size: str = "500MB", clean_up_portion: float = 0.3, **kwargs
    ):
        self.evt = asyncio.Event()
        self.cleaning = False
        self.page_size = 4096
        self.page_count = self.parse_page_count(max_size)
        self.conn = None
        self.clean_up_portion = clean_up_portion

    async def init(self, conn):
        self.conn = conn
        if self.page_count:
            await self.conn.execute(f"PRAGMA page_size={self.page_size};")
            await self.conn.execute(f"PRAGMA max_page_count={self.page_count};")

    def parse_page_count(self, max_size: str) -> int:
        try:
            if max_size.endswith("GB"):
                return int(
                    float(max_size.rstrip("GB")) * 1024 * 1024 * 1024 / self.page_size
                )
            elif max_size.endswith("MB"):
                return int(float(max_size.rstrip("MB")) * 1024 * 1024 / self.page_size)
            elif max_size.endswith("KB"):
                return int(float(max_size.rstrip("KB")) * 1024 / self.page_size)
            elif max_size.endswith("B"):
                return int(float(max_size.rstrip("B")) / self.page_size)
            elif max_size.isnumeric():
                # Assume bytes
                return int(float(max_size) / self.page_size)
            else:
                return 0
        except asyncio.CancelledError:
            raise
        except BaseException as e:
            log.error(repr(e))
            return 0

    async def clean_up(self):
        if self.cleaning:
            await self.evt.wait()
            return
        try:
            if self.evt.is_set():
                self.evt.clear()
            self.cleaning = True
            log.info("Database exceeded, deleting old messages")
            res = await self.conn.execute("SELECT COUNT(*) from mqtt")
            message_cnt = await res.fetchone()
            delete_cnt = int(message_cnt[0] * self.clean_up_portion)
            await self.conn.execute(
                "DELETE from mqtt WHERE id IN (SELECT id from mqtt ORDER BY id LIMIT ?)",
                (delete_cnt,),
            )
            log.info(f"Database clean deleted {delete_cnt} messages")
        finally:
            self.evt.set()
            self.cleaning = False


class DbVersionManager:
    """
    Performs preliminary SQL migrations or deletions to get the db in a state to be used by the disk storage manager
    """

    def __init__(self, **kwargs):
        self.version = 2
        self.path = Path()
        self.migrations = {-1: self.migrate_default}

    async def init(self, path: Path):
        """
        Retrieve the version of the database and perform the migrations
        """
        logging.getLogger("aiosqlite").disabled = True
        self.path = path
        async with aiosqlite.connect(path, isolation_level=None) as conn:
            ver = -1
            try:
                res = await conn.execute(
                    "SELECT version FROM version ORDER BY ID DESC LIMIT 1"
                )
                for (ver,) in await res.fetchall():
                    break
            except aiosqlite.OperationalError:
                pass
        await self.migrate(ver)

    async def migrate(self, cur_version: int):
        if cur_version == self.version:
            return
        elif cur_version in self.migrations:
            await self.migrations[cur_version]()
        else:
            await self.migrations[-1]()

    async def migrate_default(self):
        """
        Remove the database and insert the latest version into the version table. There will be no conflicts with the
        schema as there is nothing implemented due to the erasure of the database.
        :return:
        """
        # If the database used is in memory skip deleting the database as this is not required
        if not self.path.name == ":memory:":
            try:
                self.path.unlink()
            except (PermissionError, FileNotFoundError) as e:
                log.error(repr(e))
            try:
                self.path.with_name(f"{self.path.stem}.db-shm").unlink()
            except (PermissionError, FileNotFoundError) as e:
                log.error(repr(e))
            try:
                self.path.with_name(f"{self.path.stem}.db-wal").unlink()
            except (PermissionError, FileNotFoundError) as e:
                log.error(repr(e))
        async with aiosqlite.connect(self.path, isolation_level=None) as conn:
            await conn.execute(
                "CREATE TABLE IF NOT EXISTS version (id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "version INTEGER"
                ") "
            )
            await conn.execute(
                "INSERT INTO version (version) values (?)", (self.version,)
            )

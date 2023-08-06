import ydb
from .config import ydb_configuration
from .entity import Entity
from .entityMeta import EntityMeta


class Database:
    def __init__(self, *args, echo=False, **kwargs):
        self.echo = echo
        self.config = ydb_configuration
        self.driver = self.create_driver()
        self._database = self.config.database
        self.pool = ydb.SessionPool(self.driver)
        self.entities = {}
        self.schema = None
        self.Entity = type.__new__(EntityMeta, 'Entity', (Entity,), {})
        self.Entity._database_ = self
        self.__item_list = []
        self._path = ''

    def create_driver(self):
        driver_config = ydb.DriverConfig.default_from_endpoint_and_database(
            self.config.endpoint,
            self.config.database
        )
        driver = ydb.Driver(driver_config)
        try:
            driver.wait(timeout=5)
        except Exception:
            raise Exception(driver.discovery_debug_details())
        return driver

    def add_item(self, item):
        self.__item_list.append(item)

    def save_all(self):
        for item in self.__item_list:
            item.save()

    def create_query(self, query, params={}):
        query = f"""PRAGMA TablePathPrefix("{self._database}");
        {query}"""

        def execute_query(session):
            if self.echo:
                print(query)
                print(params)
            prepared_query = session.prepare(query)
            return session.transaction().execute(
                prepared_query,
                parameters=params,
                commit_tx=True,
                settings=ydb.BaseRequestSettings().with_timeout(3).with_operation_timeout(2),
            )

        return execute_query


    def query(self, sql, params={}):
        q = self.pool.retry_operation_sync(self.create_query(sql, params))
        if q:
            return q[0].rows

    def bulk(self, table, column_types, item_list):
        return self.driver.table_client.bulk_upsert(f'{self._database}/{table}', item_list, column_types)

    def create_table(self, table, params, pk):
        session = self.driver.table_client.session().create()
        columns = ydb.TableDescription()
        for param in params:
            columns.with_column(ydb.Column(param[0], ydb.OptionalType(param[1])))
        columns.with_primary_keys(*pk)
        session.create_table(
            self._database + '/' + table,
            columns
        )

    def update_columns(self, table, params, pk):
        path = self._database + '/' + table
        session = self.driver.table_client.session().create()
        result = session.describe_table(path)
        columns = [column.name for column in result.columns]
        new_columns = []
        for param in params:
            if param[0] not in columns:
                new_columns.append(ydb.Column(param[0], ydb.OptionalType(param[1])))
        if new_columns:
            session.alter_table(path, add_columns=new_columns)

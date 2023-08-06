from typing import  Any, Iterable, Union
from airflow.providers.common.sql.hooks.sql import DbApiHook
from airflow.models.connection import Connection
from clickhouse_driver import Client
import contextlib
from typing import *
from itertools import islice
import pandas as pd
        

__all__=["ClickHouseHook"]

class ClickHouseHook(DbApiHook):
    """
    
    ClickHouseHook provide Airflow hook class on Clickhouse instance base on SQL hook class
    @author = amirtaherkhani@outlook.com
    
    """


    conn_name_attr = 'clickhouse_conn_id'
    default_conn_name = 'clickhouse_default'
    database = ''
    conn_type = 'clickhouse'
    hook_name = 'ClickHouse'
    
    
    def _log_query(
            self,
            sql: str,
            parameters: Union[None, dict, list, tuple, Generator],
    ) -> None:
        self.log.info(
            '%s%s', sql,
            f' with {self._log_params(parameters)}' if parameters else '',
        )

    @staticmethod
    def _log_params(
            parameters: Union[dict, list, tuple, Generator],
            limit: int = 10,
    ) -> str:
        if isinstance(parameters, Generator) or len(parameters) <= limit:
            return str(parameters)
        if isinstance(parameters, dict):
            head = dict(islice(parameters.items(), limit))
        else:
            head = parameters[:limit]
        head_str = str(head)
        closing_paren = head_str[-1]
        return f'{head_str[:-1]} … and {len(parameters) - limit} ' \
            f'more parameters{closing_paren}'

    
    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        """Returns custom field behaviour"""
        return {
            "hidden_fields": [],
            "relabeling":    {'schema': 'Database','extra': 'settings'},
        }


    def get_conn(self, conn_name_attr: str = None) -> Client:
        if conn_name_attr:
            self.conn_name_attr = conn_name_attr
        conn: Connection = self.get_connection(
                getattr(self, self.conn_name_attr))
        host: str = conn.host
        port: int = int(conn.port) if conn.port else 9000
        user: str = conn.login
        password: str = conn.password
        database: str = conn.schema
        settings:dict=conn.extra_dejson.copy()
        click_kwargs = {}
        
        if password is None:
            password = ''
        click_kwargs.update(port=port)
        click_kwargs.update(user=user)
        click_kwargs.update(password=password)
        
        if settings:
            click_kwargs.update(settings=settings)
        
        if database:
            click_kwargs.update(database=database)

        result = Client(host or 'localhost', **click_kwargs)
        result.connection.connect()
        return result

    def run(self, sql: Union[str, Iterable[str]], parameters: Union[None, dict, list, tuple, Generator] = None,
            with_column_types: bool = True,types_check: bool = False, **kwargs) -> Any:
        if isinstance(sql, str):
            queries = (sql,)
        
        with _disconnecting(self.get_conn()) as client:
            last_result = None
            for sql in queries:
                self._log_query(sql, parameters)
                last_result = client.execute(
                sql,
                params=parameters,
                with_column_types=with_column_types,
                types_check=types_check,
                **kwargs
                )
        return last_result


    def bulk_dump(self, table, tmp_file):
        pass

    def bulk_load(self, table, tmp_file):
        pass



    def get_records(self, sql: Union[str, Iterable[str]], parameters: Optional[dict] = None,
            with_column_types: bool = True,types_check: bool = False, **kwargs) -> List[Tuple]:
        self._log_query(sql, parameters)
        with _disconnecting(self.get_conn()) as client:
            return client.execute(
                sql,
                params=parameters,
                with_column_types=with_column_types,
                types_check=types_check,
                **kwargs
                )

    def get_first(self, sql: Union[str, Iterable[str]], parameters: Optional[dict] = None ,
            with_column_types: bool = True,types_check: bool = False, **kwargs) -> Optional[Tuple]:
        self._log_query(sql, parameters)
        with _disconnecting(self.get_conn()) as client:
            try:
                return next(client.execute_iter(sql,
                params=parameters,
                with_column_types=with_column_types,
                types_check=types_check,
                **kwargs))
            except StopIteration:
                return None

    def get_pandas_df(self, sql: Union[str, Iterable[str]], parameters: Union[None, dict, list, tuple, Generator] = None,
            external_tables=None, query_id=None,
            settings=None, **kwargs)->pd.DataFrame:
        try:
            from pandas.io import sql as psql
        except ImportError:
            raise Exception(
                "pandas library not installed, run: pip install "
                "'apache-airflow-providers-common-sql[pandas]'."
            )
        with _disconnecting(self.get_conn()) as client:
            result = None
            self._log_query(sql)
            result = client.query_dataframe(
                sql,
                params=parameters,
                external_tables=external_tables,
                query_id=query_id,
                settings=settings,
                **kwargs
                )
        return result
    
    def set_pandas_df(self, sql: Union[str, Iterable[str]],df:pd.DataFrame , external_tables=None, query_id=None,
            settings=None,**kwargs)->None:
        try:
            from pandas.io import sql as psql
        except ImportError:
            raise Exception(
                "pandas library not installed, run: pip install "
                "'apache-airflow-providers-common-sql[pandas]'."
            )
        with _disconnecting(self.get_conn()) as client:
            result = None
            result = client.insert_dataframe(
                sql,
                df,
                external_tables=external_tables,
                query_id=query_id,
                settings=settings,
                **kwargs
                )
        return  result


_InnerT = TypeVar('_InnerT')

@contextlib.contextmanager
def _disconnecting(context: _InnerT) -> ContextManager[_InnerT]:
    """
    Context to automatically disconnect something at the end of a block.
    Similar to ``contextlib.closing`` but calls .disconnect() method on exit.
    Code like this:
    >>> with _disconnecting(<module>.open(<arguments>)) as f:
    >>>     <block>
    is equivalent to this:
    >>> f = <module>.open(<arguments>)
    >>> try:
    >>>     <block>
    >>> finally:
    >>>     f.disconnect()
    """
    try:
        yield context
    finally:
        context.disconnect()
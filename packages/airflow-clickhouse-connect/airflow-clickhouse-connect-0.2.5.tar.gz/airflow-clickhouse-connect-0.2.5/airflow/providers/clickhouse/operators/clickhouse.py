from airflow.models import BaseOperator
from airflow.providers.clickhouse.hooks.clickhouse import ClickHouseHook
from typing import Any, Dict, Generator, Iterable, Optional, Union
from typing import  Any, Iterable, Union

__all__=["ClickhouseOperator"]

class ClickhouseOperator(BaseOperator):
    """

    ClickHouseOperator provide Airflow operator execute query on Clickhouse instance
    @author = amirtaherkhani@outlook.com

    """
    template_fields = ('sql',)
    template_ext = ('.sql',)
    default_conn_name = ClickHouseHook.default_conn_name


    settings={
        "strings_encoding": "utf-8",
        "strings_as_bytes": True,
        'use_numpy': False
    }

    def __init__(self,sql: Union[str, Iterable[str]],
                 clickhouse_conn_id: str = 'clickhouse_default',
                 parameters: Union[None, dict, list, tuple, Generator] = None,
                 database: Optional[str] = None,
                 *args,
                 **kwargs,):
        super().__init__(*args, **kwargs)
        self.parameters=parameters
        self.database= database
        self.sql = sql
        self.clickhouse_conn_id = clickhouse_conn_id
        self.hook = None
        self.types_check=True
        self.do_xcom_push=False
        
        
    def execute(self, context: Dict[str, Any]) -> Any:
        self.log.info('Executing: %s', self.sql)
        client = ClickHouseHook(clickhouse_conn_id=self.clickhouse_conn_id,schema=self.database)
        result=client.run(
            sql=self.sql, parameters=self.parameters, with_column_types=True,types_check=self.types_check)
        if self.do_xcom_push:
            return result 
        else :
            return
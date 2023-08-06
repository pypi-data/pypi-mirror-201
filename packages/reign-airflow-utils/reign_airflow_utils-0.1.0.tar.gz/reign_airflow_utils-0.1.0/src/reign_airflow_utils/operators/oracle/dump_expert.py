from logging import info
from typing import Dict

from airflow.models import BaseOperator
from airflow.models.param import ParamsDict
from airflow.plugins_manager import AirflowPlugin

from  reign_airflow_utils.hooks.oracle_hook import OracleHook


class OracleOperatorDumpExpert(BaseOperator):
    template_fields = ("output_file_path", "parameters")
    template_ext = (".sql",)

    def __init__(
        self, 
        oracle_conn_id: str, 
        sql_path: str, 
        output_file_path: str, 
        parameters: Dict = None, 
        batch_size: int = 10000,
        *args, 
        **kwargs
    ):
        super(OracleOperatorDumpExpert, self).__init__(*args, **kwargs)

        self.oracle_conn_id = oracle_conn_id
        self.sql_path = sql_path
        self.output_file_path = output_file_path
        self.parameters = parameters
        self.params = ParamsDict(parameters)
        self.batch_size = batch_size

    def execute(self, context):
        with open(self.sql_path, "r") as file:
            sql = file.read()

        if not sql:
            raise IOError("Missed query")

        info(f'Dumping Oracle query results to local file {self.output_file_path} using query "{sql}"')

        hook = OracleHook(oracle_conn_id=self.oracle_conn_id)
        hook.export(sql=sql, output_file_path=self.output_file_path, parameters=self.params, batch_size=self.batch_size)


class OracleOperatorDumpExpertPlugin(AirflowPlugin):
    name = "oracle_operator_dump_expert"
    operators = [OracleOperatorDumpExpert]

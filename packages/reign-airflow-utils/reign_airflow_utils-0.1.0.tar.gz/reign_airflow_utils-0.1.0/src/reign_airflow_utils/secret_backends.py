from logging import warn
import os

from airflow.secrets import BaseSecretsBackend


class FileSystemSecretsBackend(BaseSecretsBackend):
    def __init__(
        self,
        connections_path="/opt/airflow/connections",
        variables_path="/opt/airflow/variables",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.connections_path = connections_path
        self.variables_path = variables_path

    def get_conn_uri(self, conn_id: str):
        filepath = os.path.join(self.connections_path, conn_id)
        if not os.path.exists(filepath):
            warn(
                f"{filepath} does not exist. Please check your secrets backend connections_path of the connection id."
            )
            return None
        with open(filepath) as file:
            return file.read()

    def get_variable(self, key: str):
        filepath = os.path.join(self.variables_path, key)
        if not os.path.exists(filepath):
            warn(
                f"{filepath} does not exist. Please check your secrets backend variables_path of the variable key."
            )
            return None
        with open(filepath) as file:
            return file.read()

import csv
from logging import info
from typing import List

from airflow.providers.oracle.hooks.oracle import OracleHook as AirflowOracleHook


class OracleHook(AirflowOracleHook):
    def __init__(self, *args, **kwargs):
        super(OracleHook, self).__init__(*args, **kwargs)

    def export(
        self,
        sql: str,
        output_file_path: str,
        parameters: List[str] = None,
        include_headers: bool = True,
        batch_size: int = 10000,
        **kwargs,
    ) -> str:
        with self.get_conn() as oracle_conn:
            info("Oracle connection acquired")

            cursor = oracle_conn.cursor()
            info("Oracle cursor acquired")

            with open(output_file_path, "w") as csv_file:
                info(f"Output file opened")
                csv_writer = csv.writer(csv_file)

                cursor.execute(sql, parameters, **kwargs)

                if include_headers:
                    csv_writer.writerow([desc[0] for desc in cursor.description])

                processed_row = 0
                rows = cursor.fetchmany(batch_size)
                
                while len(rows) > 0:
                    csv_writer.writerows(rows)
                    processed_row += len(rows)

                    rows = cursor.fetchmany(batch_size)

        info(f"Oracle export finished, total rows extracted: {processed_row}")

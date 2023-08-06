import pandas as pd
import pandas_gbq
from google.oauth2 import service_account
from typing import List



class BigQuery:
    """
    Classe que gerência as tabelas do big query permitindo a leitura e envio de tabelas
    """
    def __init__(self, service_account_file: str, project_name: str):
        credentials = service_account.Credentials.from_service_account_file(service_account_file)
        pandas_gbq.context.credentials = credentials
        self.project = project_name
        pandas_gbq.context.project = self.project

    def read(self, query: str) -> pd.DataFrame:
        """
        Método que faz consulta SQL de uma tabela no Big Query
        Args:
            query: Consulta SQL
        Returns:
            Dataframe com as informações de ty basic do dia pesquisado
        """
        return pd.read_gbq(query=query, project_id=self.project)

    def send(self, df: pd.DataFrame, table_name: str, table_schema: List[dict], how: str = 'append'):
        """
        Função que envia os dados para o bigquery
        Args:
            df: Dataframe que deseja ser enviado para o bigquery
            table_name: Nome da tabela junto com o nome do dicionário da table schema do cons.py
            table_schema: Schema da tabela
            how: Como deseja enviar os dados para o bigquery append, replace ou fail(se existir retorna raise)
        Returns:
        """
        pandas_gbq.to_gbq(df, table_name, project_id=self.project, if_exists=how, table_schema=table_schema)

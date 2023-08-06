import tempfile
import os

import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook


class PostgresLoader:

    def __init__(self, pg_conn_id):
        self.__pg_conn_id = pg_conn_id

    def __clearTable(self, tableName, schema):
        pgHook = PostgresHook(postgres_conn_id=self.__pg_conn_id)
        sql = f'delete from {schema}.{tableName}'
        pgHook.run(sql=sql)

    def copy_data(self, tuples, tableName, schema, columns, clear=False):
        df = pd.DataFrame(data=tuples, columns=columns);

        pgHook = PostgresHook(postgres_conn_id=self.__pg_conn_id)
        if clear == True:
            self.__clearTable(tableName=tableName, schema=schema)

        tmpFile = tempfile.NamedTemporaryFile(suffix='.csv');
        tmpPath = os.path.realpath(tmpFile.name)

        # print(('path: ', tmpPath))
        columnsJoined = ','.join(columns)

        df.to_csv(tmpFile, index=False, header=True)

        sql = f"COPY {schema}.{tableName} ({columnsJoined}) FROM STDIN DELIMITER ',' CSV HEADER"
        conn = pgHook.get_conn();
        cursor = conn.cursor()
        result = cursor.copy_expert(sql, open(tmpPath, "r"))
        # print("result: ", result)
        conn.commit()
        conn.close()

    def import_data(self, rows, colNames, tableName, schema, clear=False):
        pgHook = PostgresHook(postgres_conn_id=self.__pg_conn_id)
        if clear == True:
            self.__clearTable(tableName=tableName, schema=schema)

        # sql = PostgresHook._generate_insert_sql(table=schema + '.' +tableName, values=rows[0], target_fields=colNames, replace=False)
        columnsJoined = ', '.join(colNames)
        placeHolderJoined = ', '.join(list(map(lambda x: '%s', range(len(colNames)))))
        sql = f'insert into {schema}.{tableName}({columnsJoined}) values({placeHolderJoined})'
        for row in rows:
            pgHook.run(sql=sql, parameters=row)
        return 0

    def run_function(self, functionName, schema, parameters=[]):
        pgHook = PostgresHook(postgres_conn_id=self.__pg_conn_id)
        placeHolderJoined = ', '.join(list(map(lambda x: '%s', range(len(parameters)))))
        sql = f'select {schema}.{functionName}({placeHolderJoined})'
        result = pgHook.get_first(sql=sql, parameters=parameters)
        return result

    def get_column_names(self, tableName, schema):
        pgHook = PostgresHook(postgres_conn_id=self.__pg_conn_id)
        sql = f'''
        SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = '{schema}'
            AND table_name   = '{tableName}'
            order by ordinal_position;
        '''
        df = pgHook.get_pandas_df(sql=sql)
        columnNames = df['column_name'].tolist()
        return columnNames
    
     def load_to_tuples(self,tableName,colNames,schema):
        """
        Reads data from a Postgres table and returns it as a list of tuples.

        :param table_name: The name of the table to read from.
        :param col_names: A list of strings representing the column names to read.

        :return: A list of tuples representing the rows in the table.
        """
        pgDbHook = PostgresHook(self.__pg_conn_id)
        columns=",".join(colNames)
        df = pgDbHook.get_pandas_df(f"select {columns} from {schema}.{tableName}")
        # js = df.to_json(orient='records')
        return list(df.itertuples(index=False))

import pandas as pd


def redshift_to_df(dbconnection, sql_query, query_params=None):
    cursor = dbconnection.cursor()
    cursor.execute(sql_query, query_params)
    columns_list = [desc[0].decode("utf-8") for desc in cursor.description]
    cursor.close()
    data = pd.DataFrame(cursor.fetchall(), columns=columns_list)
    return data

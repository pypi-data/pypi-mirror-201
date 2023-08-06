import sys, uuid, csv, random, string
import pandas as pd
import numpy as np
import math
from ..s3utils.file_read import s3csvfile_todf
from ..s3utils.file_upload import df_tos3csvfile
from ..s3utils.file_delete import df_deletefile
from ..connections.dwh_awsservicer import initialize_dwhservicer_credentials
from .redshift_to_df import redshift_to_df

SERVICER_CREDENTIALS = initialize_dwhservicer_credentials()

def dftmp_file_tos3(df, tmp_file_path):
    df_tos3csvfile(df, destination=tmp_file_path)

def s3tmp_file_todf(tmp_file_path):
    get_csv_structure = s3csvfile_todf(filetoread=tmp_file_path)
    return get_csv_structure

def delete_s3tmp_file(tmp_file_path):
    tmp_file_path["file-name"] = str(tmp_file_path["file-name"]) + ".csv"
    df_deletefile(tmp_file_path)

def get_df_colnames(df):
    return df.columns.tolist()

def copy_s3to_table(dbconnection, destination_table, tmp_uuid, sep):
    cursor = dbconnection.cursor()
    try:
        cursor.execute("COPY " + destination_table + " FROM 's3://qualifyze-temporals/df-batch-uploads/" + str(tmp_uuid) + ".csv' CREDENTIALS 'aws_access_key_id="+SERVICER_CREDENTIALS['aws_access_key_id']+";aws_secret_access_key="+SERVICER_CREDENTIALS['aws_secret_access_key']+"' DELIMITER '" + sep + "' IGNOREHEADER as 1 ACCEPTINVCHARS EMPTYASNULL CSV;")
    except Exception as err:
        print(err)
    cursor.close()

def create_tmp_table(dbconnection, tmp_uuid, column_names):
    columns_str = ", ".join(["{} varchar(max)".format(col) for col in column_names])
    tmp_staging_table_statement = f"CREATE TABLE dev.tmp_{str(tmp_uuid).replace('-','')} ({columns_str});"

    cursor = dbconnection.cursor()
    cursor.execute(tmp_staging_table_statement)
    cursor.close()

def delete_tmp_table(dbconnection, tmp_uuid):
    cursor = dbconnection.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS dev.tmp_{str(tmp_uuid).replace('-','')};")
    cursor.close()

def get_operable_elements(df_existing, df_insert, unique_update_key, op_type):
    if op_type == 'insert':
        unique_ids = set(df_insert[unique_update_key].astype(str)) - set(df_existing[unique_update_key].astype(str))
    elif op_type == 'update':
        unique_ids = set(df_insert[unique_update_key].astype(str)) & set(df_existing[unique_update_key].astype(str))
    else:
        return None

    df_to_operate = df_insert[df_insert[unique_update_key].isin(unique_ids)]
    return df_to_operate

def delete_in_chunks(elements_to_update, unique_update_key, destination, dbconnection, chunk_size=200):
    # the number of chunks we will need
    num_chunks = math.ceil(len(elements_to_update) / chunk_size)
    # create a list to hold the chunks of elements
    chunks = [elements_to_update[i:i + chunk_size] for i in range(0, len(elements_to_update), chunk_size)]
    cursor = dbconnection.cursor()
    for i in range(num_chunks):
        elements_to_update_statementquery = f"({', '.join(str(el) for el in chunks[i])})"
        cursor.execute("DELETE FROM " + str(destination) + " WHERE " + str(unique_update_key) + " in " + str(
            elements_to_update_statementquery) + "")
    cursor.close()

def df_to_redshift(df, dbconnection, method, destination, unique_update_key, dest_form_cols, delimiter=",", kwargs={'bucket-name': 'qualifyze-temporals', 'use-subfolder': True, 'subfolder-full-path': 'df-batch-uploads'}):

    TMP_FILES_UUID = uuid.uuid1()
    BUCKET_NAME = kwargs['bucket-name']
    USE_SUBFOLDER = kwargs['use-subfolder']
    SUBFOLDER_PATH = kwargs['subfolder-full-path']
    TMP_FILE_PATH = {'bucket-name': BUCKET_NAME, 'use-subfolder': USE_SUBFOLDER, 'subfolder-full-path': SUBFOLDER_PATH,
                     'file-name': str(TMP_FILES_UUID)}

    if method == 'insert':
        df = df.replace('None', None)
        df = df.astype(dest_form_cols)
        dftmp_file_tos3(df, TMP_FILE_PATH)
        copy_s3to_table(dbconnection, 'dev.tmp_' + str(TMP_FILES_UUID).replace("-", "") + '', TMP_FILES_UUID, delimiter)
        #delete_s3tmp_file(TMP_FILES_UUID)

    elif method == 'upsert':
        dftmp_file_tos3(df, TMP_FILE_PATH)

        get_csv_structure = s3tmp_file_todf(TMP_FILE_PATH)
        column_names = get_df_colnames(get_csv_structure)
        create_tmp_table(dbconnection, TMP_FILES_UUID, column_names)
        copy_s3to_table(dbconnection, 'dev.tmp_' + str(TMP_FILES_UUID).replace("-", "") + '', TMP_FILES_UUID, delimiter)
        print('TMP Table has been created')

        #cursor = dbconnection.cursor()
        #cursor.execute("SELECT * FROM " + destination + "")
        #result: tuple = cursor.fetchall()
        #cursor.close()
        #df_existingdata = pd.DataFrame(result, columns=column_names)
        df_existingdata = redshift_to_df(dbconnection, "SELECT * FROM " + destination + "")
        print(df_existingdata)

        #cursor = dbconnection.cursor()
        #cursor.execute("SELECT * FROM dev.tmp_" + str(TMP_FILES_UUID).replace("-", "") + "")
        #result: tuple = cursor.fetchall()
        #cursor.close()
        #df_toupload = pd.DataFrame(result, columns=column_names)
        df_toupload = redshift_to_df(dbconnection, "SELECT * FROM dev.tmp_" + str(TMP_FILES_UUID).replace("-", "") + "")
        print(df_toupload)

        df_records_to_insert = get_operable_elements(df_existingdata, df_toupload, unique_update_key, 'insert')
        df_records_to_insert = df_records_to_insert.replace('None', None)
        df_records_to_insert = df_records_to_insert.astype(dest_form_cols)
        tmp_file_path_insertfile = TMP_FILE_PATH.copy()
        tmp_file_path_insertfile["file-name"] = str(tmp_file_path_insertfile["file-name"]) + "_i"
        dftmp_file_tos3(df_records_to_insert, tmp_file_path_insertfile)
        copy_s3to_table(dbconnection, destination, str(TMP_FILES_UUID) + "_i", delimiter)
        print(df_records_to_insert)

        df_records_to_update = get_operable_elements(df_existingdata, df_toupload, unique_update_key, 'update')
        df_records_to_update = df_records_to_update.replace('None', None)
        df_records_to_update = df_records_to_update.astype(dest_form_cols)
        tmp_file_path_updatefile = TMP_FILE_PATH.copy()
        tmp_file_path_updatefile["file-name"] = str(tmp_file_path_updatefile["file-name"]) + "_u"
        dftmp_file_tos3(df_records_to_update, tmp_file_path_updatefile)
        print(df_records_to_update)

        elements_to_update = df_records_to_update['' + unique_update_key + ''].tolist()
        elements_to_update = elements_to_update or [99999999999]
        delete_in_chunks(elements_to_update, unique_update_key, destination, dbconnection)
        #elements_to_update_statementquery = f"({', '.join(str(el) for el in elements_to_update)})"
        #print(elements_to_update_statementquery)

        #cursor = dbconnection.cursor()
        #cursor.execute("DELETE FROM " + str(destination) + " WHERE " + str(unique_update_key) + " in " + str(
        #    elements_to_update_statementquery) + "")
        #cursor.close()

        copy_s3to_table(dbconnection, destination, str(TMP_FILES_UUID) + "_u", delimiter)

        # Cleaning S3 Temp Files
        delete_tmp_table(dbconnection, TMP_FILES_UUID)
        delete_s3tmp_file(tmp_file_path_insertfile)
        delete_s3tmp_file(tmp_file_path_updatefile)


    else:
        print(f'The selected method [ {method} ] does not exist - Available methods: insert, upsert')
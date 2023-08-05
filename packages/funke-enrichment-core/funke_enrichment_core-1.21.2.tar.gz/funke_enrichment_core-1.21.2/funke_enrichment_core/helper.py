# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 12:35:11 2021

@author: Friedrich.Schmidt
"""

import os
import logging
import json
import pickle
import pandas as pd
from datetime import datetime
from google.cloud import bigquery
from google.api_core import exceptions as gc_api_exceptions
from google.cloud import secretmanager
from google.cloud import pubsub_v1
from firebase_admin import firestore, initialize_app, credentials


def err(msg):
    """
    Prints a specific error message to the console

    msg: Message to print to console
    return: Always returns None
    """
    err_msg = 'Error: {}'.format(msg)
    logging.error(err_msg)
    return None

def warning(msg):
    """
    Prints a specific error message to the console

    msg: Message to print to console
    return: Always returns None
    """
    err_msg = 'Warning: {}'.format(msg)
    logging.warning(err_msg)
    return None


def make_dict_json_serializable(json_dict, date_format=None):
    """
    Make a given dict json serializable

    json_dict: Dict to make json serializable
    date_format: How to format datetime objects. Default is None
    return: Returns a json serializable dict
    """
    for key, value in json_dict.items():
        if isinstance(value, datetime):
            if date_format:
                json_dict[key] = value.strftime(date_format)
            else:
                json_dict[key] = str(value)
        elif isinstance(value, dict):
            json_dict[key] = make_dict_json_serializable(value)
        else:
            json_dict[key] = value

    return json_dict


def get_bq_table(table_id, schema=None, truncate=None):
    """
    Get a table object for a given table_id.
    If the table does not exist, it will be created in the case that a schema has been given.

    table_id: Pandas data frame to save to BigQuery
    schema: Schema the table should have. Default is None
    truncate: Whether to truncate the table or not. Default is None
    return: Returns a table object
    """
    bq_client = bigquery.Client()
    if schema:
        planned_table = bigquery.Table(table_id, schema=schema)
    else:
        planned_table = None

    # if truncate:
    #     "TRUNCATE TABLE `{}`".format(table_id)

    #Get table object or create a new table if a planned table exists
    try:
        table = bq_client.get_table(table_id)
    except gc_api_exceptions.NotFound:
        if planned_table:
            try:
                table = bq_client.create_table(planned_table)
            except gc_api_exceptions.Conflict:
                table = bq_client.get_table(table_id)
        else:
            raise SystemError('It seems table "{}" does not exists.'.format(table_id),
                              'If you want to create it automatically, consider to pass a schema!')
    #Check if the current table object matches the planned table object, if it exists
    if planned_table:
        if table.schema == planned_table.schema:
            return table
        else:
            raise AttributeError('It seems the table: "{}" does not match the given schema!'.format(table_id))
    else:
        return table


def save_df_to_bq(input_df, bq_table, job_conf):
    """
    Save the given Pandas data frame to the given BigQuery table

    input_df: Pandas data frame to save to BigQuery
    bq_table: Path to the BigQuery table
    job_conf: Job config for the BiqQuery client
    return: Returns True and None in case of an error
    """
    if isinstance(input_df, pd.DataFrame):
        if isinstance(bq_table, str):
            if isinstance(job_conf, bigquery.LoadJobConfig):
                if job_conf.allow_jagged_rows:
                    for schema_field in job_conf.schema:
                        if not schema_field.name in input_df.columns:
                            input_df[schema_field.name] = None
                bq_client = bigquery.Client()
                future = bq_client.load_table_from_dataframe(input_df, bq_table, job_config=job_conf)
                return future
            else:
                raise ValueError('job_conf needs to be a bigquery.LoadJobConfig object!')
        else:
            raise ValueError('The given path under bq_table needs to be a string!')
    else:
        raise ValueError('Input data frame needs to be a Pandas DataFrame object!')


def save_dict_to_bq(input_dict, bq_table, job_conf):
    """
    Save the given dictionary to the given BigQuery table

    input_dict: Dictionary to save to BigQuery
    bq_table: Path to the BigQuery table
    job_conf: Job config for the BiqQuery client
    return: Returns True and None in case of an error
    """
    if isinstance(input_dict, dict):
        df = pd.DataFrame.from_dict(input_dict, orient='index')
        if set(df.columns) == set(input_dict.keys()):
            return save_df_to_bq(df, bq_table, job_conf)
        else:
            df = df.T
            if set(df.columns) == set(input_dict.keys()):
                return save_df_to_bq(df, bq_table, job_conf)
            else:
                raise ValueError('Failed to bring the given dictionary into a suitable Pandas data frame!\nKeep in mind that the keys of your dictionary will become the columns of the data frame.')
    else:
        raise ValueError('The given variable for input_dict has to be a dictionary!')


def stream_insert_dict_as_row_to_bq(row_as_dict, bq_table, ignore_unknown_values, timeout):
    """
    Save the given dictionary to the given BigQuery table

    row_as_dict: Dictionary to save to BigQuery
    bq_table: Path to the BigQuery table
    ignore_unknown_values: Cherry-pick all needed fields from the input data
    timeout: Time until the client retries to insert the row
    return: Returns True and None in case of an error
    """
    if not isinstance(row_as_dict, dict):
        raise ValueError('The given variable for "row_as_dict" has to be a dictionary!')
    if not (isinstance(bq_table, str) or isinstance(bq_table, bigquery.Table)):
        raise ValueError('The given variable for "bq_table has" to be a string!')
    if not isinstance(ignore_unknown_values, bool):
        raise ValueError('The given variable for "ignore_unknown_values" has to be a boolean!')
    if not (isinstance(timeout, int) and timeout > 0):
        raise ValueError('The given variable for "timeout" has to be a postive integer!')
    bq_client = bigquery.Client()
    return bq_client.insert_rows_json(table=bq_table,
                                      json_rows=[row_as_dict],
                                      ignore_unknown_values=ignore_unknown_values,
                                      timeout=timeout)

def read_from_bigquery(query):
    """
    Give back BigQuery results

    query: Query to return the results for
    return: Returns the query results and None in case of an error.
    """
    if not (query and isinstance(query, str)):
        raise ValueError('Query needs to be a non empty string!')
    bq_client = bigquery.Client()
    bq_answer = bq_client.query(query)
    return bq_answer
    #return bq_answer.to_dataframe()


def read_from_bigquery_to_dict(query, index_column=None):
    """
    Give back BigQuery results as a dict

    query: Query to return the results for
    index_column: The column to use as the keys for the output dictionary
    return: Returns the query results and None in case of an error.
    """
    query_result = read_from_bigquery(query)
    if query_result:
        return {row.get(index_column, idx):
                    {key: value for key, value in row.items()
                     if not key == index_column
                     }
                for idx, row in enumerate(query_result)
                }
    else:
        return query_result


def load_pickle_data(path):
    """
    Loads a pickle object

    path: Path to the pickle object
    return: Returns loaded pickle object and None in case of an error.
    """
    if isinstance(path, str):
        if os.path.isfile(path):
            with open(path,'rb') as handle:
                data = pickle.load(handle)
            handle.close()
            return data
        else:
            raise OSError('File "{}" does not exist!'.format(path))
    else:
        raise ValueError('Path needs to be a string!')


def load_text_data(path):
    """
    Loads utf-8 encoded text data into a list, split by line.

    path: Path to the text data object
    return: Returns the text data split by lines in a list and None in case of an error.
    """
    if isinstance(path, str):
        if os.path.isfile(path):
            with open(path,'r',encoding='utf-8') as handle:
                word_list = handle.read().splitlines()
            handle.close()
            return word_list
        else:
            raise OSError('File "{}" does not exist!'.format(path))
    else:
        raise ValueError('Path needs to be a string!')


def access_secret_version(secret_version_name):
    """
    Access the content of a specific secret version.

    secret_version_name: Path of the secret with version
    return: Returns the content of the given secret version and None in case of an error.
    """
    if not isinstance(secret_version_name, str):
        raise ValueError('The secret path needs to be a string!')
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=secret_version_name)
    secret_data = json.loads(response.payload.data.decode('UTF-8'))

    return secret_data


def get_firestore_client(cred_dict=None, secret_version_name=None):
    """
    Get an initialized firestore client. Credentials can also be loaded from a secret

    cred_dict: Dictionary containing the credentials for authentification. Default is None.
    secret_path: Path of the secret containing the credentials without: "/versions/{version}". Default is None.
    return: Returns the initialized firestore client and None in case of an error.
    """
    if cred_dict and isinstance(cred_dict, dict):
        creds = cred_dict
    elif secret_version_name and isinstance(secret_version_name, str):
        creds = access_secret_version(secret_version_name)
        if not creds:
            return creds
    else:
        raise ValueError('Either the credentials dictionary as a dict or the path to the secret containing the credentials dictionary as a string must be given and contain information!')

    cred = credentials.Certificate(creds)
    try:
        initialize_app(cred)
    except ValueError:
        pass

    return firestore.client()


def publish_data_to_pubsub_topic(topic_path, data, filter_attrs={}, encoding='utf-8'):
    """
    Publish given data to a Pub/Sub topic as a bytes converted json string.

    topic_path: Full path of the Pub/Sub topic.
    data: Json serialziable data to publish.
    filter_attrs: List of filter keys to add to the message with the value "True"
    encoding: How to encode the json string. Default is utf-8.
    return: Returns the Future object and None in case of an error.
    """
    if not (topic_path and isinstance(topic_path, str)):
        raise ValueError('topic_path needs to be a non empty string!')
    if data is None:
        raise ValueError('data needs to be given!')
    if not (isinstance(filter_attrs, dict) and all([isinstance(value, str) for value in filter_attrs.values()])):
        raise ValueError('filter_attrs must be a dict with a string under each key!')

    prepared_data = json.dumps(data).encode(encoding)
    publisher = pubsub_v1.PublisherClient()
    future = publisher.publish(topic_path, data=prepared_data, **filter_attrs)

    return future

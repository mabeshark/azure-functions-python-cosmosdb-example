import azure.functions as func
from azure.cosmos import CosmosClient
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import logging
import datetime
import os
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    url = os.environ['COSMOS_URL']
    key = os.environ['COSMOS_KEY']

    # Create connection to cosmos
    client = CosmosClient(url, credential=key)
    db = client.get_database_client('database1')
    container = db.get_container_client('container1')

    # Query to select all records or to select only a particular patient's records
    sql_query = 'SELECT * FROM container1'
    patient_id = req.params.get('patient_id')
    if patient_id:
        sql_query += f' WHERE container1.patient_id = "{patient_id}"'

    # enable_cross_partition_query should be set to True as the container is partitioned
    items = list(container.query_items(
        query=sql_query,       
        enable_cross_partition_query=True
    ))

    return func.HttpResponse(
        json.dumps(items),
        status_code=200,
        mimetype="application/json",
        )
    
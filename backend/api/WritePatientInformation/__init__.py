import logging
import uuid
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    my_uuid = str(uuid.uuid4())

    return func.HttpResponse(
            f"This HTTP triggered function executed successfully. uuid={my_uuid} name={name}",
            status_code=200
    )

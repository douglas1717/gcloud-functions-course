from flask import abort, jsonify
from google.cloud import bigquery
from google.oauth2 import service_account
import json
import pdb


def big_query_utils(request):

    verifications = verification_authorizations(request)

    if not verifications[0]:
        abort(verifications[1])

    if request.method == "OPTIONS":
        headers = {'Access-Control-Allow-Origin':'*',
         'Access-Control-Allow-Methods': 'POST',
         'Access-Control-Allow-Headers': 'Content-Type',
         'Access-Control-Max-Age': '3600'}
        return '', 204, headers

    headers = {'Access-Control-Allow-Origin':'*'}

    client = get_credentials_big_query()
    #job_config = bigquery.QueryJobConfig(use_legacy_sql=True)

    result = ''

    if request.method == "GET":
        result = get_amount(client)

    if request.method == "POST":
        result = insert_data(client,request)


    return result


def verification_authorizations(request):
    methods = ('GET', 'POST')

    if all(m in request.method for m in methods):
        return False, 404

    bearer_token = request.headers.get("Authorization").split()[1]
    security_acess_token = "757f7645c4e09d2824ed7f8bc2d9e5e1"
    if bearer_token != security_acess_token:
        return False, 401
    else:
        return True, 200


def get_credentials_big_query():
    credentials = service_account.Credentials.from_service_account_file('../gcloudKey/paratyai-959c7988a663.json')
    project_id = 'paratyai'
    client = bigquery.Client(credentials=credentials, project=project_id)
    return client

def get_amount(client):
    query_job = client.query("""SELECT * FROM `general.contratos_imob2` LIMIT 1000""")  # , job_config=job_config)

    results = query_job.result()  # Wait for the job to complete.

    count = 0
    for row in results:
        # print("{}: \t{}".format(row.consultor, row.valor))
        count += 1
    return str(count), 200

def insert_data(client,request):

    data_object = json.loads(request.data)
    queries = parse_insert_data(data_object)
    #query = """insert into `{}` values ({})""".format(row.consultor, row.valor)
    #query_job = client.query("""insert into `general.contratos_imob2` (id_contrato,sl,time,consultor,valor) values (999999,99999,'imob','teste.teste',1000.0)""")  # , job_config=job_config)
    count = 0
    try:
        for query in queries:
            #pdb.set_trace()
            query_job = client.query(query)
            results = query_job.result()
            query = None
            count += 1
    except:
        return 'Falha de pré-condição', 412
    return 'Sucess, {} registry(ies) inserted'.format(count), 200


def parse_insert_data(data):
    arr_fields = []
    arr_values = []
    arr_queries = []

    for fields in data['fields']:
        #pdb.set_trace()
        for field in fields['field']:
            arr_fields.append(field['key'])
            if field['type'] == "string":
                arr_values.append("'{}'".format(field['value']))
            else:
                arr_values.append(field['value'])

        field_data = ','.join(arr_fields)
        value_data = ','.join(arr_values)
        query = """insert into `{}` ({}) values ({})""".format(data['table'], field_data, value_data)
        #pdb.set_trace()
        arr_queries.append(query)
        arr_fields.clear()
        arr_values.clear()
        field_data = None
        value_data = None
        query = None

    return arr_queries



import os
import boto3
import requests
from requests_aws4auth import AWS4Auth

region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://search-codster-waf-dashboard-fxjhlkvko4n5loalxfaekzacvu.us-east-1.es.amazonaws.com'
index = 'waf_logs'  # El nombre de tu índice
url = host + '/_index_template/' + index 

headers = { "Content-Type": "application/json" }

s3 = boto3.client('s3')

def lambda_handler(event, context):
    files_to_download = ['awswaf-es-index-template.json']

    try:
        for file in files_to_download:
            url_to_download = f'https://raw.githubusercontent.com/codster-team/aws-waf-files/main/{file}'
            response = requests.get(url_to_download)
            document = response.content
            # Ahora subir el archivo a OpenSearch
            r = requests.post(url, auth=awsauth, data=document, headers=headers)
            print(r.text)
    except Exception as err:
        print(err)


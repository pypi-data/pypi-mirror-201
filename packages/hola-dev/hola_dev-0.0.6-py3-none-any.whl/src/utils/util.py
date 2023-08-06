import os
import json
import boto3

def set_secret_manager_env():
  client = boto3.client(
    service_name='secretsmanager',
    region_name='ap-northeast-2'
  )

  secret_keys = client.get_secret_value(SecretId='hola-dev/env')
  for key, value in json.loads(secret_keys['SecretString']).items():
    os.environ[key] = value
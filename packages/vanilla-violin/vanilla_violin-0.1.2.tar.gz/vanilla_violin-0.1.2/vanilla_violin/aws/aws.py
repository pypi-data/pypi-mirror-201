from botocore.client import Config
import boto3
import json

class Aws:

  def __init__(self, service, access_key, secret_key, region_name="eu-west-1"):

    self.config = Config(
      read_timeout=900,
      connect_timeout=30,
      retries={"max_attempts": 0},
      tcp_keepalive=True
    )

    self.service = service
    self.access_key = access_key
    self.secret_key = secret_key
    self.region_name = region_name
    self.client = boto3.client(
      self.service, 
      aws_access_key_id=self.access_key, 
      aws_secret_access_key=self.secret_key,
      region_name = self.region_name,
      config = self.config
    )
    
  def get_user(self, user_name):
    try:
      response = self.client.get_user(UserName=user_name)
    except:
      print(f"Couldn't get user {user_name}.")
      raise

    return response

  def create_lambda(self, function_name, iam_role_arn, image_uri, subnet_ids, security_group_ids, description='AWS Lambda'):
    try:
      response = self.client.create_function(
        FunctionName=function_name,
        Description=description,
        Role=iam_role_arn,
        Code={
          'ImageUri': image_uri,
        },
        PackageType='Image',
        Timeout=900,
        MemorySize=1024,
        VpcConfig={
          'SubnetIds': subnet_ids,
          'SecurityGroupIds': security_group_ids
        },
        Publish=True
      )
      function_arn = response['FunctionArn']
      waiter = self.client.get_waiter('function_active_v2')
      waiter.wait(FunctionName=function_name)
      print(f"Created function {function_name} with ARN: {response['FunctionArn']}.")
    except:
      print(f"Couldn't create function {function_name}.")
      raise
    else:
      return function_arn

  def get_lambda(self, function_name):
    response = None
    try:
      response = self.client.get_function(FunctionName=function_name)
    except Exception as err:
      if err.response['Error']['Code'] == 'ResourceNotFoundException':
        print(f"Function {function_name} does not exist.")
      else:
        print(f"Couldn't get function {function_name}. Reason: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
        raise err
    return response

  def delete_lambda(self, function_name):
    response = None
    try:
      response = self.client.delete_function(FunctionName=function_name)
    except Exception as err:
      if err.response['Error']['Code'] == 'ResourceNotFoundException':
        print(f"Function {function_name} does not exist.")
      else:
        print(f"Couldn't get function {function_name}. Reason: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
        raise err
    return response

  def update_lambda_configuration(self, function_name, timeout=3, memory_size=128, subnet_ids=[], security_group_ids=[]):
    try:
      response = self.client.update_function_configuration(
        FunctionName=function_name,
        Timeout=timeout,
        MemorySize=memory_size,
        VpcConfig={
          'SubnetIds': subnet_ids,
          'SecurityGroupIds': security_group_ids
        }
      )
    except Exception as err:
      print(f"Couldn't get function {function_name}. Reason: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
      raise err
    else:
      return response

  def invoke_lambda(self, function_name, function_params, get_log=False):
    try:
      response = self.client.invoke(
        FunctionName=function_name,
        Payload=json.dumps(function_params),
        InvocationType="RequestResponse",
        LogType='Tail' if get_log else 'None'
      )
      print(f"Invoked function {function_name}")
    except Exception as err:
      print(f"Couldn't invoke function {function_name}")
      raise err
    return response
  
  def create_record(self, domain, record_name, record_value, record_type, hosted_zone_id):

    if record_type == 'TXT':
      record_value = f'\"{record_value}\"'

    self.client.change_resource_record_sets(
      ChangeBatch={
        'Changes': [
          {
            'Action': 'UPSERT',
            'ResourceRecordSet': {
              'Name': f'{record_name}.{domain}',
              'ResourceRecords': [
                {
                  'Value': f'{record_value}',
                },
              ],
              'TTL': 300,
              'Type': f'{record_type}',
            },
          },
        ],
      },
      HostedZoneId=hosted_zone_id,
    )

  def get_hosted_zone_id(self, name):
    response = self.client.list_hosted_zones_by_name(DNSName=name)
    if not response:
      return 'N/A'
    elif response['HostedZones'][0]['Name'] == f'{name}.':
      return response['HostedZones'][0]['Id']
    return 'N/A'
import config
import boto3

print('Python ok')
print(boto3.client("sts").get_caller_identity())
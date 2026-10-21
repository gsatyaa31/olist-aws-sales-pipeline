from config import BUCKET,get_s3

s3=get_s3()
response=s3.list_objects_v2(Bucket=BUCKET)

for obj in response.get('Contents', []):
    print(obj['Key'], obj['Size'], "bytes")
    
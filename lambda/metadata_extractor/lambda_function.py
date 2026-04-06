import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # SNS → S3 event
    message = json.loads(event['Records'][0]['Sns']['Message'])
    record = message['Records'][0]
    
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']
    size = record['s3']['object']['size']
    
    upload_time = datetime.utcnow().isoformat() + "Z"
    
    print(f"[METADATA] File: {key}")
    print(f"[METADATA] Bucket: {bucket}")
    print(f"[METADATA] Size: {size} bytes")
    print(f"[METADATA] Upload Time: {upload_time}")
    
    metadata = {
        "file": key,
        "bucket": bucket,
        "size": size,
        "upload_time": upload_time
    }
    
    # ✅ FIXED filename (THIS was your bug)
    filename = key.split('/')[-1].split('.')[0]
    output_key = f"processed/metadata/{filename}.json"
    
    s3.put_object(
        Bucket=bucket,
        Key=output_key,
        Body=json.dumps(metadata),
        ContentType='application/json'
    )
    
    print(f"[METADATA] Uploaded to: {output_key}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Metadata processed')
    }

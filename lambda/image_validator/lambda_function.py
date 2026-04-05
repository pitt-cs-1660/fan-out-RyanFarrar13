import json
import boto3
import os

s3 = boto3.client('s3')

VALID_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']

def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    record = message['Records'][0]
    
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']
    
    # get file extension
    _, ext = os.path.splitext(key.lower())
    
    if ext in VALID_EXTENSIONS:
        print(f"[VALID] {key} is a valid image file")
        
        new_key = key.replace("uploads/", "processed/valid/")
        
        s3.copy_object(
            Bucket=bucket,
            CopySource={'Bucket': bucket, 'Key': key},
            Key=new_key
        )
        
    else:
        print(f"[INVALID] {key} is not a valid image type")
        raise Exception("Invalid file type")  # triggers DLQ
    
    return {
        'statusCode': 200,
        'body': json.dumps('Validation complete')
    }

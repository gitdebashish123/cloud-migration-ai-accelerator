import boto3
from botocore.exceptions import BotoCoreError, ClientError
# from dotenv import load_dotenv

# load_dotenv()

def check_s3_connectivity():
    s3 = boto3.client('s3')
    try:
        s3.list_buckets()
        print("✅ Successfully connected to S3!")
    except ClientError as e:
        print(f"❌ AWS Client Error: {e}")
    except BotoCoreError as e:
        print(f"❌ AWS Core Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    check_s3_connectivity()

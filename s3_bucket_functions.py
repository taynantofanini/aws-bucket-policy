import boto3
import json

clients3 = boto3.client("s3")

def list_buckets_names():
    response = clients3.list_buckets()["Buckets"]
    names = []
    for bucket in response:
        names.append(bucket["Name"])
    return names

def get_bucket_policy(listed_buckets):
    for name in listed_buckets:
        statement = '{"Sid": "Statement1","Effect": "Deny","Principal": "*","Action": "s3:*","Resource": ["arn:aws:s3:::' + name + '",' + '"arn:aws:s3:::' + name + '/*"],"Condition": {"Bool": {"aws:SecureTransport": "false"} } }'
        statement = json.loads(statement)
        new_policy = json.loads(clients3.get_bucket_policy(Bucket=name)["Policy"])
        if statement not in new_policy["Statement"]:
            att_buckets3_policy(new_policy, statement, name)

def att_buckets3_policy(new_policy, statement, name):
    new_policy["Statement"].append(statement)
    new_policy = json.dumps(new_policy)
    response = clients3.put_bucket_policy(Bucket=name, Policy=new_policy)
    
def put_buckets3_policy(listed_buckets):
    for name in listed_buckets:
        policy = '{"Version": "2012-10-17","Statement": [{"Sid": "Statement1","Effect": "Deny","Principal": "*","Action": "s3:*","Resource": ["arn:aws:s3:::' + name + '",' + '"arn:aws:s3:::' + name + '/*"],"Condition": {"Bool": {"aws:SecureTransport": "false"} } }]}'
        response = clients3.put_bucket_policy(Bucket=name, Policy=policy)

def get_buckets3_logging(listed_buckets):
    bucket_log_name = "lab-taynan-logs"
    for bucket in listed_buckets:
        bucket_logging = clients3.get_bucket_logging(Bucket=bucket)
        if "LoggingEnabled" not in bucket_logging.keys():
            put_buckets3_logging(bucket, bucket_log_name)
            print("Logging habilitado para o bucket '{}' ".format(bucket))
        else:
            if bucket_logging["LoggingEnabled"]["TargetBucket"] != bucket_log_name:
                put_buckets3_logging(bucket, bucket_log_name)
                print("Logging atualizado para o bucket '{}' ".format(bucket))
    print("Todos os buckets foram atualizados e estão com o 'Server Access Logging' ativos e atualizados")

def put_buckets3_logging(bucket, bucket_log_name):
    bucket_logging_put = clients3.put_bucket_logging(
                Bucket=bucket, 
                BucketLoggingStatus={
                    "LoggingEnabled": {
                        "TargetBucket": bucket_log_name,
                        "TargetPrefix": bucket
                    }
                })


if __name__ == "__main__":
    #listed_buckets = list_buckets_names()
    listed_buckets = ["taynan-lab"] ## list definition for manual test
    try:
        get_bucket_policy(listed_buckets)
    except:
        put_buckets3_policy(listed_buckets)
    get_buckets3_logging(listed_buckets)
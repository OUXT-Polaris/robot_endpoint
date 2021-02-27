import boto3
import argparse
import yaml

class PackageSynchronizer:
    def __init__(self, config_path):
        s3 = boto3.client('s3')
        config = {}
        with open(config_path, 'r') as yml:
            config = yaml.safe_load(yml)
        response = s3.list_objects_v2(Bucket=config['bucket_name'])
        for s3_object in response['Contents']:
            print(s3_object)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='synchronize debian package in S3')
    parser.add_argument('config_path', help='path to the config yaml path')
    args = parser.parse_args()
    sync = PackageSynchronizer(args.config_path)
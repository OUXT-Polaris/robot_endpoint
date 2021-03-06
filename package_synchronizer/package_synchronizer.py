import boto3
import argparse
import yaml
import os
import hashlib
import logging
from logger.logger_extension import LogRecordExtension, Extension
import datetime

class PackageSynchronizer:
    def __init__(self, config_path):
        self.s3 = boto3.client('s3')
        with open(config_path, 'r') as yml:
            config = yaml.safe_load(yml)
            self.local_package_directory = config['local_package_directory']
            self.bucket_name = config['bucket_name']
        if not os.path.exists(self.local_package_directory):
            os.makedirs(self.local_package_directory)
        self.response = self.s3.list_objects_v2(Bucket=self.bucket_name)

    def getHash(self, filepath):
        md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(2048 * md5.block_size), b''):
                md5.update(chunk)
        checksum = md5.hexdigest()
        return checksum

    def synchronize(self, false_update = False):
        result = {}
        bucket = boto3.resource('s3').Bucket(self.bucket_name)
        for s3_object in self.response['Contents']:
            package_path = os.path.join(self.local_package_directory, s3_object['Key'])
            metadata = self.s3.head_object(Bucket=self.bucket_name, Key=s3_object['Key'])
            md5_hash = metadata["ResponseMetadata"]["HTTPHeaders"]["x-amz-meta-codebuild-content-md5"]
            if not os.path.exists(os.path.dirname(package_path)):
                os.makedirs(os.path.dirname(package_path))
            action = {}
            stamp = {}
            if false_update:
                bucket.download_file(s3_object['Key'], package_path)
                action = {'action' : 'download new package'}
                stamp = {'stamp' : datetime.datetime.now().isoformat()}
            else:
                if not os.path.exists(package_path):
                    bucket.download_file(s3_object['Key'], package_path)
                    action = {'action' : 'download new package'}
                    stamp = {'stamp' : datetime.datetime.now().isoformat()}
                else :
                    if self.getHash(package_path) != md5_hash :
                        os.remove(package_path)
                        bucket.download_file(s3_object['Key'], package_path)
                        action = {'action' : 'update package'}
                        stamp = {'stamp' : datetime.datetime.now().isoformat()}
                    else:
                        action = {'action' : 'skip download package'}
                        stamp = {'stamp' : datetime.datetime.now().isoformat()}
            result[s3_object['Key']] = {}
            result[s3_object['Key']].update(action)
            result[s3_object['Key']].update(stamp)
        return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='synchronize debian package in S3')
    parser.add_argument('config_path', help='path to the config yaml path')
    args = parser.parse_args()
    sync = PackageSynchronizer(args.config_path)
    sync.synchronize(False)
"""Audit Agent for AWS resource scanning"""
import boto3
from typing import List, Dict
from datetime import datetime

class AuditAgent:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.rds = boto3.client('rds')
        self.s3 = boto3.client('s3')
        self.iam = boto3.client('iam')
    
    def scan_ec2_instances(self) -> List[Dict]:
        """Scan EC2 instances for compliance"""
        try:
            response = self.ec2.describe_instances()
            instances = []
            
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    instances.append({
                        'resource_type': 'EC2',
                        'resource_id': instance['InstanceId'],
                        'state': instance['State']['Name'],
                        'security_groups': [sg['GroupId'] for sg in instance['SecurityGroups']],
                        'encrypted': instance.get('EbsOptimized', False),
                        'last_scan': datetime.now().isoformat()
                    })
            return instances
        except Exception as e:
            return [{'error': f'EC2 scan failed: {str(e)}'}]
    
    def scan_rds_instances(self) -> List[Dict]:
        """Scan RDS instances for compliance"""
        try:
            response = self.rds.describe_db_instances()
            instances = []
            
            for db in response['DBInstances']:
                instances.append({
                    'resource_type': 'RDS',
                    'resource_id': db['DBInstanceIdentifier'],
                    'engine': db['Engine'],
                    'encrypted': db.get('StorageEncrypted', False),
                    'backup_retention': db.get('BackupRetentionPeriod', 0),
                    'multi_az': db.get('MultiAZ', False),
                    'last_scan': datetime.now().isoformat()
                })
            return instances
        except Exception as e:
            return [{'error': f'RDS scan failed: {str(e)}'}]
    
    def scan_s3_buckets(self) -> List[Dict]:
        """Scan S3 buckets for compliance"""
        try:
            response = self.s3.list_buckets()
            buckets = []
            
            for bucket in response['Buckets']:
                bucket_name = bucket['Name']
                try:
                    encryption = self.s3.get_bucket_encryption(Bucket=bucket_name)
                    encrypted = True
                except:
                    encrypted = False
                
                buckets.append({
                    'resource_type': 'S3',
                    'resource_id': bucket_name,
                    'encrypted': encrypted,
                    'creation_date': bucket['CreationDate'].isoformat(),
                    'last_scan': datetime.now().isoformat()
                })
            return buckets
        except Exception as e:
            return [{'error': f'S3 scan failed: {str(e)}'}]
    
    def get_all_resources(self) -> List[Dict]:
        """Get all AWS resources for compliance scanning"""
        resources = []
        resources.extend(self.scan_ec2_instances())
        resources.extend(self.scan_rds_instances())
        resources.extend(self.scan_s3_buckets())
        return resources
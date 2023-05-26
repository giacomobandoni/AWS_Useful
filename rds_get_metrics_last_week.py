import datetime
import boto3
import warnings
import sys

warnings.filterwarnings('ignore', category=FutureWarning, module='botocore.client')

cloudwatch_client = boto3.client('cloudwatch', region_name='us-east-1')

rds_instance = sys.argv[1]

response = cloudwatch_client.get_metric_data(
    MetricDataQueries=[
        {
            'Id': 'fetching_data_for_something',
            'MetricStat': {
                'Metric': {
                    'Namespace': 'AWS/RDS',
                    'MetricName': 'DatabaseConnections',
                    'Dimensions': [
                        {
                            'Name': 'DBInstanceIdentifier',
                            'Value': rds_instance
                        },
                    ]
                },
                'Period': 3600,
                'Stat': 'Average'
            },
            'ReturnData': True
        },
    ],
    StartTime=datetime.datetime.utcnow() - datetime.timedelta(days=7),
    EndTime=datetime.datetime.utcnow(),
    ScanBy='TimestampDescending',
    MaxDatapoints=123
)

noConnections=True
for connection in response['MetricDataResults'][0]['Values']:
    if connection > 0:
        noConnections=False

if noConnections:
    print('No connections in the last week')
else:
    print('At least one connection in the last week')

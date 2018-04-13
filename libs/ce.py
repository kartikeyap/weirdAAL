'''
Cost Explorer Library
'''

import boto3
import botocore
import pprint
import sys

pp = pprint.PrettyPrinter(indent=5, width=80)

#from http://docs.aws.amazon.com/general/latest/gr/rande.html
regions = ['us-east-1', ]

def ce_get_cost_and_usage(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY):
    try:
        for region in regions:
            client = boto3.client('ce', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=region)
            response = client.get_cost_and_usage(TimePeriod={'Start': '2018-01-01', 'End': '2018-04-01'}, Granularity='MONTHLY', Metrics=["BlendedCost", "UnblendedCost", "UsageQuantity"],)
            print(response)
            #if response.get('Services') is None:
            #    print("{} likely does not have Pricing permissions\n" .format(AWS_ACCESS_KEY_ID))
            #elif len(response['Services']) <= 0:
            #    print("[-] Describe Pricing Services allowed for {} but no results [-]" .format(region))
            #else:
            #    print("### {} Services  ###" .format(region))
            #    for tables in response['ServiceCode']:
            #        pp.pprint(tables)
            #        print("\n")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'UnauthorizedOperation':
            print('{} : (UnauthorizedOperation) when calling the DescribeInstances -- sure you have ec2 permissions?' .format(AWS_ACCESS_KEY_ID))
        elif e.response['Error']['Code'] == 'AccessDeniedException':
        	print('{} : (AccessDenied) when calling the Get Cost & Usage' .format(AWS_ACCESS_KEY_ID))
        elif e.response['Error']['Code'] == 'SubscriptionRequiredException':
            print('{} : Has permissions but isnt signed up for service - usually means you have a root account' .format(AWS_ACCESS_KEY_ID))
        else:
            print(e)
    except KeyboardInterrupt:
        print("CTRL-C received, exiting...")
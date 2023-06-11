import boto3


'''
    please set dynamodbURL as None before commiting the code.
    use this configuration only for local testing

'''

# dynamodbURL = "http://localhost:4566"
dynamodbURL = None


def boto3_client(**kwargs):

    if (not dynamodbURL == None):
        kwargs['endpoint_url'] = dynamodbURL
        return boto3.resource(**kwargs)

    else:
        return boto3.resource(**kwargs)

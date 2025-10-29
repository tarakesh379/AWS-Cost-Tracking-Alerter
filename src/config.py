import os

SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:ap-south-1:331867786280:cost-alerts-topic')
BUDGET_THRESHOLD = float(os.environ.get('BUDGET_THRESHOLD', '8.00'))
AWS_REGION = os.environ.get('AWS_REGION', 'ap-south-1')

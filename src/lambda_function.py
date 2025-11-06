import json
import boto3
from datetime import datetime, timedelta
import os

def lambda_handler(event, context):
    print("=== AWS Cost Tracking Alerter ===")
    print("Built on CentOS Stream 9 - Python 3.9")
    
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')
    aws_region = os.environ.get('AWS_REGION', 'ap-south-1')
    budget_threshold = float(os.environ.get('BUDGET_THRESHOLD', '8.00'))
    
    if not sns_topic_arn:
        print("ERROR: SNS_TOPIC_ARN environment variable not set")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'SNS_TOPIC_ARN not configured'})
        }
    
    print(f"Using SNS Topic: {sns_topic_arn}")
    print(f"AWS Region: {aws_region}")
    print(f"Budget Threshold: ${budget_threshold}")
    
    try:
        sns_client = boto3.client('sns', region_name=aws_region)
        ce_client = boto3.client('ce', region_name=aws_region)
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        print(f"Checking costs from {start_date} to {end_date}")

        response = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['BlendedCost'],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'SERVICE'
                }
            ]
        )

        total_cost = 0
        service_costs = {}

        for day in response['ResultsByTime']:
            for group in day['Groups']:
                service = group['Keys'][0]
                cost = float(group['Metrics']['BlendedCost']['Amount'])

                if service in service_costs:
                    service_costs[service] += cost
                else:
                    service_costs[service] = cost

                total_cost += cost

        print(f"Total cost: ${total_cost:.4f}")

        if total_cost > budget_threshold:
            print("Cost exceeds threshold - sending alert...")
            send_alert(sns_client, total_cost, service_costs, sns_topic_arn)
        else:
            print(f"Cost within budget: ${total_cost:.2f} < ${budget_threshold}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'total_cost': f"${total_cost:.4f}",
                'top_services': dict(sorted(service_costs.items(), key=lambda x: x[1], reverse=True)[:3]),
                'alert_sent': total_cost > budget_threshold,
                'built_on': 'CentOS Stream 9',
                'config_method': 'environment_variables'
            })
        }

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def send_alert(sns_client, total_cost, service_costs, sns_topic_arn):
    try:
        message = f"""
- AWS COST ALERT - Built on CentOS Stream 9 -

Your current AWS costs: ${total_cost:.2f}
Budget threshold: ${budget_threshold} (80% of $10 budget)

Top services by cost:
"""
        for service, cost in sorted(service_costs.items(), key=lambda x: x[1], reverse=True)[:3]:
            message += f"• {service}: ${cost:.2f}\n"
        
        message += "\nBuilt with Python 3.9 on CentOS Stream 9"
        message += f"\nSNS Topic: [Configured via environment]"
        
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject='AWS Cost Alert - Built on CentOS Stream 9',
            Message=message
        )
        
        print(f"Alert sent successfully! Message ID: {response['MessageId']}")
        
    except Exception as e:
        print(f"Failed to send alert: {str(e)}")

# Test locally (only if SNS_TOPIC_ARN is set)
if __name__ == "__main__":
    if os.environ.get('SNS_TOPIC_ARN'):
        result = lambda_handler({}, {})
        print(result)
    else:
        print("SNS_TOPIC_ARN not set - skipping local test")

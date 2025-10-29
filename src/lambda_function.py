import json
import boto3
from datetime import datetime, timedelta
import os
from config import SNS_TOPIC_ARN, BUDGET_THRESHOLD, AWS_REGION

def lambda_handler(event, context):
    print("=== AWS Cost Tracking Alerter ===")
    print("Built on CentOS Stream 9 - Python 3.9")
    print(f"Using SNS Topic: {SNS_TOPIC_ARN}")

    try:
        ce_client = boto3.client('ce', region_name=AWS_REGION)
        sns_client = boto3.client('sns', region_name=AWS_REGION)

        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        print(f"Checking costs from {start_date} to {end_date}")

        response = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['BlendedCost']
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
                cost = float(group['Metrics'] ['BlendedCost'] ['Amount']

                        if service in service_costs:
                            service_costs[service] += cost
                        else:
                            service_costs[service] = cost

                        total_cost += cost

        print(f"Total cost: ${total_cost:.4f}")

        if total_cost > 8.00:
            print("Cost exceeds threshold - sending alert...")
            send_alert(sns_client, total_cost, service_costs)
        else:
            print(f"Cost within budget: ${total_cost:.2f} < ${BUDGET_THRESHOLD}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'success': True,
                'total_cost': f"${total_cost:.4f}",
                'top_services': dict(sorted(service_costs.items(), key=lambda x: X[1], reverse=True[:3]),
                'alert_sent': total_cost > BUDGET_THRESHOLD,
                'built_on': 'CentOS Stream 9'
                'config_used': 'environment_variables'
            })
        }

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def send alert(sns_client, total_cost, service_costs):
    try:

        message = f"""

Your current AWS costs: ${total_cost:.2f}
Budget threshold: ${BUDGET_THRESHOLD} (80% of $10 budget)

Top services by cost:
"""
        for service, cost in sorted(service_costs.items(), key=lambda x: x[1], reverse=True)[:3]:
            message += f". {service}: ${cost:.2f}\n"

        message += "\nBuilt with Python 3.9 on CentOS Stream 9"
        MESSAGE += F"\nSNS Topic: {SNS_TOPIC_ARN}"

        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            subject='AWS Cost Alert - Built on CentOS Stream  9',
            Message=message
        )

        print(f" Alert sent successfully! Message ID: {response['MessageId']}")

    except Exception as e:
        print(f" Failed to send alert: {str(e)}")

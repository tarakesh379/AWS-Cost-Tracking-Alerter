AWS-Cost-Tracking-Alerter


Decription:
A serverless AWS cost monitoring system built on CentOS Stream 9 that tracks spending and sends email alerts when budget thresholds are exceeded.

>> Project Overview

AWS-Cost-Tracking-Alerter is a project designed to help AWS users monitor their cloud spending effectively. The system uses AWS Lambda for serverless compute, AWS Cost Explorer for cost analysis, and Amazon SNS for email notifications.

>> Key Features

- Real-time cost tracking: Monitors AWS spending in real-time.
- Email alerts: Sends automated email alerts when costs exceed predefined thresholds.
- Serverless architecture: Utilizes AWS Lambda and SNS for a scalable and cost-effective solution.
- Environment variables: Configuration is managed through environment variables for security and flexibility.

>> Challenges Faced

1. IAM Permissions: Initially, setting up the IAM role and policies for secure access to AWS services was challenging.
2. Environment Variables: Managing configuration and secrets securely without hardcoding credentials in the codebase.
3. Error Handling: Implementing robust error handling in Lambda functions to ensure the system remains operational even when individual services fail.

>> How I Overcame Them

1. IAM Permissions: Thoroughly reviewed AWS documentation and best practices to define the necessary permissions.
2. Environment Variables: Used `.env` files and AWS Secrets Manager to manage configuration securely.
3. Error Handling: Added try-catch blocks and logging to capture and resolve errors gracefully.
>> Technologies Used

- AWS Lambda: Serverless compute service for running the main logic.
- AWS Cost Explorer: API for retrieving cost data.
- Amazon SNS: Notification service for sending email alerts.
- CentOS Stream 9: Development environment for building and testing the application.
- Python 3.9: Programming language for writing Lambda functions.

>> Learning Outcomes

Through this project, I gained hands-on experience with AWS services, improved my ability to troubleshoot and debug cloud applications, and learned best practices for managing secrets and configurations securely.

>> Next Steps

- Further refine the alerting mechanism to include SMS notifications.
- Implement a dashboard using AWS CloudWatch to visualize cost trends.
- Explore integrating with AWS Budgets to automate cost management.

-- Contact --

For more information, feel free to reach out:

- LinkedIn: https://www.linkedin.com/in/tarakesh-naidu-tentu-047b36197
- Email: tarakeswaranaidu379@gmail.com

---

This README provides a clear, concise overview of the project, the challenges faced, and how they were overcome. It highlights the technologies used and the learning outcomes in a way that is accessible to both beginners and professionals.

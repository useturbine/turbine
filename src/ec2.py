import os
import boto3
import json
from flask import Flask, render_template, send_from_directory, jsonify

app = Flask(__name__)

# AWS Configuration
AWS_REGION = 'us-east-1'  # Change to your desired region
EC2_CLIENT = boto3.client('ec2', region_name=AWS_REGION)

# Directory to store generated Terraform files
OUTPUT_DIR = 'terraform_output'

@app.route('/')
def index():
    return 'Welcome to EC2 Exporter!'

@app.route('/export_ec2', methods=['GET'])
def export_ec2():
    try:
        ec2_instances = list_ec2_instances()
        generate_tf_files(ec2_instances)
        return jsonify({'message': 'EC2 instances exported successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def list_ec2_instances():
    response = EC2_CLIENT.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_data = {
                'InstanceID': instance['InstanceId'],
                'InstanceType': instance['InstanceType'],
                'KeyName': instance.get('KeyName', ''),
                'SecurityGroups': [sg['GroupName'] for sg in instance.get('SecurityGroups', [])],
                'Tags': instance.get('Tags', [])
            }
            instances.append(instance_data)
    return instances

def generate_tf_files(ec2_instances):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for instance in ec2_instances:
        instance_id = instance['InstanceID']
        file_name = f'{OUTPUT_DIR}/ec2_instance_{instance_id}.tf'
        with open(file_name, 'w') as f:
            f.write('# This is a generated Terraform configuration for EC2 instance.\n')
            f.write(f'resource "aws_instance" "{instance_id}" {{\n')
            f.write(f'  instance_type = "{instance["InstanceType"]}"\n')
            f.write(f'  key_name = "{instance["KeyName"]}"\n')
            f.write('  # Add other resource properties here\n')
            f.write('}\n')

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_from_directory(directory=OUTPUT_DIR, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)

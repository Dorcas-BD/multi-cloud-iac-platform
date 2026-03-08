#!/usr/bin/env python3
"""
AWS Cost Optimization Script
Identifies unused and underutilized resources to reduce costs.
"""

import boto3
from datetime import datetime, timedelta
import json

class CostOptimizer:
    def __init__(self, region='us-east-1'):
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.findings = []
        
    def check_unused_eips(self):
        """Find unattached Elastic IPs"""
        print("\n[*] Checking for unused Elastic IPs...")
        eips = self.ec2.describe_addresses()
        
        for eip in eips['Addresses']:
            if 'InstanceId' not in eip:
                cost_per_month = 3.60
                self.findings.append({
                    'resource': 'Elastic IP',
                    'id': eip['AllocationId'],
                    'public_ip': eip.get('PublicIp', 'N/A'),
                    'issue': 'Not attached to any instance',
                    'monthly_cost': f'${cost_per_month:.2f}',
                    'recommendation': 'Release if not needed'
                })
                print(f"  Unused EIP: {eip.get('PublicIp')} - Costs ${cost_per_month:.2f}/month")
        
    def check_stopped_instances(self):
        """Find stopped EC2 instances"""
        print("\n[*] Checking for stopped EC2 instances...")
        instances = self.ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
        )
        
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                launch_time = instance['LaunchTime']
                storage_cost = 3.00
                
                self.findings.append({
                    'resource': 'EC2 Instance',
                    'id': instance_id,
                    'type': instance_type,
                    'state': 'stopped',
                    'launched': launch_time.strftime('%Y-%m-%d'),
                    'monthly_cost': f'${storage_cost:.2f}',
                    'recommendation': 'Terminate if no longer needed'
                })
                print(f" Stopped instance: {instance_id} ({instance_type}) - Storage costs ${storage_cost:.2f}/month")
    
    def check_underutilized_instances(self):
        """Find instances with low CPU utilization"""
        print("\n[*] Checking for underutilized EC2 instances...")
        instances = self.ec2.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
        )
        
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=7)
        
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                
                try:
                    cpu_stats = self.cloudwatch.get_metric_statistics(
                        Namespace='AWS/EC2',
                        MetricName='CPUUtilization',
                        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                        StartTime=start_time,
                        EndTime=end_time,
                        Period=86400,
                        Statistics=['Average']
                    )
                    
                    if cpu_stats['Datapoints']:
                        avg_cpu = sum(dp['Average'] for dp in cpu_stats['Datapoints']) / len(cpu_stats['Datapoints'])
                        
                        if avg_cpu < 10:
                            self.findings.append({
                                'resource': 'EC2 Instance',
                                'id': instance_id,
                                'type': instance_type,
                                'avg_cpu_7d': f'{avg_cpu:.2f}%',
                                'issue': 'Very low CPU utilization',
                                'recommendation': 'Consider downsizing or spot instances'
                            })
                            print(f" Low CPU usage: {instance_id} ({instance_type}) - Avg: {avg_cpu:.2f}%")
                except Exception as e:
                    print(f"   Could not fetch metrics for {instance_id}")
    
    def check_unattached_volumes(self):
        """Find unattached EBS volumes"""
        print("\n[*] Checking for unattached EBS volumes...")
        volumes = self.ec2.describe_volumes(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )
        
        for volume in volumes['Volumes']:
            volume_id = volume['VolumeId']
            size = volume['Size']
            volume_type = volume['VolumeType']
            cost_per_month = size * 0.08
            
            self.findings.append({
                'resource': 'EBS Volume',
                'id': volume_id,
                'size': f'{size}GB',
                'type': volume_type,
                'issue': 'Not attached to any instance',
                'monthly_cost': f'${cost_per_month:.2f}',
                'recommendation': 'Delete if not needed'
            })
            print(f"  Unattached volume: {volume_id} ({size}GB) - Costs ${cost_per_month:.2f}/month")
    
    def generate_report(self):
        """Generate summary report"""
        print("\n" + "="*60)
        print("COST OPTIMIZATION SUMMARY")
        print("="*60)
        
        if not self.findings:
            print("\n No cost optimization opportunities found!")
            print("Your infrastructure is well optimized.")
            return
        
        print(f"\nFound {len(self.findings)} optimization opportunities:\n")
        
        by_type = {}
        total_monthly_savings = 0
        
        for finding in self.findings:
            resource_type = finding['resource']
            if resource_type not in by_type:
                by_type[resource_type] = []
            by_type[resource_type].append(finding)
            
            if 'monthly_cost' in finding:
                cost = float(finding['monthly_cost'].replace('$', ''))
                total_monthly_savings += cost
        
        for resource_type, items in by_type.items():
            print(f"{resource_type}: {len(items)} items")
        
        print(f"\n Potential monthly savings: ${total_monthly_savings:.2f}")
        print(f" Potential yearly savings: ${total_monthly_savings * 12:.2f}")
        
        report_file = 'scripts/cost-optimization/cost-report.json'
        with open(report_file, 'w') as f:
            json.dump({
                'scan_date': datetime.now().isoformat(),
                'region': self.region,
                'total_findings': len(self.findings),
                'potential_monthly_savings': round(total_monthly_savings, 2),
                'potential_yearly_savings': round(total_monthly_savings * 12, 2),
                'findings': self.findings
            }, f, indent=2, default=str)
        
        print(f"\n Detailed report saved to: {report_file}")
    
    def run_all_checks(self):
        """Run all optimization checks"""
        print("Starting AWS Cost Optimization Scan...")
        print(f"Region: {self.region}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.check_unused_eips()
        self.check_stopped_instances()
        self.check_underutilized_instances()
        self.check_unattached_volumes()
        
        self.generate_report()

if __name__ == '__main__':
    optimizer = CostOptimizer(region='us-east-1')
    optimizer.run_all_checks()

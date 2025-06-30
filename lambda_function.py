"""AWS Lambda function for serverless compliance monitoring"""
import json
import boto3
from agents.audit_agent import AuditAgent
from agents.compliance_agent import ComplianceAgent
from agents.policy_agent import PolicyAgent

def lambda_handler(event, context):
    """Main Lambda handler for compliance monitoring"""
    
    try:
        # Initialize agents
        audit_agent = AuditAgent()
        compliance_agent = ComplianceAgent()
        policy_agent = PolicyAgent()
        
        # Get request type
        request_type = event.get('request_type', 'scan')
        
        if request_type == 'scan':
            # Scan AWS resources
            resources = audit_agent.get_all_resources()
            
            # Analyze compliance for each resource
            compliance_results = []
            for resource in resources:
                if 'error' not in resource:
                    # Check against multiple frameworks
                    for framework in ['GDPR', 'FISMA', 'EU_AI_ACT']:
                        result = compliance_agent.analyze_compliance(resource, framework)
                        result['resource'] = resource
                        result['framework'] = framework
                        compliance_results.append(result)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Compliance scan completed',
                    'resources_scanned': len(resources),
                    'compliance_results': compliance_results
                })
            }
        
        elif request_type == 'enforce':
            # Enforce policies
            resource = event.get('resource', {})
            framework = event.get('framework', 'GDPR')
            
            enforcement_result = policy_agent.enforce_policy(resource, framework)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Policy enforcement completed',
                    'result': enforcement_result
                })
            }
        
        elif request_type == 'report':
            # Generate compliance report
            violations = event.get('violations', [])
            report = compliance_agent.generate_compliance_report(violations)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Compliance report generated',
                    'report': report
                })
            }
        
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Invalid request type'
                })
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
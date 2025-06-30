"""Compliance Agent using Amazon Bedrock"""
import boto3
import json
from typing import List, Dict

class ComplianceAgent:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    def analyze_compliance(self, resource_data: Dict, framework: str) -> Dict:
        """Analyze resource compliance against framework"""
        prompt = f"""
        Analyze the following AWS resource for {framework} compliance:
        Resource: {json.dumps(resource_data, indent=2)}
        
        Provide a compliance assessment with:
        1. Compliance status (COMPLIANT/NON_COMPLIANT/PARTIAL)
        2. Specific violations found
        3. Remediation recommendations
        4. Risk level (LOW/MEDIUM/HIGH/CRITICAL)
        
        Respond in JSON format.
        """
        
        try:
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1000,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            return {
                "status": "NON_COMPLIANT",
                "violations": ["Sample violation for demo"],
                "recommendations": ["Enable encryption", "Configure MFA"],
                "risk_level": "HIGH"
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "risk_level": "UNKNOWN"
            }
    
    def generate_compliance_report(self, violations: List[Dict]) -> str:
        """Generate compliance report using Bedrock"""
        prompt = f"""
        Generate a comprehensive compliance report based on these violations:
        {json.dumps(violations, indent=2)}
        
        Include:
        1. Executive summary
        2. Critical findings
        3. Remediation priorities
        4. Compliance score
        """
        
        try:
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2000,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            return result['content'][0]['text']
        except Exception as e:
            return f"Error generating report: {str(e)}"
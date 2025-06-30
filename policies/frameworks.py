"""Compliance frameworks and policy definitions"""

COMPLIANCE_FRAMEWORKS = {
    "GDPR": {
        "name": "General Data Protection Regulation",
        "rules": [
            "Personal data must be encrypted at rest and in transit",
            "Data retention policies must be defined and enforced",
            "User consent must be obtained for data processing",
            "Data breach notifications within 72 hours",
            "Right to be forgotten must be implemented"
        ],
        "risk_level": "HIGH"
    },
    "FISMA": {
        "name": "Federal Information Security Management Act",
        "rules": [
            "Multi-factor authentication required",
            "Regular security assessments mandatory",
            "Incident response procedures documented",
            "Access controls based on least privilege",
            "Continuous monitoring implemented"
        ],
        "risk_level": "CRITICAL"
    },
    "EU_AI_ACT": {
        "name": "EU AI Act",
        "rules": [
            "High-risk AI systems require conformity assessment",
            "AI system documentation and transparency required",
            "Human oversight for automated decision-making",
            "Bias testing and mitigation implemented",
            "AI system registration in EU database"
        ],
        "risk_level": "HIGH"
    },
    "ISO_42001": {
        "name": "ISO/IEC 42001 AI Management",
        "rules": [
            "AI governance framework established",
            "Risk management for AI systems",
            "AI system lifecycle management",
            "Stakeholder engagement documented",
            "Continuous improvement processes"
        ],
        "risk_level": "MEDIUM"
    }
}

POLICY_VIOLATIONS = [
    {"framework": "GDPR", "resource": "RDS Database", "violation": "Unencrypted personal data", "severity": "HIGH"},
    {"framework": "FISMA", "resource": "EC2 Instance", "violation": "Missing MFA", "severity": "CRITICAL"},
    {"framework": "EU_AI_ACT", "resource": "SageMaker Model", "violation": "No bias testing", "severity": "HIGH"},
    {"framework": "ISO_42001", "resource": "Lambda Function", "violation": "Missing AI documentation", "severity": "MEDIUM"}
]
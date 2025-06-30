"""EnforceAI - Multi-Agent Governance & Compliance Platform"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Import agents
from agents.compliance_agent import ComplianceAgent
from agents.audit_agent import AuditAgent
from agents.policy_agent import PolicyAgent
from policies.frameworks import COMPLIANCE_FRAMEWORKS, POLICY_VIOLATIONS

# Page config
st.set_page_config(
    page_title="EnforceAI - Governance Platform",
    page_icon="🛡️",
    layout="wide"
)

# Initialize session state
if 'scan_results' not in st.session_state:
    st.session_state.scan_results = []
if 'compliance_score' not in st.session_state:
    st.session_state.compliance_score = 75

def main():
    st.title("🛡️ EnforceAI - Multi-Agent Governance Platform")
    st.markdown("*AI-powered DevOps compliance and governance automation*")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", [
        "Dashboard", 
        "Compliance Monitoring", 
        "Policy Management", 
        "AI Assistant",
        "Reports"
    ])
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Compliance Monitoring":
        show_compliance_monitoring()
    elif page == "Policy Management":
        show_policy_management()
    elif page == "AI Assistant":
        show_ai_assistant()
    elif page == "Reports":
        show_reports()

def show_dashboard():
    st.header("📊 Compliance Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Compliance Score", f"{st.session_state.compliance_score}%", "↑ 5%")
    
    with col2:
        st.metric("Active Policies", "12", "↑ 2")
    
    with col3:
        st.metric("Resources Monitored", "156", "↑ 8")
    
    with col4:
        st.metric("Critical Violations", "3", "↓ 2")
    
    # Compliance score chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Compliance Score Trend")
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        scores = [70 + (i % 10) + (i // 5) for i in range(len(dates))]
        
        fig = px.line(x=dates, y=scores, title="30-Day Compliance Trend")
        fig.update_layout(xaxis_title="Date", yaxis_title="Compliance Score (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Framework Compliance")
        frameworks = list(COMPLIANCE_FRAMEWORKS.keys())
        scores = [85, 72, 68, 90]
        
        fig = px.bar(x=frameworks, y=scores, title="Compliance by Framework")
        fig.update_layout(xaxis_title="Framework", yaxis_title="Compliance Score (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent violations
    st.subheader("🚨 Recent Policy Violations")
    violations_df = pd.DataFrame(POLICY_VIOLATIONS)
    st.dataframe(violations_df, use_container_width=True)

def show_compliance_monitoring():
    st.header("🔍 Compliance Monitoring")
    
    # Real-time scanning
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("AWS Resource Scanning")
        
        if st.button("🔄 Start Compliance Scan", type="primary"):
            with st.spinner("Scanning AWS resources..."):
                audit_agent = AuditAgent()
                compliance_agent = ComplianceAgent()
                
                # Get resources
                resources = audit_agent.get_all_resources()
                st.session_state.scan_results = resources
                
                st.success(f"Scanned {len(resources)} resources")
        
        # Display scan results
        if st.session_state.scan_results:
            st.subheader("Scan Results")
            results_df = pd.DataFrame(st.session_state.scan_results)
            st.dataframe(results_df, use_container_width=True)
    
    with col2:
        st.subheader("Framework Selection")
        selected_frameworks = st.multiselect(
            "Select compliance frameworks:",
            list(COMPLIANCE_FRAMEWORKS.keys()),
            default=["GDPR", "FISMA"]
        )
        
        st.subheader("Scan Configuration")
        scan_frequency = st.selectbox("Scan Frequency", ["Real-time", "Hourly", "Daily", "Weekly"])
        auto_remediation = st.checkbox("Enable Auto-remediation", value=True)
    
    # Framework details
    st.subheader("📋 Compliance Frameworks")
    for framework, details in COMPLIANCE_FRAMEWORKS.items():
        with st.expander(f"{framework} - {details['name']}"):
            st.write(f"**Risk Level:** {details['risk_level']}")
            st.write("**Rules:**")
            for rule in details['rules']:
                st.write(f"• {rule}")

def show_policy_management():
    st.header("⚙️ Policy Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Create New Policy")
        
        policy_name = st.text_input("Policy Name")
        policy_framework = st.selectbox("Framework", list(COMPLIANCE_FRAMEWORKS.keys()))
        policy_description = st.text_area("Description")
        policy_rules = st.text_area("Rules (one per line)")
        
        if st.button("Create Policy"):
            st.success(f"Policy '{policy_name}' created successfully!")
    
    with col2:
        st.subheader("Policy Enforcement")
        
        # Simulate policy enforcement
        if st.button("🚀 Run Policy Enforcement"):
            with st.spinner("Enforcing policies..."):
                policy_agent = PolicyAgent()
                
                # Mock resource for demo
                mock_resource = {
                    "resource_id": "i-1234567890abcdef0",
                    "resource_type": "EC2",
                    "encrypted": False
                }
                
                result = policy_agent.enforce_policy(mock_resource, "GDPR")
                
                st.json(result)
    
    # Active policies table
    st.subheader("Active Policies")
    policies_data = [
        {"Name": "GDPR Data Encryption", "Framework": "GDPR", "Status": "Active", "Last Updated": "2024-01-15"},
        {"Name": "FISMA Access Control", "Framework": "FISMA", "Status": "Active", "Last Updated": "2024-01-14"},
        {"Name": "AI Act Compliance", "Framework": "EU_AI_ACT", "Status": "Active", "Last Updated": "2024-01-13"}
    ]
    
    policies_df = pd.DataFrame(policies_data)
    st.dataframe(policies_df, use_container_width=True)

def show_ai_assistant():
    st.header("🤖 AI Compliance Assistant")
    st.markdown("*Powered by Amazon Bedrock*")
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI compliance assistant. How can I help you with governance and compliance today?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about compliance, policies, or governance..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Simulate AI response using Bedrock
                compliance_agent = ComplianceAgent()
                
                if "gdpr" in prompt.lower():
                    response = "GDPR requires encryption of personal data at rest and in transit. I can help you scan your AWS resources for GDPR compliance. Would you like me to run a compliance check?"
                elif "policy" in prompt.lower():
                    response = "I can help you create, manage, and enforce compliance policies. What specific policy framework are you working with?"
                elif "scan" in prompt.lower():
                    response = "I can perform real-time compliance scans of your AWS infrastructure. This includes EC2, RDS, S3, and other services. Shall I start a scan?"
                else:
                    response = "I can assist with compliance monitoring, policy enforcement, and governance automation. What specific area would you like help with?"
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

def show_reports():
    st.header("📄 Compliance Reports")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Generate Report")
        
        report_type = st.selectbox("Report Type", [
            "Executive Summary",
            "Detailed Compliance Report",
            "Violation Analysis",
            "Remediation Plan"
        ])
        
        report_framework = st.multiselect(
            "Frameworks",
            list(COMPLIANCE_FRAMEWORKS.keys()),
            default=["GDPR", "FISMA"]
        )
        
        if st.button("📊 Generate Report", type="primary"):
            with st.spinner("Generating compliance report..."):
                compliance_agent = ComplianceAgent()
                
                # Generate report using Bedrock
                report = compliance_agent.generate_compliance_report(POLICY_VIOLATIONS)
                
                st.subheader("Generated Report")
                st.markdown("""
                ## Executive Compliance Summary
                
                **Overall Compliance Score:** 75%
                
                ### Key Findings:
                - 4 critical violations identified across GDPR and FISMA frameworks
                - 12 resources require immediate attention
                - Auto-remediation available for 8 violations
                
                ### Priority Actions:
                1. Enable encryption on RDS databases (GDPR)
                2. Configure MFA for EC2 instances (FISMA)
                3. Implement bias testing for ML models (EU AI Act)
                4. Update AI documentation (ISO 42001)
                
                ### Compliance Scores by Framework:
                - GDPR: 72% (Needs Improvement)
                - FISMA: 68% (Critical)
                - EU AI Act: 85% (Good)
                - ISO 42001: 90% (Excellent)
                """)
    
    with col2:
        st.subheader("Report History")
        
        reports_data = [
            {"Date": "2024-01-15", "Type": "Executive", "Score": "75%"},
            {"Date": "2024-01-14", "Type": "Detailed", "Score": "73%"},
            {"Date": "2024-01-13", "Type": "Violation", "Score": "71%"}
        ]
        
        for report in reports_data:
            st.write(f"**{report['Date']}** - {report['Type']} ({report['Score']})")
        
        st.subheader("Export Options")
        st.button("📥 Download PDF")
        st.button("📧 Email Report")
        st.button("☁️ Save to S3")

if __name__ == "__main__":
    main()
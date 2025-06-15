import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import base64
from io import BytesIO

from compliance_checker import ComplianceChecker
from document_processor import DocumentProcessor
from report_generator import ReportGenerator

# Configure page
st.set_page_config(
    page_title="AI Compliance Checker",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = None

def main():
    st.title("🛡️ AI-Powered Enterprise Compliance Checker")
    st.markdown("**Detect regulatory violations across GDPR, SOC2, HIPAA, and RBI frameworks**")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Compliance frameworks selection
        st.subheader("Compliance Frameworks")
        frameworks = st.multiselect(
            "Select frameworks to check:",
            ["GDPR", "SOC2", "HIPAA", "RBI"],
            default=["GDPR", "SOC2", "HIPAA", "RBI"]
        )
        
        # Analysis settings
        st.subheader("Analysis Settings")
        sensitivity_level = st.selectbox(
            "Detection Sensitivity:",
            ["High", "Medium", "Low"],
            index=1
        )
        
        include_pii = st.checkbox("Include PII Detection", value=True)
        include_ai_analysis = st.checkbox("Include AI Analysis", value=True)
        
        # API Key status
        st.subheader("System Status")
        checker = ComplianceChecker()
        if checker.check_api_connection():
            st.success("✅ OpenAI API Connected")
        else:
            st.error("❌ OpenAI API Not Available")
            st.info("Set OPENAI_API_KEY environment variable")
    
    # Main content area
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.header("📄 Document Upload")
        
        uploaded_file = st.file_uploader(
            "Choose a document to analyze",
            type=['pdf', 'docx', 'txt'],
            help="Supported formats: PDF, Word Documents, Text files"
        )
        
        if uploaded_file:
            st.session_state.uploaded_file_name = uploaded_file.name
            
            # File info
            file_details = {
                "Filename": uploaded_file.name,
                "File Size": f"{uploaded_file.size} bytes",
                "File Type": uploaded_file.type
            }
            st.json(file_details)
            
            # Analysis button
            analyze_button = st.button(
                "🔍 Analyze Document",
                type="primary",
                use_container_width=True
            )
            
            if analyze_button:
                with st.spinner("Processing document and analyzing compliance..."):
                    try:
                        # Process document
                        processor = DocumentProcessor()
                        text_content = processor.process_file(uploaded_file)
                        
                        if not text_content.strip():
                            st.error("No text content found in the document.")
                            return
                        
                        # Initialize compliance checker
                        checker = ComplianceChecker(
                            frameworks=frameworks,
                            sensitivity=sensitivity_level.lower(),
                            include_pii=include_pii,
                            include_ai_analysis=include_ai_analysis
                        )
                        
                        # Perform analysis
                        results = checker.analyze_document(text_content)
                        st.session_state.analysis_results = results
                        
                        st.success("✅ Analysis completed successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")
    
    with col2:
        st.header("📊 Analysis Results")
        
        if st.session_state.analysis_results:
            results = st.session_state.analysis_results
            
            # Summary metrics
            st.subheader("Compliance Summary")
            
            total_violations = sum(len(results['violations'].get(fw, [])) for fw in frameworks)
            total_pii = len(results.get('pii_entities', []))
            compliance_score = results.get('overall_score', 0)
            
            col_metric1, col_metric2, col_metric3 = st.columns(3)
            with col_metric1:
                st.metric("Total Violations", total_violations)
            with col_metric2:
                st.metric("PII Entities Found", total_pii)
            with col_metric3:
                st.metric("Compliance Score", f"{compliance_score}%")
            
            # Violations by framework
            if total_violations > 0:
                st.subheader("Violations by Framework")
                
                framework_data = []
                for framework in frameworks:
                    violations = results['violations'].get(framework, [])
                    if violations:
                        for violation in violations:
                            framework_data.append({
                                'Framework': framework,
                                'Severity': violation.get('severity', 'Medium'),
                                'Type': violation.get('type', 'Unknown'),
                                'Description': violation.get('description', ''),
                                'Location': violation.get('location', '')
                            })
                
                if framework_data:
                    violations_df = pd.DataFrame(framework_data)
                    
                    # Severity distribution chart
                    severity_counts = violations_df['Severity'].value_counts()
                    fig = px.pie(
                        values=severity_counts.values,
                        names=severity_counts.index,
                        title="Violations by Severity",
                        color_discrete_map={
                            'High': '#ff4444',
                            'Medium': '#ffaa00',
                            'Low': '#44ff44'
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Detailed violations table
                    st.subheader("Detailed Violations")
                    st.dataframe(violations_df, use_container_width=True)
            
            # PII Detection Results
            if include_pii and results.get('pii_entities'):
                st.subheader("PII Detection Results")
                
                pii_data = []
                for entity in results['pii_entities']:
                    pii_data.append({
                        'Entity': entity.get('text', ''),
                        'Type': entity.get('label', ''),
                        'Confidence': f"{entity.get('confidence', 0):.2f}",
                        'Start': entity.get('start', 0),
                        'End': entity.get('end', 0)
                    })
                
                pii_df = pd.DataFrame(pii_data)
                st.dataframe(pii_df, use_container_width=True)
            
            # AI Analysis Insights
            if include_ai_analysis and results.get('ai_insights'):
                st.subheader("AI Analysis Insights")
                insights = results['ai_insights']
                
                if insights.get('summary'):
                    st.write("**Summary:**")
                    st.write(insights['summary'])
                
                if insights.get('recommendations'):
                    st.write("**Recommendations:**")
                    for i, rec in enumerate(insights['recommendations'], 1):
                        st.write(f"{i}. {rec}")
                
                if insights.get('risk_assessment'):
                    st.write("**Risk Assessment:**")
                    risk = insights['risk_assessment']
                    
                    risk_level = risk.get('level', 'Unknown')
                    risk_color = {
                        'Low': 'green',
                        'Medium': 'orange',
                        'High': 'red'
                    }.get(risk_level, 'gray')
                    
                    st.markdown(f"**Risk Level:** :{risk_color}[{risk_level}]")
                    if risk.get('explanation'):
                        st.write(risk['explanation'])
            
            # Export functionality
            st.subheader("Export Report")
            col_export1, col_export2 = st.columns(2)
            
            with col_export1:
                if st.button("📄 Download PDF Report", use_container_width=True):
                    try:
                        report_gen = ReportGenerator()
                        pdf_buffer = report_gen.generate_pdf_report(
                            results, 
                            st.session_state.uploaded_file_name,
                            frameworks
                        )
                        
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_buffer,
                            file_name=f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"Error generating PDF: {str(e)}")
            
            with col_export2:
                if st.button("📊 Download Excel Report", use_container_width=True):
                    try:
                        report_gen = ReportGenerator()
                        excel_buffer = report_gen.generate_excel_report(
                            results,
                            st.session_state.uploaded_file_name,
                            frameworks
                        )
                        
                        st.download_button(
                            label="⬇️ Download Excel",
                            data=excel_buffer,
                            file_name=f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    except Exception as e:
                        st.error(f"Error generating Excel: {str(e)}")
        
        else:
            st.info("Upload and analyze a document to see results here.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**AI-Powered Enterprise Compliance Checker** | "
        "Powered by OpenAI GPT-4o and advanced NLP techniques"
    )

if __name__ == "__main__":
    main()

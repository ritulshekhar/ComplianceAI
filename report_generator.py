import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
import json
from io import BytesIO
import base64

class ReportGenerator:
    """Generate compliance reports in various formats."""
    
    def __init__(self):
        self.report_timestamp = datetime.now()
    
    def generate_pdf_report(self, results: Dict[str, Any], filename: str, 
                          frameworks: List[str]) -> bytes:
        """
        Generate PDF compliance report.
        Note: This is a simplified implementation. In production, you'd use libraries like reportlab.
        """
        try:
            # For this implementation, we'll create a text-based report
            # In production, you would use reportlab or similar for proper PDF generation
            
            report_content = self._generate_text_report(results, filename, frameworks)
            
            # Convert to bytes (in reality, this would be a proper PDF)
            return report_content.encode('utf-8')
            
        except Exception as e:
            raise Exception(f"Error generating PDF report: {str(e)}")
    
    def generate_excel_report(self, results: Dict[str, Any], filename: str,
                            frameworks: List[str]) -> bytes:
        """Generate Excel compliance report with multiple sheets."""
        try:
            buffer = BytesIO()
            
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                # Summary sheet
                summary_data = self._prepare_summary_data(results, filename, frameworks)
                summary_df = pd.DataFrame([summary_data])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Violations sheet
                violations_data = self._prepare_violations_data(results, frameworks)
                if violations_data:
                    violations_df = pd.DataFrame(violations_data)
                    violations_df.to_excel(writer, sheet_name='Violations', index=False)
                
                # PII Detection sheet
                if results.get('pii_entities'):
                    pii_data = self._prepare_pii_data(results['pii_entities'])
                    pii_df = pd.DataFrame(pii_data)
                    pii_df.to_excel(writer, sheet_name='PII_Detection', index=False)
                
                # Recommendations sheet
                if results.get('ai_insights', {}).get('recommendations'):
                    rec_data = self._prepare_recommendations_data(results['ai_insights'])
                    rec_df = pd.DataFrame(rec_data)
                    rec_df.to_excel(writer, sheet_name='Recommendations', index=False)
            
            buffer.seek(0)
            return buffer.getvalue()
            
        except Exception as e:
            raise Exception(f"Error generating Excel report: {str(e)}")
    
    def _generate_text_report(self, results: Dict[str, Any], filename: str,
                            frameworks: List[str]) -> str:
        """Generate a comprehensive text-based report."""
        
        report_lines = []
        
        # Header
        report_lines.extend([
            "=" * 80,
            "AI-POWERED ENTERPRISE COMPLIANCE ANALYSIS REPORT",
            "=" * 80,
            "",
            f"Document: {filename}",
            f"Analysis Date: {self.report_timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Frameworks Analyzed: {', '.join(frameworks)}",
            f"Overall Compliance Score: {results.get('overall_score', 0)}%",
            "",
        ])
        
        # Executive Summary
        report_lines.extend([
            "EXECUTIVE SUMMARY",
            "-" * 50,
            ""
        ])
        
        total_violations = sum(len(results['violations'].get(fw, [])) for fw in frameworks)
        total_pii = len(results.get('pii_entities', []))
        
        report_lines.extend([
            f"Total Violations Detected: {total_violations}",
            f"PII Entities Found: {total_pii}",
            f"Compliance Score: {results.get('overall_score', 0)}%",
            ""
        ])
        
        # Risk Assessment
        if results.get('ai_insights', {}).get('risk_assessment'):
            risk = results['ai_insights']['risk_assessment']
            report_lines.extend([
                "RISK ASSESSMENT",
                "-" * 50,
                f"Risk Level: {risk.get('level', 'Unknown').upper()}",
                f"Explanation: {risk.get('explanation', 'No explanation available')}",
                ""
            ])
        
        # Violations by Framework
        report_lines.extend([
            "VIOLATIONS BY FRAMEWORK",
            "-" * 50,
            ""
        ])
        
        for framework in frameworks:
            violations = results['violations'].get(framework, [])
            report_lines.append(f"{framework}: {len(violations)} violations")
            
            if violations:
                for i, violation in enumerate(violations, 1):
                    report_lines.extend([
                        f"  {i}. {violation.get('type', 'Unknown')} [{violation.get('severity', 'Medium')}]",
                        f"     Description: {violation.get('description', 'No description')}",
                        f"     Location: {violation.get('location', 'Unknown')}",
                        f"     Recommendation: {violation.get('recommendation', 'No recommendation')}",
                        ""
                    ])
            else:
                report_lines.append("     No violations detected")
            
            report_lines.append("")
        
        # PII Detection Results
        if results.get('pii_entities'):
            report_lines.extend([
                "PII DETECTION RESULTS",
                "-" * 50,
                ""
            ])
            
            pii_by_type = {}
            for entity in results['pii_entities']:
                entity_type = entity.get('label', 'Unknown')
                if entity_type not in pii_by_type:
                    pii_by_type[entity_type] = []
                pii_by_type[entity_type].append(entity)
            
            for pii_type, entities in pii_by_type.items():
                report_lines.append(f"{pii_type}: {len(entities)} instances")
                for entity in entities:
                    confidence = entity.get('confidence', 0)
                    report_lines.append(f"  - '{entity.get('text', '')}' (Confidence: {confidence:.2f})")
                report_lines.append("")
        
        # AI Insights
        if results.get('ai_insights'):
            insights = results['ai_insights']
            
            report_lines.extend([
                "AI ANALYSIS INSIGHTS",
                "-" * 50,
                ""
            ])
            
            if insights.get('summary'):
                report_lines.extend([
                    "Summary:",
                    insights['summary'],
                    ""
                ])
            
            if insights.get('recommendations'):
                report_lines.extend([
                    "Recommendations:",
                ])
                for i, rec in enumerate(insights['recommendations'], 1):
                    report_lines.append(f"{i}. {rec}")
                report_lines.append("")
            
            if insights.get('compliance_gaps'):
                report_lines.extend([
                    "Major Compliance Gaps:",
                ])
                for gap in insights['compliance_gaps']:
                    report_lines.append(f"• {gap}")
                report_lines.append("")
            
            if insights.get('strengths'):
                report_lines.extend([
                    "Compliance Strengths:",
                ])
                for strength in insights['strengths']:
                    report_lines.append(f"• {strength}")
                report_lines.append("")
        
        # Footer
        report_lines.extend([
            "=" * 80,
            "End of Report",
            f"Generated by AI-Powered Enterprise Compliance Checker",
            f"Report ID: {self.report_timestamp.strftime('%Y%m%d_%H%M%S')}",
            "=" * 80
        ])
        
        return "\n".join(report_lines)
    
    def _prepare_summary_data(self, results: Dict[str, Any], filename: str,
                            frameworks: List[str]) -> Dict[str, Any]:
        """Prepare summary data for Excel report."""
        total_violations = sum(len(results['violations'].get(fw, [])) for fw in frameworks)
        total_pii = len(results.get('pii_entities', []))
        
        high_severity = sum(
            len([v for v in results['violations'].get(fw, []) if v.get('severity') == 'High'])
            for fw in frameworks
        )
        
        return {
            'Document_Name': filename,
            'Analysis_Date': self.report_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'Frameworks_Analyzed': ', '.join(frameworks),
            'Total_Violations': total_violations,
            'High_Severity_Violations': high_severity,
            'PII_Entities_Found': total_pii,
            'Overall_Compliance_Score': results.get('overall_score', 0),
            'Risk_Level': results.get('ai_insights', {}).get('risk_assessment', {}).get('level', 'Unknown')
        }
    
    def _prepare_violations_data(self, results: Dict[str, Any],
                               frameworks: List[str]) -> List[Dict[str, Any]]:
        """Prepare violations data for Excel report."""
        violations_data = []
        
        for framework in frameworks:
            violations = results['violations'].get(framework, [])
            for violation in violations:
                violations_data.append({
                    'Framework': framework,
                    'Category': violation.get('category', 'Unknown'),
                    'Type': violation.get('type', 'Unknown'),
                    'Severity': violation.get('severity', 'Medium'),
                    'Description': violation.get('description', ''),
                    'Location': violation.get('location', ''),
                    'Matched_Text': violation.get('matched_text', ''),
                    'Recommendation': violation.get('recommendation', ''),
                    'Confidence': violation.get('confidence', '')
                })
        
        return violations_data
    
    def _prepare_pii_data(self, pii_entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prepare PII data for Excel report."""
        pii_data = []
        
        for entity in pii_entities:
            pii_data.append({
                'Entity_Text': entity.get('text', ''),
                'Entity_Type': entity.get('label', ''),
                'Confidence': entity.get('confidence', 0),
                'Start_Position': entity.get('start', 0),
                'End_Position': entity.get('end', 0),
                'Detection_Method': entity.get('detection_method', 'Unknown')
            })
        
        return pii_data
    
    def _prepare_recommendations_data(self, ai_insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prepare recommendations data for Excel report."""
        rec_data = []
        
        recommendations = ai_insights.get('recommendations', [])
        for i, recommendation in enumerate(recommendations, 1):
            rec_data.append({
                'Priority': i,
                'Recommendation': recommendation,
                'Category': 'AI Suggestion'
            })
        
        # Add compliance gaps as high-priority recommendations
        gaps = ai_insights.get('compliance_gaps', [])
        for gap in gaps:
            rec_data.append({
                'Priority': len(recommendations) + 1,
                'Recommendation': f"Address compliance gap: {gap}",
                'Category': 'Critical Gap'
            })
        
        return rec_data
    
    def export_json_report(self, results: Dict[str, Any], filename: str,
                          frameworks: List[str]) -> str:
        """Export results as formatted JSON."""
        export_data = {
            'metadata': {
                'document_name': filename,
                'analysis_timestamp': self.report_timestamp.isoformat(),
                'frameworks_analyzed': frameworks,
                'report_version': '1.0'
            },
            'results': results
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)

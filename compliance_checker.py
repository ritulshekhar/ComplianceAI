import os
import json
from typing import List, Dict, Any
from openai import OpenAI

from pii_detector import PIIDetector
from compliance_frameworks import ComplianceFrameworks
from utils import chunk_text, calculate_compliance_score

class ComplianceChecker:
    def __init__(self, frameworks: List[str] = None, sensitivity: str = "medium", 
                 include_pii: bool = True, include_ai_analysis: bool = True):
        """
        Initialize the compliance checker with specified frameworks and settings.
        
        Args:
            frameworks: List of compliance frameworks to check against
            sensitivity: Detection sensitivity level (high, medium, low)
            include_pii: Whether to include PII detection
            include_ai_analysis: Whether to include AI-powered analysis
        """
        self.frameworks = frameworks or ["GDPR", "SOC2", "HIPAA", "RBI"]
        self.sensitivity = sensitivity
        self.include_pii = include_pii
        self.include_ai_analysis = include_ai_analysis
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "default_key")
        )
        
        # Initialize components
        if self.include_pii:
            self.pii_detector = PIIDetector()
        
        self.compliance_frameworks = ComplianceFrameworks()
        
    def check_api_connection(self) -> bool:
        """Check if OpenAI API is available and working."""
        try:
            # Test with a minimal request
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            return True
        except Exception:
            return False
    
    def analyze_document(self, text_content: str) -> Dict[str, Any]:
        """
        Perform comprehensive compliance analysis on document text.
        
        Args:
            text_content: The text content of the document to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        results = {
            'violations': {},
            'pii_entities': [],
            'ai_insights': {},
            'overall_score': 0,
            'analysis_timestamp': None
        }
        
        try:
            # 1. Rule-based compliance checking
            for framework in self.frameworks:
                violations = self._check_framework_compliance(text_content, framework)
                results['violations'][framework] = violations
            
            # 2. PII Detection
            if self.include_pii:
                results['pii_entities'] = self.pii_detector.detect_pii(text_content)
            
            # 3. AI-powered analysis
            if self.include_ai_analysis:
                results['ai_insights'] = self._perform_ai_analysis(text_content, results['violations'])
            
            # 4. Calculate overall compliance score
            results['overall_score'] = calculate_compliance_score(results)
            
            # 5. Set timestamp
            from datetime import datetime
            results['analysis_timestamp'] = datetime.now().isoformat()
            
        except Exception as e:
            raise Exception(f"Error during compliance analysis: {str(e)}")
        
        return results
    
    def _check_framework_compliance(self, text: str, framework: str) -> List[Dict[str, Any]]:
        """
        Check compliance against a specific framework using rule-based detection.
        
        Args:
            text: Document text to analyze
            framework: Compliance framework to check against
            
        Returns:
            List of detected violations
        """
        violations = []
        
        try:
            # Get framework-specific rules
            framework_rules = self.compliance_frameworks.get_framework_rules(framework)
            
            # Check each rule category
            for category, rules in framework_rules.items():
                category_violations = self._check_rule_category(text, category, rules, framework)
                violations.extend(category_violations)
            
            # AI-enhanced violation detection for context-aware analysis
            if self.include_ai_analysis:
                ai_violations = self._ai_enhanced_framework_check(text, framework)
                violations.extend(ai_violations)
                
        except Exception as e:
            print(f"Error checking {framework} compliance: {str(e)}")
        
        return violations
    
    def _check_rule_category(self, text: str, category: str, rules: Dict, framework: str) -> List[Dict[str, Any]]:
        """Check specific rule category against text."""
        violations = []
        
        # Pattern-based detection
        patterns = rules.get('patterns', [])
        for pattern in patterns:
            matches = self.compliance_frameworks.find_pattern_matches(text, pattern)
            for match in matches:
                violation = {
                    'framework': framework,
                    'category': category,
                    'type': pattern.get('type', 'Pattern Match'),
                    'description': pattern.get('description', 'Pattern violation detected'),
                    'severity': self._determine_severity(pattern.get('severity', 'medium')),
                    'location': f"Position {match['start']}-{match['end']}",
                    'matched_text': match['text'],
                    'recommendation': pattern.get('recommendation', 'Review and update content')
                }
                violations.append(violation)
        
        # Keyword-based detection
        keywords = rules.get('required_keywords', [])
        missing_keywords = []
        for keyword_group in keywords:
            if not self.compliance_frameworks.check_keyword_presence(text, keyword_group):
                missing_keywords.append(keyword_group)
        
        if missing_keywords:
            violation = {
                'framework': framework,
                'category': category,
                'type': 'Missing Required Content',
                'description': f'Missing required keywords/phrases: {", ".join(missing_keywords)}',
                'severity': 'Medium',
                'location': 'Document-wide',
                'matched_text': '',
                'recommendation': 'Add required compliance statements and disclosures'
            }
            violations.append(violation)
        
        return violations
    
    def _ai_enhanced_framework_check(self, text: str, framework: str) -> List[Dict[str, Any]]:
        """Use AI to detect context-aware compliance violations."""
        violations = []
        
        try:
            # Chunk text for processing
            chunks = chunk_text(text, max_length=3000)
            
            for i, chunk in enumerate(chunks):
                chunk_violations = self._analyze_chunk_with_ai(chunk, framework, i)
                violations.extend(chunk_violations)
                
        except Exception as e:
            print(f"Error in AI-enhanced {framework} checking: {str(e)}")
        
        return violations
    
    def _analyze_chunk_with_ai(self, chunk: str, framework: str, chunk_index: int) -> List[Dict[str, Any]]:
        """Analyze a text chunk using AI for compliance violations."""
        try:
            prompt = self._build_compliance_prompt(chunk, framework)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert compliance auditor specializing in regulatory frameworks. "
                                 "Analyze text for compliance violations and respond with structured JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            ai_result = json.loads(response.choices[0].message.content)
            violations = []
            
            for violation in ai_result.get('violations', []):
                violations.append({
                    'framework': framework,
                    'category': violation.get('category', 'AI Detection'),
                    'type': violation.get('type', 'AI-Detected Violation'),
                    'description': violation.get('description', ''),
                    'severity': self._determine_severity(violation.get('severity', 'medium')),
                    'location': f"Chunk {chunk_index + 1}",
                    'matched_text': violation.get('matched_text', ''),
                    'recommendation': violation.get('recommendation', ''),
                    'confidence': violation.get('confidence', 0.8)
                })
            
            return violations
            
        except Exception as e:
            print(f"Error in AI chunk analysis: {str(e)}")
            return []
    
    def _build_compliance_prompt(self, text: str, framework: str) -> str:
        """Build AI prompt for compliance checking."""
        framework_descriptions = {
            'GDPR': 'EU General Data Protection Regulation - focus on data protection, consent, privacy rights, data processing lawfulness',
            'SOC2': 'SOC 2 Type II compliance - focus on security, availability, processing integrity, confidentiality, privacy controls',
            'HIPAA': 'Health Insurance Portability and Accountability Act - focus on protected health information (PHI) privacy and security',
            'RBI': 'Reserve Bank of India guidelines - focus on financial data protection, KYC requirements, cybersecurity frameworks'
        }
        
        description = framework_descriptions.get(framework, f'{framework} compliance requirements')
        
        return f"""
Analyze the following text for {framework} compliance violations.

Framework: {framework}
Description: {description}

Text to analyze:
{text}

Please identify any compliance violations and respond with JSON in this format:
{{
    "violations": [
        {{
            "category": "category_name",
            "type": "violation_type",
            "description": "detailed_description",
            "severity": "high|medium|low",
            "matched_text": "relevant_text_excerpt",
            "recommendation": "remediation_suggestion",
            "confidence": 0.95
        }}
    ]
}}

Focus on:
- Missing required disclosures or statements
- Improper data handling descriptions
- Non-compliant language or terms
- Missing consent mechanisms
- Inadequate security measure descriptions
- Regulatory requirement gaps

Return empty violations array if no violations found.
"""
    
    def _perform_ai_analysis(self, text: str, violations: Dict[str, List]) -> Dict[str, Any]:
        """Perform comprehensive AI analysis of the document and violations."""
        try:
            # Prepare violations summary for AI context
            violation_summary = self._prepare_violation_summary(violations)
            
            prompt = f"""
Analyze this document for enterprise compliance and provide comprehensive insights.

Document Text (first 2000 characters):
{text[:2000]}...

Detected Violations Summary:
{violation_summary}

Please provide a comprehensive analysis in JSON format:
{{
    "summary": "executive summary of compliance status",
    "risk_assessment": {{
        "level": "high|medium|low",
        "explanation": "detailed risk explanation"
    }},
    "recommendations": ["list", "of", "actionable", "recommendations"],
    "compliance_gaps": ["list", "of", "major", "gaps"],
    "strengths": ["list", "of", "compliance", "strengths"]
}}
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior compliance consultant with expertise in GDPR, SOC2, HIPAA, and RBI regulations. "
                                 "Provide actionable insights for enterprise compliance improvement."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.2
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error in AI analysis: {str(e)}")
            return {
                "summary": "AI analysis unavailable",
                "risk_assessment": {"level": "unknown", "explanation": "Analysis failed"},
                "recommendations": ["Review document manually for compliance"],
                "compliance_gaps": [],
                "strengths": []
            }
    
    def _prepare_violation_summary(self, violations: Dict[str, List]) -> str:
        """Prepare a summary of violations for AI context."""
        summary_parts = []
        
        for framework, framework_violations in violations.items():
            if framework_violations:
                violation_count = len(framework_violations)
                high_severity = len([v for v in framework_violations if v.get('severity') == 'High'])
                summary_parts.append(f"{framework}: {violation_count} violations ({high_severity} high severity)")
        
        return "; ".join(summary_parts) if summary_parts else "No violations detected"
    
    def _determine_severity(self, severity_input: str) -> str:
        """Normalize severity levels."""
        severity_map = {
            'high': 'High',
            'medium': 'Medium', 
            'low': 'Low',
            'critical': 'High',
            'warning': 'Medium',
            'info': 'Low'
        }
        
        return severity_map.get(severity_input.lower(), 'Medium')

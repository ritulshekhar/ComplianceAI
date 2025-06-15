import re
from typing import Dict, List, Any

class ComplianceFrameworks:
    """Define compliance rules and patterns for different regulatory frameworks."""
    
    def __init__(self):
        self.frameworks = {
            'GDPR': self._define_gdpr_rules(),
            'SOC2': self._define_soc2_rules(),
            'HIPAA': self._define_hipaa_rules(),
            'RBI': self._define_rbi_rules()
        }
    
    def get_framework_rules(self, framework: str) -> Dict[str, Any]:
        """Get rules for a specific compliance framework."""
        return self.frameworks.get(framework, {})
    
    def _define_gdpr_rules(self) -> Dict[str, Any]:
        """Define GDPR compliance rules and patterns."""
        return {
            'data_protection': {
                'required_keywords': [
                    ['data protection', 'personal data'],
                    ['lawful basis', 'legitimate interest', 'consent'],
                    ['data subject rights', 'right to erasure', 'right to rectification']
                ],
                'patterns': [
                    {
                        'type': 'Missing Consent Mechanism',
                        'pattern': r'(?i)collect.*personal.*data(?!.*consent)',
                        'description': 'Personal data collection mentioned without consent mechanism',
                        'severity': 'high',
                        'recommendation': 'Add clear consent mechanism for personal data collection'
                    },
                    {
                        'type': 'Vague Data Processing Purpose',
                        'pattern': r'(?i)process.*data.*for.*business.*purposes?(?!.*specific)',
                        'description': 'Data processing purpose is too vague',
                        'severity': 'medium',
                        'recommendation': 'Specify exact purposes for data processing'
                    },
                    {
                        'type': 'Missing Data Retention Policy',
                        'pattern': r'(?i)retain.*data(?!.*(period|time|duration))',
                        'description': 'Data retention mentioned without specific timeframe',
                        'severity': 'medium',
                        'recommendation': 'Specify data retention periods'
                    }
                ]
            },
            'privacy_rights': {
                'required_keywords': [
                    ['right to access', 'data portability'],
                    ['data protection officer', 'DPO'],
                    ['privacy by design', 'privacy by default']
                ],
                'patterns': [
                    {
                        'type': 'Missing Subject Rights',
                        'pattern': r'(?i)personal.*data(?!.*(right to access|right to erasure|right to rectification))',
                        'description': 'Personal data mentioned without subject rights',
                        'severity': 'high',
                        'recommendation': 'Include comprehensive data subject rights information'
                    }
                ]
            },
            'international_transfers': {
                'required_keywords': [
                    ['adequate protection', 'standard contractual clauses'],
                    ['third country', 'international transfer']
                ],
                'patterns': [
                    {
                        'type': 'Unprotected International Transfer',
                        'pattern': r'(?i)(transfer|share|send).*data.*(outside|abroad|international)(?!.*(adequate|protection|safeguards))',
                        'description': 'International data transfer without adequate protection',
                        'severity': 'high',
                        'recommendation': 'Implement adequate safeguards for international transfers'
                    }
                ]
            }
        }
    
    def _define_soc2_rules(self) -> Dict[str, Any]:
        """Define SOC 2 compliance rules and patterns."""
        return {
            'security': {
                'required_keywords': [
                    ['access controls', 'authentication'],
                    ['encryption', 'data encryption'],
                    ['vulnerability management', 'security monitoring']
                ],
                'patterns': [
                    {
                        'type': 'Weak Access Control',
                        'pattern': r'(?i)access.*system(?!.*(authentication|authorization|multi-factor))',
                        'description': 'System access mentioned without proper controls',
                        'severity': 'high',
                        'recommendation': 'Implement strong authentication and authorization controls'
                    },
                    {
                        'type': 'Unencrypted Data Storage',
                        'pattern': r'(?i)store.*data(?!.*encrypt)',
                        'description': 'Data storage mentioned without encryption',
                        'severity': 'high',
                        'recommendation': 'Implement encryption for data at rest'
                    }
                ]
            },
            'availability': {
                'required_keywords': [
                    ['backup', 'disaster recovery'],
                    ['business continuity', 'redundancy'],
                    ['uptime', 'service level agreement']
                ],
                'patterns': [
                    {
                        'type': 'Missing Backup Strategy',
                        'pattern': r'(?i)critical.*data(?!.*(backup|recovery))',
                        'description': 'Critical data mentioned without backup strategy',
                        'severity': 'medium',
                        'recommendation': 'Implement comprehensive backup and recovery procedures'
                    }
                ]
            },
            'processing_integrity': {
                'required_keywords': [
                    ['data validation', 'input validation'],
                    ['error handling', 'exception handling'],
                    ['audit trail', 'logging']
                ],
                'patterns': [
                    {
                        'type': 'Missing Input Validation',
                        'pattern': r'(?i)user.*input(?!.*(validat|sanitiz|check))',
                        'description': 'User input processing without validation',
                        'severity': 'high',
                        'recommendation': 'Implement comprehensive input validation'
                    }
                ]
            }
        }
    
    def _define_hipaa_rules(self) -> Dict[str, Any]:
        """Define HIPAA compliance rules and patterns."""
        return {
            'protected_health_information': {
                'required_keywords': [
                    ['protected health information', 'PHI'],
                    ['covered entity', 'business associate'],
                    ['minimum necessary', 'administrative safeguards']
                ],
                'patterns': [
                    {
                        'type': 'Unsecured PHI',
                        'pattern': r'(?i)(health.*information|medical.*record|PHI)(?!.*(encrypt|secure|protect))',
                        'description': 'Health information mentioned without security measures',
                        'severity': 'high',
                        'recommendation': 'Implement encryption and access controls for PHI'
                    },
                    {
                        'type': 'Missing Business Associate Agreement',
                        'pattern': r'(?i)(share|disclose|provide).*health.*information.*vendor(?!.*agreement)',
                        'description': 'PHI sharing with vendors without BAA',
                        'severity': 'high',
                        'recommendation': 'Ensure Business Associate Agreements are in place'
                    }
                ]
            },
            'access_controls': {
                'required_keywords': [
                    ['role-based access', 'access controls'],
                    ['audit logs', 'access monitoring'],
                    ['user authentication', 'password policy']
                ],
                'patterns': [
                    {
                        'type': 'Weak PHI Access Control',
                        'pattern': r'(?i)access.*PHI(?!.*(role|permission|authorization))',
                        'description': 'PHI access without proper role-based controls',
                        'severity': 'high',
                        'recommendation': 'Implement role-based access controls for PHI'
                    }
                ]
            },
            'breach_notification': {
                'required_keywords': [
                    ['breach notification', 'incident response'],
                    ['72 hours', 'breach assessment'],
                    ['HHS notification', 'patient notification']
                ],
                'patterns': [
                    {
                        'type': 'Missing Breach Procedures',
                        'pattern': r'(?i)security.*incident(?!.*(notification|report|procedure))',
                        'description': 'Security incidents mentioned without notification procedures',
                        'severity': 'medium',
                        'recommendation': 'Establish clear breach notification procedures'
                    }
                ]
            }
        }
    
    def _define_rbi_rules(self) -> Dict[str, Any]:
        """Define RBI (Reserve Bank of India) compliance rules and patterns."""
        return {
            'data_localization': {
                'required_keywords': [
                    ['data localization', 'India storage'],
                    ['payment data', 'financial data'],
                    ['local storage', 'domestic storage']
                ],
                'patterns': [
                    {
                        'type': 'Non-compliant Data Storage',
                        'pattern': r'(?i)(payment|financial).*data.*stor.*(?!.*India)',
                        'description': 'Payment/financial data storage location not specified as India',
                        'severity': 'high',
                        'recommendation': 'Ensure payment and financial data is stored within India'
                    },
                    {
                        'type': 'Cross-border Data Transfer',
                        'pattern': r'(?i)(transfer|send).*payment.*data.*(overseas|abroad|foreign)',
                        'description': 'Cross-border transfer of payment data',
                        'severity': 'high',
                        'recommendation': 'Comply with RBI data localization requirements'
                    }
                ]
            },
            'cybersecurity': {
                'required_keywords': [
                    ['cybersecurity framework', 'cyber resilience'],
                    ['incident response', 'cyber incident'],
                    ['risk assessment', 'vulnerability assessment']
                ],
                'patterns': [
                    {
                        'type': 'Missing Cybersecurity Framework',
                        'pattern': r'(?i)financial.*system(?!.*(cybersecurity|security.*framework))',
                        'description': 'Financial systems without cybersecurity framework',
                        'severity': 'high',
                        'recommendation': 'Implement comprehensive cybersecurity framework as per RBI guidelines'
                    }
                ]
            },
            'kyc_aml': {
                'required_keywords': [
                    ['know your customer', 'KYC'],
                    ['anti-money laundering', 'AML'],
                    ['customer due diligence', 'CDD']
                ],
                'patterns': [
                    {
                        'type': 'Inadequate KYC Process',
                        'pattern': r'(?i)customer.*onboard(?!.*(KYC|identity.*verification|due.*diligence))',
                        'description': 'Customer onboarding without proper KYC procedures',
                        'severity': 'high',
                        'recommendation': 'Implement comprehensive KYC and AML procedures'
                    }
                ]
            }
        }
    
    def find_pattern_matches(self, text: str, pattern_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find all matches for a specific pattern in text."""
        matches = []
        pattern = pattern_info['pattern']
        
        try:
            for match in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
                matches.append({
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'context': self._get_context(text, match.start(), match.end())
                })
        except re.error as e:
            print(f"Regex error for pattern {pattern}: {str(e)}")
        
        return matches
    
    def check_keyword_presence(self, text: str, keywords: List[str]) -> bool:
        """Check if any of the required keywords are present in text."""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)
    
    def _get_context(self, text: str, start: int, end: int, context_length: int = 100) -> str:
        """Get surrounding context for a match."""
        context_start = max(0, start - context_length)
        context_end = min(len(text), end + context_length)
        
        context = text[context_start:context_end]
        
        # Add ellipsis if context is truncated
        if context_start > 0:
            context = "..." + context
        if context_end < len(text):
            context = context + "..."
        
        return context.strip()
    
    def get_framework_description(self, framework: str) -> str:
        """Get description of a compliance framework."""
        descriptions = {
            'GDPR': 'EU General Data Protection Regulation - Comprehensive data protection and privacy regulation',
            'SOC2': 'SOC 2 Type II - Security, availability, processing integrity, confidentiality, and privacy controls',
            'HIPAA': 'Health Insurance Portability and Accountability Act - Healthcare data privacy and security',
            'RBI': 'Reserve Bank of India Guidelines - Financial sector cybersecurity and data protection'
        }
        return descriptions.get(framework, f'{framework} compliance framework')
    
    def get_severity_color(self, severity: str) -> str:
        """Get color code for severity level."""
        colors = {
            'high': '#ff4444',
            'medium': '#ffaa00',
            'low': '#44ff44'
        }
        return colors.get(severity.lower(), '#cccccc')

import spacy
import re
from typing import List, Dict, Any
import os

class PIIDetector:
    """Detect Personally Identifiable Information using NLP and pattern matching."""
    
    def __init__(self):
        self.nlp = self._load_spacy_model()
        self.custom_patterns = self._initialize_custom_patterns()
    
    def _load_spacy_model(self):
        """Load spaCy model with fallback options."""
        models_to_try = ['en_core_web_sm', 'en_core_web_md', 'en_core_web_lg']
        
        for model_name in models_to_try:
            try:
                return spacy.load(model_name)
            except OSError:
                continue
        
        # If no model is available, create a blank model with just the tokenizer
        print("Warning: No spaCy model found. PII detection will use pattern matching only.")
        return spacy.blank('en')
    
    def _initialize_custom_patterns(self) -> Dict[str, List[Dict]]:
        """Initialize custom regex patterns for PII detection."""
        return {
            'email': [
                {
                    'pattern': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                    'confidence': 0.95
                }
            ],
            'phone': [
                {
                    'pattern': r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
                    'confidence': 0.85
                },
                {
                    'pattern': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                    'confidence': 0.80
                }
            ],
            'ssn': [
                {
                    'pattern': r'\b\d{3}-\d{2}-\d{4}\b',
                    'confidence': 0.95
                },
                {
                    'pattern': r'\b\d{9}\b',
                    'confidence': 0.60  # Lower confidence as 9 digits could be many things
                }
            ],
            'credit_card': [
                {
                    'pattern': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
                    'confidence': 0.80
                }
            ],
            'ip_address': [
                {
                    'pattern': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
                    'confidence': 0.75
                }
            ],
            'driver_license': [
                {
                    'pattern': r'\b[A-Z]{1,2}\d{6,8}\b',
                    'confidence': 0.70
                }
            ],
            'passport': [
                {
                    'pattern': r'\b[A-Z]{2}\d{7}\b',
                    'confidence': 0.75
                }
            ],
            'bank_account': [
                {
                    'pattern': r'\b\d{8,17}\b',
                    'confidence': 0.50  # Very low confidence as many number sequences could match
                }
            ],
            'date_of_birth': [
                {
                    'pattern': r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4})|(?:\d{2,4}[/-]\d{1,2}[/-]\d{1,2})\b',
                    'confidence': 0.65
                }
            ]
        }
    
    def detect_pii(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect PII entities in text using both NER and pattern matching.
        
        Args:
            text: Text content to analyze
            
        Returns:
            List of detected PII entities with metadata
        """
        pii_entities = []
        
        # 1. Use spaCy NER if model is available
        if self.nlp.has_pipe('ner'):
            ner_entities = self._detect_with_ner(text)
            pii_entities.extend(ner_entities)
        
        # 2. Use custom pattern matching
        pattern_entities = self._detect_with_patterns(text)
        pii_entities.extend(pattern_entities)
        
        # 3. Remove duplicates and merge overlapping entities
        pii_entities = self._deduplicate_entities(pii_entities)
        
        # 4. Sort by position in text
        pii_entities.sort(key=lambda x: x['start'])
        
        return pii_entities
    
    def _detect_with_ner(self, text: str) -> List[Dict[str, Any]]:
        """Detect PII using spaCy Named Entity Recognition."""
        entities = []
        
        try:
            doc = self.nlp(text)
            
            for ent in doc.ents:
                if self._is_pii_entity(ent.label_):
                    entities.append({
                        'text': ent.text,
                        'label': self._normalize_entity_label(ent.label_),
                        'start': ent.start_char,
                        'end': ent.end_char,
                        'confidence': 0.85,  # Default confidence for NER
                        'detection_method': 'NER'
                    })
        
        except Exception as e:
            print(f"Error in NER detection: {str(e)}")
        
        return entities
    
    def _detect_with_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Detect PII using regex patterns."""
        entities = []
        
        for pii_type, patterns in self.custom_patterns.items():
            for pattern_info in patterns:
                pattern = pattern_info['pattern']
                confidence = pattern_info['confidence']
                
                matches = re.finditer(pattern, text, re.IGNORECASE)
                
                for match in matches:
                    # Additional validation for certain PII types
                    if self._validate_pattern_match(pii_type, match.group()):
                        entities.append({
                            'text': match.group(),
                            'label': pii_type.upper(),
                            'start': match.start(),
                            'end': match.end(),
                            'confidence': confidence,
                            'detection_method': 'Pattern'
                        })
        
        return entities
    
    def _is_pii_entity(self, label: str) -> bool:
        """Check if entity label represents PII."""
        pii_labels = {
            'PERSON', 'ORG', 'GPE',  # People, organizations, locations
            'DATE', 'TIME',          # Dates and times
            'MONEY', 'PERCENT',      # Financial information
            'CARDINAL', 'ORDINAL'    # Numbers (could be IDs)
        }
        return label in pii_labels
    
    def _normalize_entity_label(self, label: str) -> str:
        """Normalize entity labels to standard PII categories."""
        label_mapping = {
            'PERSON': 'PERSON_NAME',
            'ORG': 'ORGANIZATION',
            'GPE': 'LOCATION',
            'DATE': 'DATE',
            'TIME': 'TIME',
            'MONEY': 'FINANCIAL',
            'PERCENT': 'FINANCIAL',
            'CARDINAL': 'NUMBER',
            'ORDINAL': 'NUMBER'
        }
        return label_mapping.get(label, label)
    
    def _validate_pattern_match(self, pii_type: str, matched_text: str) -> bool:
        """Additional validation for pattern matches to reduce false positives."""
        
        if pii_type == 'ssn':
            # Validate SSN format and check for obviously fake numbers
            if matched_text.replace('-', '') in ['000000000', '111111111', '123456789']:
                return False
            
        elif pii_type == 'credit_card':
            # Basic Luhn algorithm check for credit cards
            return self._luhn_check(matched_text.replace('-', '').replace(' ', ''))
            
        elif pii_type == 'ip_address':
            # Validate IP address ranges
            parts = matched_text.split('.')
            try:
                return all(0 <= int(part) <= 255 for part in parts)
            except ValueError:
                return False
                
        elif pii_type == 'phone':
            # Check for obviously fake numbers
            clean_number = re.sub(r'[^\d]', '', matched_text)
            if len(set(clean_number)) <= 2:  # All same digits or alternating
                return False
                
        return True
    
    def _luhn_check(self, card_number: str) -> bool:
        """Validate credit card number using Luhn algorithm."""
        if not card_number.isdigit():
            return False
            
        digits = [int(d) for d in card_number]
        checksum = 0
        
        # Double every second digit from right to left
        for i in range(len(digits) - 2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        
        return sum(digits) % 10 == 0
    
    def _deduplicate_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate and overlapping entities."""
        if not entities:
            return entities
        
        # Sort by start position
        entities.sort(key=lambda x: (x['start'], x['end']))
        
        deduplicated = []
        
        for entity in entities:
            # Check for overlap with existing entities
            overlaps = False
            
            for existing in deduplicated:
                if (entity['start'] < existing['end'] and 
                    entity['end'] > existing['start']):
                    # There's an overlap - keep the one with higher confidence
                    if entity['confidence'] > existing['confidence']:
                        deduplicated.remove(existing)
                        break
                    else:
                        overlaps = True
                        break
            
            if not overlaps:
                deduplicated.append(entity)
        
        return deduplicated
    
    def get_pii_summary(self, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics for detected PII."""
        if not entities:
            return {
                'total_entities': 0,
                'types_found': [],
                'high_confidence_count': 0,
                'risk_level': 'Low'
            }
        
        type_counts = {}
        high_confidence_count = 0
        
        for entity in entities:
            entity_type = entity['label']
            type_counts[entity_type] = type_counts.get(entity_type, 0) + 1
            
            if entity['confidence'] >= 0.8:
                high_confidence_count += 1
        
        # Determine risk level
        total_entities = len(entities)
        if total_entities >= 10 or high_confidence_count >= 5:
            risk_level = 'High'
        elif total_entities >= 5 or high_confidence_count >= 2:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        return {
            'total_entities': total_entities,
            'types_found': list(type_counts.keys()),
            'type_counts': type_counts,
            'high_confidence_count': high_confidence_count,
            'risk_level': risk_level
        }

import re
from typing import List, Dict, Any
import math

def chunk_text(text: str, max_length: int = 3000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks for processing.
    
    Args:
        text: Text to chunk
        max_length: Maximum length of each chunk
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + max_length
        
        # If this isn't the last chunk, try to break at a sentence or word boundary
        if end < len(text):
            # Look for sentence boundary
            sentence_end = text.rfind('.', start, end)
            if sentence_end > start + max_length // 2:
                end = sentence_end + 1
            else:
                # Look for word boundary
                word_end = text.rfind(' ', start, end)
                if word_end > start + max_length // 2:
                    end = word_end
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start position with overlap
        start = max(start + max_length - overlap, end)
        
        if start >= len(text):
            break
    
    return chunks

def calculate_compliance_score(results: Dict[str, Any]) -> int:
    """
    Calculate overall compliance score based on violations and other factors.
    
    Args:
        results: Analysis results dictionary
        
    Returns:
        Compliance score from 0-100
    """
    base_score = 100
    
    # Deduct points for violations
    for framework, violations in results.get('violations', {}).items():
        for violation in violations:
            severity = violation.get('severity', 'Medium').lower()
            
            if severity == 'high':
                base_score -= 15
            elif severity == 'medium':
                base_score -= 8
            elif severity == 'low':
                base_score -= 3
    
    # Deduct points for PII entities (data exposure risk)
    pii_entities = results.get('pii_entities', [])
    high_risk_pii = ['SSN', 'CREDIT_CARD', 'PASSPORT', 'DRIVER_LICENSE']
    
    for entity in pii_entities:
        entity_type = entity.get('label', '').upper()
        confidence = entity.get('confidence', 0)
        
        if entity_type in high_risk_pii and confidence > 0.8:
            base_score -= 10
        elif confidence > 0.7:
            base_score -= 5
        else:
            base_score -= 2
    
    # Factor in AI risk assessment if available
    ai_insights = results.get('ai_insights', {})
    risk_assessment = ai_insights.get('risk_assessment', {})
    risk_level = risk_assessment.get('level', '').lower()
    
    if risk_level == 'high':
        base_score = min(base_score, 60)  # Cap at 60 for high risk
    elif risk_level == 'medium':
        base_score = min(base_score, 80)  # Cap at 80 for medium risk
    
    # Ensure score is within valid range
    return max(0, min(100, base_score))

def extract_contact_info(text: str) -> Dict[str, List[str]]:
    """
    Extract contact information from text.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with contact information types and found instances
    """
    contact_info = {
        'emails': [],
        'phones': [],
        'addresses': []
    }
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    contact_info['emails'] = re.findall(email_pattern, text)
    
    # Phone pattern
    phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    contact_info['phones'] = re.findall(phone_pattern, text)
    
    # Simple address pattern (very basic)
    address_pattern = r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Lane|Ln|Drive|Dr|Boulevard|Blvd)\b'
    contact_info['addresses'] = re.findall(address_pattern, text, re.IGNORECASE)
    
    return contact_info

def normalize_text(text: str) -> str:
    """
    Normalize text for consistent processing.
    
    Args:
        text: Text to normalize
        
    Returns:
        Normalized text
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Normalize quotes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    
    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    
    return text.strip()

def extract_dates(text: str) -> List[str]:
    """
    Extract date patterns from text.
    
    Args:
        text: Text to analyze
        
    Returns:
        List of found date strings
    """
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or DD/MM/YYYY
        r'\b\d{2,4}[/-]\d{1,2}[/-]\d{1,2}\b',  # YYYY/MM/DD
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4}\b',  # Month DD, YYYY
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}\b'  # DD Month YYYY
    ]
    
    dates = []
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        dates.extend(matches)
    
    return list(set(dates))  # Remove duplicates

def calculate_text_complexity(text: str) -> Dict[str, float]:
    """
    Calculate text complexity metrics.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with complexity metrics
    """
    if not text:
        return {'readability_score': 0, 'avg_sentence_length': 0, 'avg_word_length': 0}
    
    # Basic text statistics
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    words = text.split()
    word_count = len(words)
    sentence_count = len(sentences)
    
    if sentence_count == 0:
        return {'readability_score': 0, 'avg_sentence_length': 0, 'avg_word_length': 0}
    
    # Average sentence length
    avg_sentence_length = word_count / sentence_count
    
    # Average word length
    total_chars = sum(len(word) for word in words)
    avg_word_length = total_chars / word_count if word_count > 0 else 0
    
    # Simple readability score (Flesch-like)
    # Higher score = easier to read
    readability_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * (avg_word_length / 5))
    readability_score = max(0, min(100, readability_score))
    
    return {
        'readability_score': round(readability_score, 2),
        'avg_sentence_length': round(avg_sentence_length, 2),
        'avg_word_length': round(avg_word_length, 2)
    }

def highlight_text(text: str, highlights: List[Dict[str, int]], 
                  highlight_class: str = 'highlight') -> str:
    """
    Add HTML highlighting to text based on position ranges.
    
    Args:
        text: Original text
        highlights: List of dicts with 'start' and 'end' positions
        highlight_class: CSS class for highlighting
        
    Returns:
        HTML string with highlighted text
    """
    if not highlights:
        return text
    
    # Sort highlights by start position (reverse order for easier insertion)
    highlights = sorted(highlights, key=lambda x: x['start'], reverse=True)
    
    highlighted_text = text
    
    for highlight in highlights:
        start = highlight['start']
        end = highlight['end']
        
        if 0 <= start < end <= len(highlighted_text):
            before = highlighted_text[:start]
            highlighted = highlighted_text[start:end]
            after = highlighted_text[end:]
            
            highlighted_text = f"{before}<span class='{highlight_class}'>{highlighted}</span>{after}"
    
    return highlighted_text

def format_confidence_score(confidence: float) -> str:
    """
    Format confidence score as percentage string.
    
    Args:
        confidence: Confidence value between 0 and 1
        
    Returns:
        Formatted percentage string
    """
    if confidence is None:
        return "N/A"
    
    percentage = confidence * 100
    return f"{percentage:.1f}%"

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe file operations.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        max_name_length = 255 - len(ext) - 1 if ext else 255
        filename = name[:max_name_length] + ('.' + ext if ext else '')
    
    return filename

def get_severity_emoji(severity: str) -> str:
    """
    Get emoji representation for severity level.
    
    Args:
        severity: Severity level string
        
    Returns:
        Appropriate emoji
    """
    emoji_map = {
        'high': '🔴',
        'medium': '🟡', 
        'low': '🟢',
        'critical': '🔴',
        'warning': '🟡',
        'info': '🔵'
    }
    
    return emoji_map.get(severity.lower(), '⚪')

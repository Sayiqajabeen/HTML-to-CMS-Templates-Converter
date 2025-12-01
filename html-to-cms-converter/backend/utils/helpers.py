import re
from typing import Dict, List

def clean_html(html_string: str) -> str:
    """Remove excessive whitespace from HTML"""
    html_string = re.sub(r'\s+', ' ', html_string)
    return html_string.strip()

def extract_inline_styles(html_string: str) -> Dict[str, str]:
    """Extract inline CSS styles from HTML"""
    styles = {}
    style_pattern = r'style=["\']([^"\']*)["\']'
    matches = re.findall(style_pattern, html_string)
    
    for match in matches:
        properties = match.split(';')
        for prop in properties:
            if ':' in prop:
                key, value = prop.split(':', 1)
                styles[key.strip()] = value.strip()
    
    return styles

def detect_framework(html_string: str) -> str:
    """Detect if HTML uses Bootstrap, Tailwind, or other frameworks"""
    html_lower = html_string.lower()
    
    if 'bootstrap' in html_lower or 'btn-primary' in html_lower:
        return 'bootstrap'
    elif 'tailwind' in html_lower:
        return 'tailwind'
    elif 'material' in html_lower or 'mui' in html_lower:
        return 'material-ui'
    
    return 'custom'

def sanitize_filename(name: str) -> str:
    """Sanitize string for use as filename"""
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name)
    return name.lower()
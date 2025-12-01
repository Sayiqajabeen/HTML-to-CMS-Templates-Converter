# ============================================
# FILE: backend/services/css_parser.py
# CSS Parser for extracting colors, fonts, and layout
# ============================================

import re
from typing import Dict, List

class CSSParser:
    """Parse and analyze CSS to extract styling information for CMS"""
    
    def __init__(self, css_content):
        self.css_content = css_content
        self.parsed_rules = {}
        self.color_scheme = {}
        self.typography = {}
        self.layout_info = {}
    
    def parse(self):
        """Parse CSS and extract all relevant information"""
        self._parse_css_rules()
        self._extract_color_scheme()
        self._extract_typography()
        self._extract_layout()
        
        return {
            'rules': self.parsed_rules,
            'color_scheme': self.color_scheme,
            'typography': self.typography,
            'layout': self.layout_info
        }
    
    def _parse_css_rules(self):
        """Parse CSS into structured rules"""
        # Remove comments
        css_clean = re.sub(r'/\*.*?\*/', '', self.css_content, flags=re.DOTALL)
        
        # Extract CSS rules using regex
        rule_pattern = r'([^{]+)\{([^}]+)\}'
        matches = re.findall(rule_pattern, css_clean)
        
        for selector, declarations in matches:
            selector = selector.strip()
            properties = {}
            
            # Parse declarations
            for declaration in declarations.split(';'):
                if ':' in declaration:
                    prop, value = declaration.split(':', 1)
                    properties[prop.strip()] = value.strip()
            
            if properties:
                self.parsed_rules[selector] = properties
    
    def _extract_color_scheme(self):
        """Extract color palette from CSS"""
        colors = set()
        
        for selector, properties in self.parsed_rules.items():
            for prop, value in properties.items():
                if any(p in prop for p in ['color', 'background', 'border', 'fill']):
                    # Extract hex colors
                    hex_colors = re.findall(r'#[0-9a-fA-F]{3,6}', value)
                    colors.update(hex_colors)
                    
                    # Extract rgb/rgba colors
                    rgb_colors = re.findall(r'rgba?\([^)]+\)', value)
                    colors.update(rgb_colors)
        
        # Categorize colors
        self.color_scheme = {
            'primary': list(colors)[:3] if colors else [],
            'all_colors': list(colors),
            'total_colors': len(colors)
        }
    
    def _extract_typography(self):
        """Extract typography information"""
        fonts = set()
        font_sizes = set()
        
        for selector, properties in self.parsed_rules.items():
            if 'font-family' in properties:
                font = properties['font-family'].replace('"', '').replace("'", '')
                fonts.add(font)
            
            if 'font-size' in properties:
                font_sizes.add(properties['font-size'])
        
        self.typography = {
            'fonts': list(fonts),
            'sizes': list(font_sizes),
            'primary_font': list(fonts)[0] if fonts else 'inherit'
        }
    
    def _extract_layout(self):
        """Extract layout information"""
        layout_types = {
            'flexbox': False,
            'grid': False,
            'responsive': False
        }
        
        for selector, properties in self.parsed_rules.items():
            if 'display' in properties:
                if 'flex' in properties['display']:
                    layout_types['flexbox'] = True
                if 'grid' in properties['display']:
                    layout_types['grid'] = True
            
            # Check for media queries
            if '@media' in selector:
                layout_types['responsive'] = True
        
        self.layout_info = layout_types
# ============================================
# FILE: backend/services/html_parser_enhanced.py
# Enhanced HTML parser with CSS integration
# ============================================

from bs4 import BeautifulSoup
import re
from typing import Dict, List, Tuple

class EnhancedHTMLParser:
    """Enhanced HTML parser with CSS integration"""
    
    def __init__(self, html_content, css_data=None):
        self.soup = BeautifulSoup(html_content, 'html5lib')  # FIXED for Windows
        self.css_data = css_data or {}
        self.structure = {}
    
    def parse(self):
        """Parse HTML with CSS context"""
        self.structure = {
            'title': self._get_title(),
            'meta': self._extract_meta(),
            'sections': self._identify_sections(),
            'components': self._identify_components(),
            'navigation': self._extract_navigation(),
            'footer': self._extract_footer(),
            'forms': self._extract_forms(),
            'media': self._extract_media(),
            'styling_context': self.css_data
        }
        return self.structure
    
    def _get_title(self):
        title = self.soup.find('title')
        h1 = self.soup.find('h1')
        return {
            'page_title': title.text if title else 'Untitled',
            'main_heading': h1.text if h1 else ''
        }
    
    def _extract_meta(self):
        """Extract meta information"""
        meta_tags = self.soup.find_all('meta')
        meta_data = {}
        
        for tag in meta_tags:
            name = tag.get('name') or tag.get('property')
            content = tag.get('content')
            if name and content:
                meta_data[name] = content
        
        return meta_data
    
    def _identify_sections(self):
        """Identify major page sections"""
        sections = []
        
        # Look for semantic sections
        for section in self.soup.find_all(['section', 'article', 'div'], class_=True):
            classes = ' '.join(section.get('class', []))
            
            # Identify section type
            section_type = self._classify_section(section, classes)
            
            if section_type:
                sections.append({
                    'type': section_type,
                    'classes': classes,
                    'id': section.get('id', ''),
                    'content': self._extract_section_content(section),
                    'html_snippet': str(section)[:500]
                })
        
        return sections
    
    def _classify_section(self, section, classes):
        """Classify section based on classes and content"""
        classes_lower = classes.lower()
        
        # Hero/Banner
        if any(word in classes_lower for word in ['hero', 'banner', 'jumbotron', 'splash']):
            return 'hero'
        
        # Features
        if any(word in classes_lower for word in ['feature', 'benefit', 'service']):
            return 'features'
        
        # Testimonials
        if any(word in classes_lower for word in ['testimonial', 'review', 'quote']):
            return 'testimonials'
        
        # Pricing
        if any(word in classes_lower for word in ['pricing', 'plan', 'package']):
            return 'pricing'
        
        # CTA Section
        if any(word in classes_lower for word in ['cta', 'call-to-action', 'conversion']):
            return 'cta_section'
        
        # Content
        if any(word in classes_lower for word in ['content', 'about', 'description']):
            return 'content'
        
        return 'generic'
    
    def _extract_section_content(self, section):
        """Extract structured content from a section"""
        content = {
            'heading': '',
            'subheading': '',
            'paragraphs': [],
            'images': [],
            'buttons': []
        }
        
        # Headings
        for i, tag_name in enumerate(['h1', 'h2', 'h3', 'h4']):
            heading = section.find(tag_name)
            if heading:
                if i == 0:
                    content['heading'] = heading.get_text(strip=True)
                else:
                    content['subheading'] = heading.get_text(strip=True)
                break
        
        # Paragraphs
        for p in section.find_all('p'):
            text = p.get_text(strip=True)
            if len(text) > 10:
                content['paragraphs'].append(text)
        
        # Images
        for img in section.find_all('img'):
            content['images'].append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            })
        
        # Buttons/CTAs
        for btn in section.find_all(['button', 'a'], class_=True):
            classes = ' '.join(btn.get('class', []))
            if any(word in classes.lower() for word in ['btn', 'button', 'cta']):
                content['buttons'].append({
                    'text': btn.   (strip=True),
                    'href': btn.get('href', '#'),
                    'classes': classes
                })
        
        return content
    
    def _identify_components(self):
        """Identify reusable components"""
        components = {
            'cards': [],
            'buttons': [],
            'forms': [],
            'modals': []
        }
        
        # Cards
        for card in self.soup.find_all(class_=re.compile(r'card', re.I)):
            components['cards'].append({
                'classes': ' '.join(card.get('class', [])),
                'content': card.get_text(strip=True)[:200]
            })
        
        # Buttons
        for btn in self.soup.find_all(['button', 'a'], class_=re.compile(r'btn|button', re.I)):
            components['buttons'].append({
                'text': btn.get_text(strip=True),
                'type': btn.name,
                'classes': ' '.join(btn.get('class', []))
            })
        
        return components
    
    def _extract_navigation(self):
        """Extract navigation menu"""
        nav = self.soup.find('nav')
        if not nav:
            nav = self.soup.find(class_=re.compile(r'nav|menu', re.I))
        
        if nav:
            links = []
            for link in nav.find_all('a'):
                links.append({
                    'text': link.get_text(strip=True),
                    'href': link.get('href', '#')
                })
            return links
        
        return []
    
    def _extract_footer(self):
        """Extract footer content"""
        footer = self.soup.find('footer')
        if footer:
            return {
                'text': footer.get_text(strip=True),
                'links': [{'text': a.get_text(strip=True), 'href': a.get('href', '#')} 
                         for a in footer.find_all('a')]
            }
        return {}
    
    def _extract_forms(self):
        """Extract form fields"""
        forms = []
        for form in self.soup.find_all('form'):
            fields = []
            for input_tag in form.find_all(['input', 'textarea', 'select']):
                fields.append({
                    'type': input_tag.get('type', 'text'),
                    'name': input_tag.get('name', ''),
                    'placeholder': input_tag.get('placeholder', ''),
                    'required': input_tag.has_attr('required')
                })
            
            forms.append({
                'action': form.get('action', ''),
                'method': form.get('method', 'post'),
                'fields': fields
            })
        
        return forms
    
    def _extract_media(self):
        """Extract all media elements"""
        media = {
            'images': [],
            'videos': [],
            'icons': []
        }
        
        # Images
        for img in self.soup.find_all('img'):
            media['images'].append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'width': img.get('width', ''),
                'height': img.get('height', '')
            })
        
        # Videos
        for video in self.soup.find_all(['video', 'iframe']):
            media['videos'].append({
                'src': video.get('src', ''),
                'type': video.name
            })
        
        # SVG icons
        for svg in self.soup.find_all('svg'):
            media['icons'].append({
                'classes': ' '.join(svg.get('class', []))
            })
        
        return media

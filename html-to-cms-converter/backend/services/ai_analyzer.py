# ============================================
# FILE: backend/services/ai_analyzer.py
# OpenAI GPT-4 Integration for intelligent analysis
# ============================================

from openai import OpenAI
import json
import os

class AIAnalyzer:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
    
    def analyze_structure(self, parsed_data):
        """Use GPT-4 to intelligently identify content zones"""
        
        prompt = self._create_analysis_prompt(parsed_data)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing HTML structures and identifying content zones for CMS conversion. You identify CTAs, hero sections, descriptions, image placeholders, and other content types with high accuracy."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"AI Analysis Error: {e}")
            return self._fallback_analysis(parsed_data)
    
    def _create_analysis_prompt(self, parsed_data):
        """Create a detailed prompt for GPT-4"""
        
        elements_summary = []
        if 'elements' in parsed_data:
            for elem in parsed_data['elements'][:50]:  # Limit to avoid token limits
                elements_summary.append({
                    'type': elem['type'],
                    'tag': elem.get('tag', ''),
                    'text': elem.get('text', '')[:100],  # Truncate long text
                    'classes': elem.get('classes', '')
                })
        
        prompt = f"""
Analyze this HTML structure and identify content zones for CMS conversion.

Page Title: {parsed_data.get('title', 'Unknown')}

Elements Found:
{json.dumps(elements_summary, indent=2)}

Please identify and categorize:
1. CTAs (Call-to-Actions) - buttons or links for actions
2. Hero Section - main banner/headline area
3. Descriptions - main content/body text
4. Images - all image placeholders
5. Navigation - menu items
6. Footer - footer content
7. Forms - any form fields

Return a JSON object with this structure:
{{
    "ctas": [
        {{"text": "...", "purpose": "...", "location": "..."}}
    ],
    "hero": {{
        "headline": "...",
        "subheadline": "...",
        "description": "..."
    }},
    "content_sections": [
        {{"heading": "...", "description": "...", "type": "..."}}
    ],
    "images": [
        {{"purpose": "...", "alt_text": "...", "location": "..."}}
    ],
    "navigation": [...],
    "forms": [...],
    "cms_mapping": {{
        "recommended_cms": "wordpress|webflow|strapi",
        "field_mappings": {{}}
    }}
}}
"""
        return prompt
    
    def _fallback_analysis(self, parsed_data):
        """Fallback rule-based analysis if API fails"""
        return {
            "ctas": [],
            "hero": {},
            "content_sections": [],
            "images": [],
            "navigation": [],
            "forms": [],
            "cms_mapping": {
                "recommended_cms": "wordpress",
                "field_mappings": {}
            },
            "error": "AI analysis unavailable, using fallback"
        }
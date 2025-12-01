# ============================================
# FILE: backend/test_converter.py
# Testing Script for Final Converter
# ============================================

import requests
import json
from pathlib import Path

def test_converter():
    """Test the final converter"""
    
    print("\n" + "="*70)
    print("🧪 TESTING FINAL CONVERTER v6.0")
    print("="*70 + "\n")
    
    # Load test HTML
    html_file = Path('../tests/sample.html')
    if not html_file.exists():
        print("❌ Test HTML file not found")
        return
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"✓ Loaded test HTML ({len(html_content)} chars)")
    
    # Make API request
    url = 'http://localhost:5000/api/convert'
    payload = {
        'html': html_content,
        'css': ''
    }
    
    print("✓ Sending request to API...")
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ SUCCESS!")
            print(f"   Version: {result.get('version')}")
            print(f"   Accuracy: {result.get('accuracy')}")
            print(f"   Total Blocks: {result.get('total_blocks')}")
            
            print(f"\n📦 Generated Blocks:")
            for block in result.get('blocks', []):
                print(f"   • {block['name']} ({block['field_count']} fields)")
                
                # Count improvements
                alt_texts = sum(1 for f in block['fields'] if f.get('semantic_role') == 'accessibility')
                icons = sum(1 for f in block['fields'] if f.get('semantic_role') in ['icon', 'icon_set'])
                
                if alt_texts > 0:
                    print(f"     ✓ {alt_texts} alt text fields")
                if icons > 0:
                    print(f"     ✓ {icons} icon fields")
            
            print(f"\n✨ Improvements Applied:")
            improvements = result.get('improvements', {})
            for key, value in improvements.items():
                print(f"   {'✓' if value else '✗'} {key.replace('_', ' ').title()}")
            
            print(f"\n📁 Output: {result.get('output_directory')}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Is the server running?")
        print("   Start with: python app.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_analyze():
    """Test the analyze endpoint"""
    
    print("\n" + "="*70)
    print("🔍 TESTING ANALYZE ENDPOINT")
    print("="*70 + "\n")
    
    html_file = Path('../tests/sample.html')
    if not html_file.exists():
        print("❌ Test HTML file not found")
        return
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    url = 'http://localhost:5000/api/analyze'
    payload = {'html': html_content}
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            analysis = result.get('analysis', {})
            
            print("✅ Analysis Complete!")
            print(f"\n📊 Content Statistics:")
            print(f"   Sections: {analysis.get('sections')}")
            print(f"   Paragraphs: {analysis.get('paragraphs')}")
            print(f"   Links: {analysis.get('links')}")
            print(f"   Forms: {analysis.get('forms')}")
            
            images = analysis.get('images', {})
            print(f"\n🖼️  Image Analysis:")
            print(f"   Total Images: {images.get('total')}")
            print(f"   Regular Images: {images.get('regular_images')}")
            print(f"   Icons: {images.get('icons')}")
            print(f"   With Alt Text: {images.get('with_alt_text')}")
            print(f"   Without Alt Text: {images.get('without_alt_text')}")
            print(f"   Alt Coverage: {images.get('alt_coverage')}")
            
            recommendations = result.get('recommendations', [])
            if recommendations:
                print(f"\n💡 Recommendations:")
                for rec in recommendations:
                    priority = rec.get('priority', 'low').upper()
                    print(f"   [{priority}] {rec.get('message')}")
            
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_health():
    """Test the health endpoint"""
    
    print("\n" + "="*70)
    print("💚 TESTING HEALTH ENDPOINT")
    print("="*70 + "\n")
    
    try:
        response = requests.get('http://localhost:5000/api/health')
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Server is healthy!")
            print(f"   Version: {result.get('version')}")
            print(f"   Status: {result.get('status')}")
            
            features = result.get('features', {})
            print(f"\n✨ Features Enabled:")
            for feature, status in features.items():
                print(f"   {'✓' if status == 'enabled' or status == 'full' else '✗'} {feature.replace('_', ' ').title()}")
        else:
            print(f"❌ Server unhealthy: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'convert':
            test_converter()
        elif command == 'analyze':
            test_analyze()
        elif command == 'health':
            test_health()
        elif command == 'all':
            test_health()
            test_analyze()
            test_converter()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python test_converter.py [convert|analyze|health|all]")
    else:
        # Run all tests by default
        test_health()
        test_analyze()
        test_converter()
    
    print("\n" + "="*70)
    print("✅ TESTING COMPLETE")
    print("="*70 + "\n")
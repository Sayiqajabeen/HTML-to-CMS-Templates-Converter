# ============================================
# FILE: tests/test_generalized.py
# Test the Generalized Block Generator
# ============================================

import sys
sys.path.insert(0, '../backend')

from services.block_cms_generator_generalized import GeneralizedBlockGenerator
import json

def test_case_1():
    """Test Case 1: Simple Hero Section"""
    print("\n" + "="*70)
    print("TEST 1: Simple Hero Section")
    print("="*70)
    
    html = '''
    <section class="hero-banner">
        <h1>Welcome to Our <strong>Amazing</strong> Platform</h1>
        <p>Discover the future of web development with our cutting-edge tools.</p>
        <a href="/signup" class="btn-primary">Get Started Today</a>
        <img src="/images/hero-bg.jpg" alt="Hero Background" />
    </section>
    '''
    
    converter = GeneralizedBlockGenerator(html, 'concrete5')
    result = converter.convert()
    
    print(f"\n✅ Blocks Generated: {result['total_blocks']}")
    
    for block in result['blocks']:
        print(f"\n📦 Block: {block['block_name']}")
        print(f"   ID: {block['block_id']}")
        print(f"   Fields: {block['field_count']}")
        print("\n   Extracted Fields:")
        for field in block['fields']:
            print(f"      • {field['label']} ({field['type']}) - {field.get('semantic_role', 'N/A')}")
    
    return result

def test_case_3():
    """Test Case 3: Feature Cards Grid"""
    print("\n" + "="*70)
    print("TEST 3: Feature Cards Grid")
    print("="*70)
    
    html = '''
    <section class="features-grid">
        <h2>Why Choose Us</h2>
        <p>Here are the top reasons our customers love us.</p>
        
        <div class="row">
            <div class="col">
                <h3>Fast Performance</h3>
                <p>Lightning-fast load times guaranteed.</p>
            </div>
            <div class="col">
                <h3>24/7 Support</h3>
                <p>Our team is always here to help.</p>
            </div>
            <div class="col">
                <h3>Secure Platform</h3>
                <p>Bank-level encryption for your data.</p>
            </div>
        </div>
        
        <img src="/icons/feature1.svg" alt="Feature 1" />
        <img src="/icons/feature2.svg" alt="Feature 2" />
        <img src="/icons/feature3.svg" alt="Feature 3" />
    </section>
    '''
    
    converter = GeneralizedBlockGenerator(html, 'concrete5')
    result = converter.convert()
    
    print(f"\n✅ Blocks Generated: {result['total_blocks']}")
    
    for block in result['blocks']:
        print(f"\n📦 Block: {block['block_name']}")
        print(f"   Fields: {block['field_count']}")
        print("\n   Extracted Fields:")
        for field in block['fields']:
            value_preview = str(field.get('value', ''))[:50]
            print(f"      • {field['label']} - {value_preview}...")
    
    return result

def test_case_4():
    """Test Case 4: Your Contact Map Block"""
    print("\n" + "="*70)
    print("TEST 4: Your Real Contact Map Block (from provided files)")
    print("="*70)
    
    html = '''
    <section class="map_wrapper curve_bot">
        <div class="cnt flex">
            <div class="map_details">
                <div class="title_sec">
                    <h3>VISIT US</h3>
                    <h2>Come visit our <strong>Milton Keynes Practice</strong></h2>
                    <p>If you have any questions about access at our practice, please call our friendly team and we will be happy to assist you.</p>
                </div>
                
                <p><i class="fa-solid fa-location-dot"></i> 12 Whittle Court, Knowlhill, Milton Keynes, MK5 8FT</p>
                <p><i class="fa-solid fa-phone"></i> <a href="tel:01908398068">01908 398 068</a></p>
                <p><i class="fa-solid fa-envelope"></i> <a href="mailto:hello@smilelux.co.uk">hello@smilelux.co.uk</a></p>
                
                <h6><i class="fa fa-clock"></i> Opening Hours</h6>
                <ul class="open_time">
                    <dl>
                        <dt>Monday</dt>
                        <dd>8:30am to 1:00pm</dd>
                        <dt>Tuesday</dt>
                        <dd>8:00am to 5:30pm</dd>
                        <dt>Wednesday</dt>
                        <dd>8:00am to 5:30pm</dd>
                        <dt>Thursday</dt>
                        <dd>8:00am to 5:30pm</dd>
                        <dt>Friday</dt>
                        <dd>8:30am to 2:00pm</dd>
                    </dl>
                </ul>
            </div>
            
            <div class="map-with-tabs">
                <div class="map-wrap">
                    <div class="google_map" id="location_map"></div>
                </div>
            </div>
        </div>
    </section>
    '''
    
    converter = GeneralizedBlockGenerator(html, 'concrete5')
    result = converter.convert()
    
    print(f"\n✅ Blocks Generated: {result['total_blocks']}")
    
    for block in result['blocks']:
        print(f"\n📦 Block: {block['block_name']}")
        print(f"   ID: {block['block_id']}")
        print(f"   Classes: {block['classes']}")
        print(f"   Total Fields: {block['field_count']}")
        
        print("\n   📋 All Extracted Fields:")
        for field in block['fields']:
            print(f"      • {field['name']} ({field['type']})")
            print(f"        Label: {field['label']}")
            print(f"        Role: {field.get('semantic_role', 'N/A')}")
            print(f"        Importance: {field.get('importance', 'N/A')}")
            value_preview = str(field.get('value', ''))[:60]
            print(f"        Value: {value_preview}...")
            print()
        
        # Save files for inspection
        print("\n   💾 Saving Generated Files...")
        import os
        output_dir = f'../output/test_{block["block_id"]}'
        os.makedirs(output_dir, exist_ok=True)
        
        with open(f'{output_dir}/view.php', 'w', encoding='utf-8') as f:
            f.write(block['view_php'])
        with open(f'{output_dir}/controller.php', 'w', encoding='utf-8') as f:
            f.write(block['controller_php'])
        with open(f'{output_dir}/form.php', 'w', encoding='utf-8') as f:
            f.write(block['form_php'])
        with open(f'{output_dir}/db.xml', 'w', encoding='utf-8') as f:
            f.write(block['db_xml'])
        
        # Save content.json
        content_json = {field['name']: field.get('value', '') for field in block['fields']}
        with open(f'{output_dir}/content.json', 'w', encoding='utf-8') as f:
            json.dump(content_json, f, indent=2, ensure_ascii=False)
        
        print(f"      ✓ Saved to: {output_dir}/")
        print(f"      ✓ Files: view.php, controller.php, form.php, db.xml, content.json")
    
    return result

def test_case_5():
    """Test Case 5: Complex Multi-Element Section"""
    print("\n" + "="*70)
    print("TEST 5: Complex Section (Headings + Paragraphs + Images + CTAs)")
    print("="*70)
    
    html = '''
    <section class="about-us-section">
        <h1>About Our Company</h1>
        <h2>Leading the Industry Since 2010</h2>
        
        <p>We are a team of passionate professionals dedicated to delivering excellence.</p>
        <p>Our mission is to revolutionize the way businesses operate through innovative technology solutions.</p>
        <p>With over 500 satisfied clients worldwide, we continue to push boundaries.</p>
        
        <img src="/team-photo.jpg" alt="Our Team" />
        <img src="/office-photo.jpg" alt="Our Office" />
        
        <a href="/about" class="btn-learn-more">Learn More About Us</a>
        <a href="/contact" class="btn-contact">Contact Our Team</a>
        
        <ul>
            <li>10+ Years Experience</li>
            <li>500+ Happy Clients</li>
            <li>50+ Team Members</li>
            <li>24/7 Customer Support</li>
        </ul>
    </section>
    '''
    
    converter = GeneralizedBlockGenerator(html, 'concrete5')
    result = converter.convert()
    
    print(f"\n✅ Blocks Generated: {result['total_blocks']}")
    
    for block in result['blocks']:
        print(f"\n📦 Block: {block['block_name']}")
        print(f"   Fields: {block['field_count']}")
        
        # Group by semantic role
        roles = {}
        for field in block['fields']:
            role = field.get('semantic_role', 'other')
            if role not in roles:
                roles[role] = []
            roles[role].append(field['label'])
        
        print("\n   📊 Fields by Role:")
        for role, fields in roles.items():
            print(f"      {role.upper()}: {len(fields)} fields")
            for field_label in fields:
                print(f"         - {field_label}")
    
    return result

def run_all_tests():
    """Run all test cases"""
    print("\n" + "="*70)
    print("🧪 TESTING GENERALIZED BLOCK GENERATOR")
    print("="*70)
    print("\nThis will test the generator with 5 different HTML structures")
    print("to prove it works WITHOUT hardcoded templates.\n")
    
    results = []
    
    try:
        results.append(("Simple Hero", test_case_1()))
    except Exception as e:
        print(f"\n❌ Test 1 Failed: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        results.append(("Contact Form", test_case_2()))
    except Exception as e:
        print(f"\n❌ Test 2 Failed: {e}")
    
    try:
        results.append(("Feature Grid", test_case_3()))
    except Exception as e:
        print(f"\n❌ Test 3 Failed: {e}")
    
    try:
        results.append(("Contact Map", test_case_4()))
    except Exception as e:
        print(f"\n❌ Test 4 Failed: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        results.append(("Complex Section", test_case_5()))
    except Exception as e:
        print(f"\n❌ Test 5 Failed: {e}")
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    total_blocks = 0
    total_fields = 0
    
    for name, result in results:
        blocks = result.get('total_blocks', 0)
        total_blocks += blocks
        
        for block in result.get('blocks', []):
            total_fields += block['field_count']
        
        print(f"\n✅ {name}:")
        print(f"   Blocks: {blocks}")
        print(f"   Fields: {sum(b['field_count'] for b in result.get('blocks', []))}")
    
    print(f"\n" + "="*70)
    print(f"🎉 TOTAL RESULTS:")
    print(f"   Total Blocks Generated: {total_blocks}")
    print(f"   Total Fields Extracted: {total_fields}")
    print(f"   Success Rate: {len(results)}/5 tests passed")
    print("="*70)
    
    print("\n✨ Generalized Generator Test Complete!")
    print("💡 Check ../output/test_block_* directories for generated files")

if __name__ == '__main__':
    run_all_tests()']} ({field['type']}) - Role: {field['semantic_role']}")
        
        print("\n   View.php Preview (first 500 chars):")
        print(block['view_php'][:500] + "...")
    
    return result

def test_case_2():
    """Test Case 2: Contact Section with Form"""
    print("\n" + "="*70)
    print("TEST 2: Contact Section with Form")
    print("="*70)
    
    html = '''
    <section class="contact-us">
        <h2>Get in Touch</h2>
        <p>We'd love to hear from you. Fill out the form below.</p>
        
        <form action="/submit" method="post">
            <label for="name">Your Name</label>
            <input type="text" id="name" name="name" required />
            
            <label for="email">Email Address</label>
            <input type="email" id="email" name="email" required />
            
            <label for="message">Message</label>
            <textarea id="message" name="message" rows="5"></textarea>
            
            <button type="submit">Send Message</button>
        </form>
    </section>
    '''
    
    converter = GeneralizedBlockGenerator(html, 'concrete5')
    result = converter.convert()
    
    print(f"\n✅ Blocks Generated: {result['total_blocks']}")
    
    for block in result['blocks']:
        print(f"\n📦 Block: {block['block_name']}")
        print(f"   Fields: {block['field_count']}")
        print("\n   Extracted Fields:")
        for field in block['fields']:
            print(f"      • {field['label']}
# ============================================
# FILE: backend/routes/enhanced_routes.py
# Enhanced Routes for Concrete5 Block Generation
# ============================================

from flask import request, jsonify, send_file
from datetime import datetime
from pathlib import Path
import zipfile
import io
import json
from services.block_cms_generator_enhanced import EnhancedBlockGenerator
from services.css_parser import CSSParser
from utils.helpers import clean_html, detect_framework

# Output directory configuration
OUTPUT_DIR = Path('../output')
OUTPUT_DIR.mkdir(exist_ok=True)
(OUTPUT_DIR / 'concrete5-blocks').mkdir(exist_ok=True)

def register_enhanced_routes(app):
    """Register all enhanced routes with Flask app"""
    
    @app.route('/api/convert/enhanced', methods=['POST'])
    def convert_enhanced():
        """
        Enhanced conversion endpoint with smart content extraction
        
        Request Body:
        {
            "html": "<html>...</html>",
            "css": "body { ... }",
            "cms_type": "concrete5"
        }
        """
        try:
            data = request.json
            html_content = data.get('html')
            css_content = data.get('css', '')
            cms_type = data.get('cms_type', 'concrete5')
            
            if not html_content:
                return jsonify({
                    "success": False,
                    "error": "HTML content is required"
                }), 400
            
            if len(html_content) > 500000:  # 500KB limit
                return jsonify({
                    "success": False,
                    "error": "HTML too large. Max: 500000 bytes"
                }), 400
            
            print(f"\n{'='*70}")
            print(f"🔄 Enhanced Block Generation Starting")
            print(f"{'='*70}\n")
            
            # Step 1: Clean HTML
            html_content = clean_html(html_content)
            framework = detect_framework(html_content)
            print(f"🎨 Detected framework: {framework}")
            
            # Step 2: Parse CSS
            css_data = {}
            if css_content:
                print("🎨 Parsing CSS...")
                css_parser = CSSParser(css_content)
                css_data = css_parser.parse()
                print(f"   ✓ {len(css_data.get('rules', {}))} CSS rules")
                print(f"   ✓ {len(css_data.get('color_scheme', {}).get('all_colors', []))} colors")
                print(f"   ✓ {len(css_data.get('typography', {}).get('fonts', []))} fonts")
            
            # Step 3: Enhanced block generation
            print("\n🚀 Using Enhanced Block Generator...")
            converter = EnhancedBlockGenerator(html_content, cms_type)
            conversion_result = converter.convert()
            
            blocks = conversion_result.get('blocks', [])
            print(f"\n✓ Generated {len(blocks)} blocks:")
            
            block_summary = {}
            for block in blocks:
                block_type = block['type']
                block_summary[block_type] = block_summary.get(block_type, 0) + 1
                print(f"   • {block['block_name']} (fields: {block['field_count']})")
            
            # Step 4: Save block files
            blocks_dir = OUTPUT_DIR / 'concrete5-blocks'
            blocks_dir.mkdir(exist_ok=True)
            
            saved_files = []
            for block in blocks:
                # Create block directory
                block_dir = blocks_dir / block['block_id']
                block_dir.mkdir(exist_ok=True)
                
                # Save view.php
                view_file = block_dir / 'view.php'
                with open(view_file, 'w', encoding='utf-8') as f:
                    f.write(block['view_php'])
                
                # Save controller.php
                controller_file = block_dir / 'controller.php'
                with open(controller_file, 'w', encoding='utf-8') as f:
                    f.write(block['controller_php'])
                
                # Save form.php
                form_file = block_dir / 'form.php'
                with open(form_file, 'w', encoding='utf-8') as f:
                    f.write(block['form_php'])
                
                # Save db.xml
                db_file = block_dir / 'db.xml'
                with open(db_file, 'w', encoding='utf-8') as f:
                    f.write(block['db_xml'])
                
                # Save extracted content as JSON
                content_file = block_dir / 'content.json'
                with open(content_file, 'w', encoding='utf-8') as f:
                    json.dump(block['content_extracted'], f, indent=2)
                
                saved_files.append({
                    'block_id': block['block_id'],
                    'block_name': block['block_name'],
                    'files': ['view.php', 'controller.php', 'form.php', 'db.xml', 'content.json']
                })
                
                print(f"   ✓ Saved: {block['block_id']}/")
            
            # Step 5: Generate README
            readme_content = _generate_enhanced_readme(blocks, block_summary, css_data)
            readme_file = blocks_dir / 'README.md'
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            print(f"   ✓ Generated README.md")
            
            # Step 6: Generate installation guide
            install_guide = _generate_installation_guide(blocks)
            install_file = blocks_dir / 'INSTALLATION.md'
            with open(install_file, 'w', encoding='utf-8') as f:
                f.write(install_guide)
            print(f"   ✓ Generated INSTALLATION.md")
            
            # Step 7: Generate manifest
            manifest = {
                'generated_at': datetime.now().isoformat(),
                'total_blocks': len(blocks),
                'block_types': block_summary,
                'framework': framework,
                'css_colors': css_data.get('color_scheme', {}).get('primary', []),
                'css_fonts': css_data.get('typography', {}).get('fonts', []),
                'blocks': [
                    {
                        'id': b['block_id'],
                        'name': b['block_name'],
                        'type': b['type'],
                        'fields': len(b['content_extracted'])
                    }
                    for b in blocks
                ]
            }
            
            manifest_file = blocks_dir / 'manifest.json'
            with open(manifest_file, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2)
            print(f"   ✓ Generated manifest.json")
            
            print(f"\n{'='*70}")
            print(f"✅ Conversion Complete!")
            print(f"{'='*70}\n")
            
            return jsonify({
                "success": True,
                "cms_type": cms_type,
                "total_blocks": len(blocks),
                "block_types": block_summary,
                "blocks": [
                    {
                        'id': b['block_id'],
                        'name': b['block_name'],
                        'type': b['type'],
                        'fields': b['content_extracted'],
                        'field_count': b['field_count']
                    }
                    for b in blocks
                ],
                "output_directory": str(blocks_dir),
                "files": saved_files,
                "metadata": {
                    'framework': framework,
                    'generated_at': datetime.now().isoformat(),
                    'css_data': {
                        'colors': css_data.get('color_scheme', {}).get('all_colors', []),
                        'fonts': css_data.get('typography', {}).get('fonts', [])
                    }
                }
            })
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            import traceback
            traceback.print_exc()
            
            return jsonify({
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }), 500

    @app.route('/api/download/enhanced/<cms_type>', methods=['POST'])
    def download_enhanced(cms_type):
        """Download enhanced blocks as ZIP"""
        try:
            data = request.json
            blocks = data.get('blocks', [])
            
            if not blocks or cms_type != 'concrete5':
                return jsonify({"error": "Invalid request"}), 400
            
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                for block in blocks:
                    block_id = block['id']
                    
                    # Add view.php
                    zf.writestr(f'{block_id}/view.php', block.get('view_php', ''))
                    
                    # Add controller.php
                    zf.writestr(f'{block_id}/controller.php', block.get('controller_php', ''))
                    
                    # Add form.php
                    zf.writestr(f'{block_id}/form.php', block.get('form_php', ''))
                    
                    # Add db.xml
                    zf.writestr(f'{block_id}/db.xml', block.get('db_xml', ''))
                    
                    # Add content.json
                    content_json = json.dumps(block.get('fields', {}), indent=2)
                    zf.writestr(f'{block_id}/content.json', content_json)
                
                # Add README
                readme = data.get('readme', '')
                if readme:
                    zf.writestr('README.md', readme)
                
                # Add manifest
                manifest = data.get('manifest', {})
                if manifest:
                    zf.writestr('manifest.json', json.dumps(manifest, indent=2))
            
            memory_file.seek(0)
            return send_file(
                memory_file,
                mimetype='application/zip',
                as_attachment=True,
                download_name=f'concrete5-blocks-{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
            )
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/blocks/analyze', methods=['POST'])
    def analyze_blocks():
        """Analyze blocks without conversion"""
        try:
            data = request.json
            html_content = data.get('html', '')
            
            if not html_content:
                return jsonify({"error": "HTML required"}), 400
            
            converter = EnhancedBlockGenerator(html_content, 'concrete5')
            sections = converter.soup.find_all('section')
            
            analysis = {
                "total_sections": len(sections),
                "block_types": [],
                "content_summary": {}
            }
            
            type_counts = {}
            for section in sections:
                classes = ' '.join(section.get('class', []))
                block_type = converter._identify_block_type_smart(section, classes)
                
                if block_type:
                    type_counts[block_type] = type_counts.get(block_type, 0) + 1
                    analysis['block_types'].append({
                        "type": block_type,
                        "classes": classes,
                        "field_count": len(converter._extract_content_smart(section, block_type))
                    })
            
            analysis['content_summary'] = type_counts
            
            return jsonify({
                "success": True,
                "analysis": analysis
            })
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# ============================================
# HELPER FUNCTIONS
# ============================================

def _generate_enhanced_readme(blocks, block_summary, css_data):
    """Generate comprehensive README"""
    
    readme = f"""# Concrete5 Blocks - Enhanced Generation

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This package contains **{len(blocks)}** intelligent Concrete5 blocks automatically generated from your HTML template.

### Block Types Generated

"""
    
    for block_type, count in block_summary.items():
        readme += f"- **{block_type}**: {count} block(s)\n"
    
    readme += f"""

## Block Details

"""
    
    for block in blocks:
        readme += f"""
### {block['block_name']}

- **ID**: `{block['block_id']}`
- **Type**: `{block['type']}`
- **Extracted Fields**: {block['field_count']}

**Files**:
- `view.php` - Frontend display template
- `controller.php` - Block logic and database
- `form.php` - Admin edit form
- `db.xml` - Database schema
- `content.json` - Extracted content reference

"""
    
    if css_data:
        readme += f"""
## Styling Information

**Colors Found**: {', '.join(css_data.get('color_scheme', {}).get('primary', [])[:5])}

**Fonts**: {', '.join(css_data.get('typography', {}).get('fonts', [])[:3])}

"""
    
    readme += """
## Installation Instructions

1. **Upload Blocks**
   ```bash
   cd your-c5-site/application/blocks
   unzip concrete5-blocks-*.zip
   ```

2. **Refresh Dashboard**
   - Go to Dashboard → Extend Concrete5 → Install
   - Dashboard should auto-discover new blocks

3. **Add to Pages**
   - Edit any page
   - Add blocks from the block library
   - Configure content in the edit form

4. **Customize**
   - Edit `view.php` for HTML structure
   - Edit `controller.php` for PHP logic
   - Edit `form.php` for admin interface

## Database Schema

Each block creates its own database table:
- Table name: `btc_[block_type]`
- Fields defined in `db.xml`

## Best Practices

- Test blocks in a development environment first
- Backup your database before installing
- Customize form.php to match your content needs
- Add validation in controller.php

## Troubleshooting

**Blocks not appearing?**
- Clear dashboard cache: Dashboard → System & Settings → Clear Cache
- Check file permissions (755 for directories, 644 for files)

**Form fields not saving?**
- Verify db.xml field names match PHP variable names
- Check controller.php save() method implementation

**Styling issues?**
- Verify CSS classes match your theme
- Check bootstrap version compatibility

## Support

For Concrete5 block development documentation:
https://documentation.concrete5.org/block-development

Generated by: HTML to CMS Converter - Enhanced Block Generator
"""
    
    return readme

def _generate_installation_guide(blocks):
    """Generate detailed installation guide"""
    
    guide = """# Installation Guide - Concrete5 Blocks

## Step-by-Step Installation

### 1. Prepare Your Environment

Ensure you have:
- Concrete5 installation (v8.0 or higher)
- FTP/SFTP or SSH access
- Administrator access to Concrete5 dashboard

### 2. Extract Files to Correct Location

```
your-c5-site/
└── application/
    └── blocks/
        ├── block_1/
        │   ├── controller.php
        │   ├── view.php
        │   ├── form.php
        │   ├── db.xml
        │   └── content.json
        └── block_2/
            └── ... (same structure)
```

### 3. Set File Permissions

```bash
chmod 755 application/blocks/block_*/
chmod 644 application/blocks/block_*/*.php
chmod 644 application/blocks/block_*/db.xml
```

### 4. Register in Concrete5

1. Go to Dashboard
2. Navigate to **Extend Concrete5** section
3. Click **Installed Packages** or **Install**
4. Concrete5 will auto-discover blocks
5. Refresh page if blocks don't appear

### 5. Verify Installation

- Go to Page Editor
- Click "Add" to add a block
- Your blocks should appear in the block library
- Test adding one to a page

### 6. Customize (Optional)

Edit block files to customize:

**view.php** - Frontend display:
```php
<?php defined('C5_EXECUTE') or die('Access Denied.'); ?>
<section><?php echo $content; ?></section>
```

**controller.php** - Backend logic:
```php
class Controller extends BlockController {
    public function save($args) {
        parent::save($args);
    }
}
```

**form.php** - Admin form:
```php
<div class="form-group">
    <label>Field Name</label>
    <input type="text" name="field_name" />
</div>
```

## Common Issues

### Blocks Not Appearing

**Solution 1**: Clear cache
- Dashboard → System & Settings → Clear Cache

**Solution 2**: Check permissions
```bash
ls -la application/blocks/block_1/
```

**Solution 3**: Verify namespace in controller.php

### Form Not Saving

**Check**: db.xml field names match PHP variables

### Styling Broken

**Check**: CSS class names exist in your theme

## Support

Concrete5 Documentation: https://documentation.concrete5.org/
Block Development: https://documentation.concrete5.org/block-development
"""
    
    return guide
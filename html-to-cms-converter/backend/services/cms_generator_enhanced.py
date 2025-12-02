# ============================================
# FILE: backend/services/cms_generator_enhanced.py
# Enhanced CMS template generator with CSS support
# ============================================

import json
from typing import Dict, List

class EnhancedCMSGenerator:
    """Enhanced CMS template generator with CSS support"""
    
    def __init__(self, html_structure, css_data, cms_type='wordpress'):
        self.html_structure = html_structure
        self.css_data = css_data
        self.cms_type = cms_type
    
    def generate(self):
        """Generate comprehensive CMS template"""
        if self.cms_type == 'wordpress':
            return self._generate_wordpress_theme()
        elif self.cms_type == 'webflow':
            return self._generate_webflow_cms()
        elif self.cms_type == 'strapi':
            return self._generate_strapi_schema()
        else:
            return self._generate_generic_cms()
    
    def _generate_wordpress_theme(self):
        """Generate complete WordPress theme structure"""
        
        theme = {
            'theme_info': {
                'name': self.html_structure['title']['page_title'],
                'version': '1.0.0',
                'author': 'AI Generated'
            },
            'style_css': self._generate_wordpress_styles(),
            'template_parts': {},
            'acf_fields': self._generate_acf_fields(),
            'customizer_settings': self._generate_customizer_settings()
        }
        
        # Generate template files
        theme['template_parts'] = {
            'header.php': self._generate_header_template(),
            'footer.php': self._generate_footer_template(),
            'front-page.php': self._generate_front_page_template(),
            'functions.php': self._generate_functions_php()
        }
        
        return theme
    
    def _generate_wordpress_styles(self):
        """Generate WordPress style.css with theme info"""
        style_content = f"""
/*
Theme Name: {self.html_structure['title']['page_title']}
Theme URI: https://example.com
Author: AI Generated
Author URI: https://example.com
Description: AI-generated theme from HTML/CSS template
Version: 1.0.0
License: GNU General Public License v2 or later
Text Domain: ai-theme
*/

/* Color Scheme */
:root {{
"""
        # Add color variables from CSS
        if self.css_data.get('color_scheme'):
            for i, color in enumerate(self.css_data['color_scheme'].get('primary', [])):
                style_content += f"  --color-primary-{i+1}: {color};\n"
        
        # Add typography
        if self.css_data.get('typography'):
            fonts = self.css_data['typography'].get('fonts', [])
            if fonts:
                style_content += f"  --font-primary: {fonts[0]};\n"
        
        style_content += "}\n"
        
        return style_content
    
    def _generate_acf_fields(self):
        """Generate Advanced Custom Fields configuration"""
        acf_groups = []
        
        # Hero Section Fields
        hero_fields = {
            'group_name': 'Hero Section',
            'location': 'page_template == front-page.php',
            'fields': []
        }
        
        for section in self.html_structure.get('sections', []):
            if section['type'] == 'hero':
                content = section.get('content', {})
                if content.get('heading'):
                    hero_fields['fields'].append({
                        'name': 'hero_heading',
                        'type': 'text',
                        'label': 'Hero Heading',
                        'default_value': content['heading']
                    })
                if content.get('subheading'):
                    hero_fields['fields'].append({
                        'name': 'hero_subheading',
                        'type': 'textarea',
                        'label': 'Hero Subheading',
                        'default_value': content['subheading']
                    })
        
        if hero_fields['fields']:
            acf_groups.append(hero_fields)
        
        return acf_groups
    
    def _generate_customizer_settings(self):
        """Generate WordPress Customizer settings"""
        settings = {
            'colors': [],
            'typography': {},
            'layout': {}
        }
        
        # Color settings
        if self.css_data.get('color_scheme'):
            for i, color in enumerate(self.css_data['color_scheme'].get('primary', [])[:5]):
                settings['colors'].append({
                    'setting': f'primary_color_{i+1}',
                    'label': f'Primary Color {i+1}',
                    'default': color,
                    'type': 'color'
                })
        
        return settings
    
    def _generate_header_template(self):
        """Generate header.php template"""
        template = """<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="< bloginfo( 'charset' ); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<header class="site-header">
    <nav class="main-navigation">
        <?php
        wp_nav_menu( array(
            'theme_location' => 'primary',
            'menu_class'     => 'primary-menu',
        ) );
        ?>
    </nav>
</header>
"""
        return template
    
    def _generate_footer_template(self):
        """Generate footer.php template"""
        template = """<footer class="site-footer">
    <div class="footer-content">
        <p><?php echo get_theme_mod('footer_text', '&copy; 2024 All Rights Reserved'); ?></p>
    </div>
    <?php wp_footer(); ?>
</footer>
</body>
</html>
"""
        return template
    
    def _generate_front_page_template(self):
        
        template = """<?php
/**
 * Template Name: Front Page
 */

get_header();
?>

<main id="primary" class="site-main">
    
    <!-- Hero Section -->
    <section class="hero-section">
        <h1><?php the_field('hero_heading'); ?></h1>
        <p><?php the_field('hero_subheading'); ?></p>
    </section>

</main>

<?php
get_footer();
"""
        return template
    
    def _generate_functions_php(self):
        """Generate functions.php"""
        template = """<?php
/**
 * Theme Functions
 */

// Enqueue styles and scripts
function ai_theme_enqueue_styles() {
    wp_enqueue_style( 'ai-theme-style', get_stylesheet_uri() );
}
add_action( 'wp_enqueue_scripts', 'ai_theme_enqueue_styles' );

// Register navigation menus
function ai_theme_register_menus() {
    register_nav_menus( array(
        'primary' => __( 'Primary Menu', 'ai-theme' ),
    ) );
}
add_action( 'init', 'ai_theme_register_menus' );

// Add theme support
function ai_theme_setup() {
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'custom-logo' );
}
add_action( 'after_setup_theme', 'ai_theme_setup' );
"""
        return template
    
    def _generate_webflow_cms(self):
        """Generate Webflow CMS structure"""
        return {
            'collections': [
                {
                    'name': 'Pages',
                    'fields': [
                        {'name': 'Name', 'type': 'PlainText', 'required': True},
                        {'name': 'Slug', 'type': 'PlainText', 'required': True},
                        {'name': 'Hero Heading', 'type': 'PlainText'},
                        {'name': 'Hero Description', 'type': 'RichText'},
                        {'name': 'Featured Image', 'type': 'Image'}
                    ]
                }
            ],
            'styling': self.css_data
        }
    
    def _generate_strapi_schema(self):
        """Generate Strapi content schema"""
        return {
            'contentTypes': {
                'page': {
                    'kind': 'collectionType',
                    'attributes': {
                        'title': {'type': 'string', 'required': True},
                        'slug': {'type': 'uid', 'targetField': 'title'},
                        'heroHeading': {'type': 'string'},
                        'heroDescription': {'type': 'richtext'},
                        'featuredImage': {'type': 'media'}
                    }
                }
            }
        }
    
    def _generate_generic_cms(self):
        """Generate generic CMS-agnostic JSON"""
        return {
            'template_name': self.html_structure['title']['page_title'],
            'sections': self.html_structure['sections'],
            'components': self.html_structure['components'],
            'styling': self.css_data,
            'navigation': self.html_structure['navigation'],
            'footer': self.html_structure['footer']
        }

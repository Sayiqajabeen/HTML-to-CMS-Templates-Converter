// ============================================
// FILE: frontend/script.js
// Main JavaScript for HTML to CMS Converter
// ============================================

const API_URL = 'http://localhost:5000/api';
let currentData = null;
let currentTab = 'summary';

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Event Listeners
    document.getElementById('convertBtn').addEventListener('click', convertHTML);
    document.getElementById('analyzeBtn').addEventListener('click', analyzeHTML);
    document.getElementById('downloadBtn').addEventListener('click', downloadZIP);
    document.getElementById('copyBtn').addEventListener('click', copyToClipboard);
    document.getElementById('previewBtn').addEventListener('click', previewTemplate);
    document.getElementById('htmlFile').addEventListener('change', loadHTMLFile);

    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });

    // Check server status
    checkServerStatus();
}

// Check if server is running
async function checkServerStatus() {
    try {
        const response = await fetch(`${API_URL}/health`, { timeout: 3000 });
        if (response.ok) {
            console.log('✅ Server is running');
        }
    } catch (error) {
        console.warn('⚠️ Server not detected. Make sure to run: python backend/app.py');
        showMessage('⚠️ Server not running. Please start the backend server.', 'error');
    }
}

// Main conversion function
async function convertHTML() {
    const html = document.getElementById('htmlInput').value;
    const css = document.getElementById('cssInput').value;
    const cmsType = document.getElementById('cmsType').value;
    
    if (!html.trim()) {
        alert('❌ Please paste HTML content first!');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_URL}/convert`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ 
                html: html, 
                css: css, 
                cms_type: cmsType 
            })
        });
        
        const data = await response.json();
        currentData = data;
        
        if (data.success) {
            displayResults(data);
            document.getElementById('actionBtns').classList.remove('hidden');
            showMessage('✅ Conversion successful! Check the output below.', 'success');
        } else {
            displayError(data.error || 'Conversion failed');
        }
    } catch (error) {
        displayError('❌ Connection error. Make sure the server is running on port 5000.');
        console.error('Conversion error:', error);
    } finally {
        showLoading(false);
    }
}

// Quick analyze function
async function analyzeHTML() {
    const html = document.getElementById('htmlInput').value;
    
    if (!html.trim()) {
        alert('❌ Please paste HTML content first!');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_URL}/analyze-html`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ html: html })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayAnalysis(data.analysis);
            showMessage('✅ Analysis complete!', 'success');
        } else {
            displayError('Analysis failed');
        }
    } catch (error) {
        displayError('❌ Analysis failed. Make sure server is running.');
        console.error('Analysis error:', error);
    } finally {
        showLoading(false);
    }
}

// Display results based on current tab
function displayResults(data) {
    const output = document.getElementById('output');
    
    switch(currentTab) {
        case 'summary':
            output.innerHTML = formatSummary(data);
            break;
        case 'blocks':
            output.innerHTML = formatBlocks(data);
            break;
        case 'code':
            output.innerHTML = formatCode(data);
            break;
        case 'json':
            output.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            break;
        default:
            output.innerHTML = formatSummary(data);
    }
}

// Format summary view
function formatSummary(data) {
    const metadata = data.metadata || {};
    const cmsType = data.cms_type;
    
    let html = '<div class="summary">';
    
    // Stats
    html += '<div class="stats">';
    
    if (cmsType === 'concrete5') {
        html += `
            <div class="stat-card">
                <h3>${metadata.total_blocks || 0}</h3>
                <p>Blocks Generated</p>
            </div>
        `;
    } else {
        html += `
            <div class="stat-card">
                <h3>${metadata.total_sections || 0}</h3>
                <p>Sections Found</p>
            </div>
        `;
    }
    
    html += `
        <div class="stat-card">
            <h3>${metadata.total_images || 0}</h3>
            <p>Images</p>
        </div>
        <div class="stat-card">
            <h3>${metadata.colors_found || 0}</h3>
            <p>Colors</p>
        </div>
    </div>`;
    
    // Files generated
    if (data.files_generated && data.files_generated.length > 0) {
        html += '<h3 style="margin: 20px 0 10px; color: #333;">📁 Files Generated:</h3>';
        html += '<ul class="block-list">';
        data.files_generated.forEach(file => {
            html += `<li class="block-item"><h4>✓ ${file}</h4></li>`;
        });
        html += '</ul>';
    }
    
    // Output directory
    if (data.output_directory) {
        html += `<p style="margin-top: 20px; color: #666; background: #f9f9f9; padding: 15px; border-radius: 8px;">
            <strong>📂 Output Directory:</strong><br>
            <code style="background: #e0e0e0; padding: 5px 10px; border-radius: 4px; word-break: break-all;">
                ${data.output_directory}
            </code>
        </p>`;
    }
    
    html += '</div>';
    return html;
}

// Format blocks view
function formatBlocks(data) {
    const blocks = data.blocks || [];
    
    if (blocks.length === 0) {
        return '<p class="placeholder">No blocks generated</p>';
    }
    
    let html = '<ul class="block-list">';
    
    blocks.forEach((block, i) => {
        const contentCount = Object.keys(block.content_extracted || {}).length;
        html += `
            <li class="block-item">
                <h4>${i + 1}. ${block.block_name}</h4>
                <p><strong>File:</strong> <code>${block.block_type}.php</code></p>
                <p><strong>Content items:</strong> ${contentCount}</p>
                <p><strong>Classes:</strong> <code>${block.original_classes || 'N/A'}</code></p>
            </li>
        `;
    });
    
    html += '</ul>';
    return html;
}

// Format code view
function formatCode(data) {
    if (data.blocks && data.blocks.length > 0) {
        const firstBlock = data.blocks[0];
        return `
            <div style="margin-bottom: 15px;">
                <h4 style="color: #333; margin-bottom: 10px;">
                    ${firstBlock.block_name} 
                    <span style="color: #999; font-size: 0.8em;">(${firstBlock.block_type}.php)</span>
                </h4>
            </div>
            <pre>${escapeHtml(firstBlock.php_template)}</pre>
        `;
    }
    return '<p class="placeholder">No code available</p>';
}

// Display analysis results
function displayAnalysis(analysis) {
    const output = document.getElementById('output');
    
    let html = '<div class="analysis">';
    html += `<h3 style="color: #333; margin-bottom: 20px;">📊 Quick Analysis</h3>`;
    html += '<div class="stats">';
    html += `
        <div class="stat-card">
            <h3>${analysis.total_sections}</h3>
            <p>Sections</p>
        </div>
        <div class="stat-card">
            <h3>${analysis.images_count}</h3>
            <p>Images</p>
        </div>
        <div class="stat-card">
            <h3>${analysis.forms_count}</h3>
            <p>Forms</p>
        </div>
    </div>`;
    
    html += '<h4 style="margin: 20px 0 10px; color: #333;">📋 Section Types Found:</h4>';
    html += '<ul class="block-list">';
    analysis.section_types.forEach(section => {
        html += `<li class="block-item">
            <h4>${section.type}</h4>
            <p>Classes: <code>${section.classes || 'none'}</code></p>
        </li>`;
    });
    html += '</ul></div>';
    
    output.innerHTML = html;
}

// Tab switching
function switchTab(tabName) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    currentTab = tabName;
    
    if (currentData) {
        displayResults(currentData);
    }
}

// Download ZIP file
async function downloadZIP() {
    if (!currentData) {
        alert('No data to download');
        return;
    }
    
    const cmsType = currentData.cms_type;
    
    try {
        showMessage('📥 Preparing download...', 'success');
        
        const response = await fetch(`${API_URL}/download/${cmsType}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(currentData)
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${cmsType}-template-${Date.now()}.zip`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            showMessage('✅ Download started successfully!', 'success');
        } else {
            const errorData = await response.json();
            showMessage('❌ Download failed: ' + (errorData.error || 'Unknown error'), 'error');
        }
    } catch (error) {
        showMessage('❌ Download error: ' + error.message, 'error');
        console.error('Download error:', error);
    }
}

// Copy to clipboard
function copyToClipboard() {
    if (!currentData) {
        alert('No data to copy');
        return;
    }
    
    let textToCopy = '';
    
    if (currentData.blocks && currentData.blocks.length > 0) {
        textToCopy = currentData.blocks[0].php_template;
    } else if (currentData.cms_template) {
        textToCopy = JSON.stringify(currentData.cms_template, null, 2);
    } else {
        textToCopy = JSON.stringify(currentData, null, 2);
    }
    
    navigator.clipboard.writeText(textToCopy).then(() => {
        showMessage('✅ Copied to clipboard!', 'success');
    }).catch((error) => {
        console.error('Copy failed:', error);
        // Fallback method
        const textarea = document.createElement('textarea');
        textarea.value = textToCopy;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showMessage('✅ Copied to clipboard!', 'success');
    });
}

// Preview template
async function previewTemplate() {
    if (!currentData) {
        alert('No data to preview');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/preview`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                blocks: currentData.blocks,
                cms_template: currentData.cms_template,
                cms_type: currentData.cms_type
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            const preview = window.open('', '_blank', 'width=1200,height=800');
            preview.document.write(data.preview_html);
            preview.document.close();
        } else {
            showMessage('❌ Preview failed: ' + (data.error || 'Unknown error'), 'error');
        }
    } catch (error) {
        showMessage('❌ Preview error: ' + error.message, 'error');
        console.error('Preview error:', error);
    }
}

// Load HTML file
function loadHTMLFile(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    if (!file.name.endsWith('.html') && !file.name.endsWith('.htm')) {
        alert('❌ Please select an HTML file');
        return;
    }
    
    const reader = new FileReader();
    
    reader.onload = (e) => {
        document.getElementById('htmlInput').value = e.target.result;
        showMessage(`✅ File loaded: ${file.name} (${formatFileSize(file.size)})`, 'success');
    };
    
    reader.onerror = () => {
        showMessage('❌ Failed to load file', 'error');
    };
    
    reader.readAsText(file);
}

// Show/hide loading state
function showLoading(show) {
    const loadingEl = document.getElementById('loading');
    const convertBtn = document.getElementById('convertBtn');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    loadingEl.classList.toggle('hidden', !show);
    convertBtn.disabled = show;
    analyzeBtn.disabled = show;
    
    if (show) {
        convertBtn.textContent = '⏳ Converting...';
        analyzeBtn.textContent = '⏳ Analyzing...';
    } else {
        convertBtn.textContent = '🔄 Convert to CMS';
        analyzeBtn.textContent = '🔍 Quick Analyze';
    }
}

// Display error message
function displayError(message) {
    document.getElementById('output').innerHTML = 
        `<div class="error-message">
            <strong>❌ Error:</strong><br>
            ${message}
            <br><br>
            <small>Make sure the backend server is running: <code>python backend/app.py</code></small>
        </div>`;
}

// Show temporary message
function showMessage(message, type) {
    const className = type === 'success' ? 'success-message' : 'error-message';
    const output = document.getElementById('output');
    const msgDiv = document.createElement('div');
    msgDiv.className = className;
    msgDiv.textContent = message;
    output.insertBefore(msgDiv, output.firstChild);
    
    setTimeout(() => {
        msgDiv.style.opacity = '0';
        msgDiv.style.transform = 'translateY(-10px)';
        setTimeout(() => msgDiv.remove(), 300);
    }, 3000);
}

// Escape HTML for safe display
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Format file size
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' bytes';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    else return (bytes / 1048576).toFixed(1) + ' MB';
}

// Log app info to console
console.log('%c🚀 HTML to CMS Converter', 'color: #667eea; font-size: 20px; font-weight: bold;');
console.log('%cVersion: 3.0', 'color: #666;');
console.log('%cAPI URL: ' + API_URL, 'color: #666;');
#!/usr/bin/env python3
"""
Export Knowledge Base

Exports the knowledge base to various formats:
- markdown: Copy files with relative link conversion and index
- html: Static website with navigation, CSS, and search
- pdf: Single PDF document with table of contents
- obsidian: Obsidian vault format with wiki-style links

Usage:
    python export_knowledge_base.py <project_dir> [format] [options]

Examples:
    python export_knowledge_base.py /path/to/project
    python export_knowledge_base.py /path/to/project html
    python export_knowledge_base.py /path/to/project pdf --output=/tmp/export
    python export_knowledge_base.py /path/to/project --include=wiki,definitions
"""

import argparse
import json
import logging
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install PyYAML")
    sys.exit(1)

try:
    import markdown
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    from markdown.extensions.toc import TocExtension
except ImportError:
    markdown = None

# Optional dependencies
try:
    from weasyprint import HTML as WeasyHTML
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import HtmlFormatter
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False


# =============================================================================
# Embedded Templates
# =============================================================================

CSS_STYLES = '''
:root {
    --bg: #ffffff;
    --bg-secondary: #f8f9fa;
    --text: #212529;
    --text-muted: #6c757d;
    --sidebar-bg: #f1f3f5;
    --sidebar-width: 280px;
    --link: #0066cc;
    --link-hover: #004499;
    --border: #dee2e6;
    --accent: #228be6;
    --code-bg: #f4f4f4;
    --success: #40c057;
    --warning: #fab005;
    --danger: #fa5252;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg: #1a1b1e;
        --bg-secondary: #25262b;
        --text: #c1c2c5;
        --text-muted: #909296;
        --sidebar-bg: #141517;
        --link: #74c0fc;
        --link-hover: #a5d8ff;
        --border: #373a40;
        --accent: #339af0;
        --code-bg: #2c2e33;
    }
}

* {
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    background: var(--bg);
    color: var(--text);
}

/* Sidebar */
.sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: var(--sidebar-width);
    height: 100vh;
    background: var(--sidebar-bg);
    border-right: 1px solid var(--border);
    overflow-y: auto;
    padding: 1.5rem;
    z-index: 100;
}

.sidebar h1 {
    font-size: 1.25rem;
    margin: 0 0 1rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}

.sidebar h1 a {
    color: var(--text);
    text-decoration: none;
}

/* Search */
.search-container {
    margin-bottom: 1.5rem;
}

.search-input {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 1px solid var(--border);
    border-radius: 4px;
    background: var(--bg);
    color: var(--text);
    font-size: 0.875rem;
}

.search-input:focus {
    outline: none;
    border-color: var(--accent);
}

.search-results {
    margin-top: 0.5rem;
    max-height: 300px;
    overflow-y: auto;
}

.search-result {
    padding: 0.5rem;
    border-radius: 4px;
    margin-bottom: 0.25rem;
}

.search-result:hover {
    background: var(--bg-secondary);
}

.search-result a {
    color: var(--link);
    text-decoration: none;
    display: block;
}

.search-result small {
    color: var(--text-muted);
    font-size: 0.75rem;
}

/* Navigation */
.nav-section {
    margin-bottom: 1.5rem;
}

.nav-section h2 {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin: 0 0 0.5rem 0;
}

.nav-section ul {
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav-section li {
    margin: 0.25rem 0;
}

.nav-section a {
    color: var(--text);
    text-decoration: none;
    font-size: 0.875rem;
    display: block;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.nav-section a:hover {
    background: var(--bg-secondary);
    color: var(--link);
}

.nav-section a.active {
    background: var(--accent);
    color: white;
}

/* Main content */
.content {
    margin-left: var(--sidebar-width);
    padding: 2rem 3rem;
    max-width: 900px;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    font-weight: 600;
    line-height: 1.3;
}

h1 { font-size: 2rem; margin-top: 0; }
h2 { font-size: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }
h3 { font-size: 1.25rem; }
h4 { font-size: 1rem; }

a {
    color: var(--link);
    text-decoration: none;
}

a:hover {
    color: var(--link-hover);
    text-decoration: underline;
}

p {
    margin: 1em 0;
}

/* Lists */
ul, ol {
    margin: 1em 0;
    padding-left: 2em;
}

li {
    margin: 0.25em 0;
}

/* Code */
code {
    font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace;
    font-size: 0.875em;
    background: var(--code-bg);
    padding: 0.2em 0.4em;
    border-radius: 3px;
}

pre {
    background: var(--code-bg);
    padding: 1rem;
    border-radius: 6px;
    overflow-x: auto;
    margin: 1em 0;
}

pre code {
    background: none;
    padding: 0;
}

/* Tables */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 1em 0;
}

th, td {
    border: 1px solid var(--border);
    padding: 0.5rem 0.75rem;
    text-align: left;
}

th {
    background: var(--bg-secondary);
    font-weight: 600;
}

tr:nth-child(even) {
    background: var(--bg-secondary);
}

/* Blockquotes */
blockquote {
    margin: 1em 0;
    padding: 0.5em 1em;
    border-left: 4px solid var(--accent);
    background: var(--bg-secondary);
    color: var(--text-muted);
}

blockquote p {
    margin: 0.5em 0;
}

/* Frontmatter display */
.frontmatter {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1rem;
    margin-bottom: 1.5rem;
    font-size: 0.875rem;
}

.frontmatter table {
    margin: 0;
    border: none;
}

.frontmatter td, .frontmatter th {
    border: none;
    padding: 0.25rem 0.5rem;
    background: transparent;
}

.frontmatter th {
    text-align: right;
    color: var(--text-muted);
    font-weight: normal;
    width: 120px;
}

/* Status badges */
.status {
    display: inline-block;
    padding: 0.2em 0.5em;
    border-radius: 3px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
}

.status-pending { background: var(--warning); color: #000; }
.status-in-progress { background: var(--accent); color: #fff; }
.status-completed, .status-done { background: var(--success); color: #fff; }
.status-blocked { background: var(--danger); color: #fff; }

/* Breadcrumb */
.breadcrumb {
    font-size: 0.875rem;
    color: var(--text-muted);
    margin-bottom: 1rem;
}

.breadcrumb a {
    color: var(--text-muted);
}

.breadcrumb a:hover {
    color: var(--link);
}

/* Footer */
.footer {
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    font-size: 0.875rem;
    color: var(--text-muted);
}

/* Print styles */
@media print {
    .sidebar {
        display: none;
    }
    .content {
        margin-left: 0;
        max-width: none;
    }
    a {
        color: inherit;
        text-decoration: underline;
    }
    .no-print {
        display: none;
    }
}

/* Responsive */
@media (max-width: 768px) {
    .sidebar {
        position: relative;
        width: 100%;
        height: auto;
        border-right: none;
        border-bottom: 1px solid var(--border);
    }
    .content {
        margin-left: 0;
        padding: 1rem;
    }
}
'''

SEARCH_JS = '''
(function() {
    let searchIndex = [];
    let searchInput = document.getElementById('search-input');
    let searchResults = document.getElementById('search-results');

    // Load search index
    fetch('search-index.json')
        .then(response => response.json())
        .then(data => {
            searchIndex = data;
        })
        .catch(err => console.error('Failed to load search index:', err));

    function search(query) {
        if (!query || query.length < 2) {
            searchResults.innerHTML = '';
            return;
        }

        query = query.toLowerCase();
        let results = searchIndex.filter(item => {
            return item.title.toLowerCase().includes(query) ||
                   item.content.toLowerCase().includes(query) ||
                   (item.tags && item.tags.some(tag => tag.toLowerCase().includes(query)));
        }).slice(0, 10);

        if (results.length === 0) {
            searchResults.innerHTML = '<div class="search-result"><small>No results found</small></div>';
            return;
        }

        searchResults.innerHTML = results.map(item => {
            return `<div class="search-result">
                <a href="${item.url}">${item.title}</a>
                <small>${item.category}</small>
            </div>`;
        }).join('');
    }

    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            search(e.target.value);
        });
    }
})();
'''

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Knowledge Base</title>
    <link rel="stylesheet" href="{css_path}">
</head>
<body>
    <nav class="sidebar">
        <h1><a href="{index_path}">Knowledge Base</a></h1>
        <div class="search-container">
            <input type="text" id="search-input" class="search-input" placeholder="Search...">
            <div id="search-results" class="search-results"></div>
        </div>
        {navigation}
    </nav>
    <main class="content">
        <div class="breadcrumb">
            <a href="{index_path}">Home</a> / <a href="{category_path}">{category}</a> / {title}
        </div>
        {frontmatter_html}
        <article>
            {content}
        </article>
        <footer class="footer">
            Exported with Project Analysis Framework on {export_date}
        </footer>
    </main>
    <script src="{js_path}"></script>
</body>
</html>
'''

INDEX_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Knowledge Base</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <nav class="sidebar">
        <h1><a href="index.html">Knowledge Base</a></h1>
        <div class="search-container">
            <input type="text" id="search-input" class="search-input" placeholder="Search...">
            <div id="search-results" class="search-results"></div>
        </div>
        {navigation}
    </nav>
    <main class="content">
        <h1>Knowledge Base</h1>
        <p><strong>Exported:</strong> {export_date}<br>
        <strong>Source:</strong> {source_path}</p>

        <h2>Contents</h2>
        {sections}

        <footer class="footer">
            Exported with Project Analysis Framework
        </footer>
    </main>
    <script src="js/search.js"></script>
</body>
</html>
'''

PDF_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Knowledge Base</title>
    <style>
        {css}

        @page {{
            size: A4;
            margin: 2cm;
            @bottom-center {{
                content: counter(page);
            }}
        }}

        body {{
            font-size: 11pt;
        }}

        .sidebar {{
            display: none;
        }}

        .content {{
            margin: 0;
            max-width: none;
        }}

        .page-break {{
            page-break-after: always;
        }}

        .toc {{
            page-break-after: always;
        }}

        .toc h2 {{
            margin-top: 2em;
        }}

        .toc ul {{
            list-style: none;
            padding-left: 0;
        }}

        .toc li {{
            margin: 0.5em 0;
        }}

        .toc a {{
            color: inherit;
            text-decoration: none;
        }}

        .section-header {{
            page-break-before: always;
            margin-top: 0;
        }}

        .article {{
            page-break-inside: avoid;
            margin-bottom: 2em;
        }}

        h1, h2, h3 {{
            page-break-after: avoid;
        }}

        table, pre, blockquote {{
            page-break-inside: avoid;
        }}
    </style>
</head>
<body>
    <div class="content">
        <h1>Knowledge Base</h1>
        <p><strong>Exported:</strong> {export_date}<br>
        <strong>Source:</strong> {source_path}</p>

        <div class="toc">
            <h2>Table of Contents</h2>
            {toc}
        </div>

        {content}
    </div>
</body>
</html>
'''

OBSIDIAN_CONFIG = {
    "app.json": {
        "showViewHeader": True
    },
    "appearance.json": {
        "accentColor": ""
    },
    "core-plugins.json": [
        "file-explorer",
        "global-search",
        "graph",
        "backlink",
        "outgoing-link",
        "tag-pane",
        "page-preview",
        "note-composer",
        "command-palette",
        "markdown-importer",
        "editor-status",
        "starred",
        "outline"
    ],
    "graph.json": {
        "collapse-filter": False,
        "search": "",
        "showTags": True,
        "showAttachments": False,
        "hideUnresolved": False,
        "showOrphans": True,
        "collapse-color-groups": False,
        "colorGroups": [],
        "collapse-display": False,
        "lineSizeMultiplier": 1,
        "nodeSizeMultiplier": 1,
        "showArrow": False,
        "textFadeMultiplier": 0,
        "centerStrength": 0.518713,
        "repelStrength": 10,
        "linkStrength": 1,
        "linkDistance": 250,
        "scale": 1,
        "close": True
    }
}


# =============================================================================
# Core Classes
# =============================================================================

class KnowledgeFile:
    """Represents a single knowledge base file."""

    def __init__(self, path: Path, kb_dir: Path):
        self.path = path
        self.kb_dir = kb_dir
        self.relative_path = path.relative_to(kb_dir)
        self.category = self.relative_path.parts[0] if len(self.relative_path.parts) > 1 else 'root'
        self.frontmatter = {}
        self.content = ''
        self.title = path.stem.replace('-', ' ').title()

        self._parse()

    def _parse(self):
        """Parse frontmatter and content from file."""
        text = self.path.read_text(encoding='utf-8')

        # Parse YAML frontmatter
        if text.startswith('---'):
            parts = text.split('---', 2)
            if len(parts) >= 3:
                try:
                    self.frontmatter = yaml.safe_load(parts[1]) or {}
                    self.content = parts[2].strip()
                except yaml.YAMLError:
                    self.content = text
            else:
                self.content = text
        else:
            self.content = text

        # Extract title from frontmatter or first heading
        if 'title' in self.frontmatter:
            self.title = self.frontmatter['title']
        else:
            # Try to find first heading
            match = re.search(r'^#\s+(.+)$', self.content, re.MULTILINE)
            if match:
                self.title = match.group(1).strip()


class KnowledgeBaseExporter:
    """Main exporter class that handles all formats."""

    CATEGORIES = ['meetings', 'tasks', 'people', 'definitions', 'wiki', 'project-status', 'jira-drafts']
    CATEGORY_TITLES = {
        'meetings': 'Meetings',
        'tasks': 'Tasks',
        'people': 'People',
        'definitions': 'Definitions',
        'wiki': 'Wiki',
        'project-status': 'Project Status',
        'jira-drafts': 'JIRA Drafts'
    }

    def __init__(self, project_dir: Path, output_dir: Optional[Path] = None,
                 include_dirs: Optional[list] = None, exclude_dirs: Optional[list] = None):
        self.project_dir = project_dir
        self.kb_dir = project_dir / 'knowledge'
        self.output_dir = output_dir or (project_dir / 'exports')
        self.include_dirs = include_dirs
        self.exclude_dirs = exclude_dirs or []
        self.files: list[KnowledgeFile] = []
        self.logger = logging.getLogger('export')

        # Validate
        if not self.kb_dir.exists():
            raise ValueError(f"Knowledge base directory not found: {self.kb_dir}")

    def collect_files(self) -> list[KnowledgeFile]:
        """Gather all markdown files from knowledge/, respecting include/exclude."""
        self.files = []

        # Determine which directories to process
        dirs_to_process = self.include_dirs if self.include_dirs else self.CATEGORIES
        dirs_to_process = [d for d in dirs_to_process if d not in self.exclude_dirs]

        for category in dirs_to_process:
            category_dir = self.kb_dir / category
            if not category_dir.exists():
                continue

            for md_file in category_dir.glob('**/*.md'):
                try:
                    kf = KnowledgeFile(md_file, self.kb_dir)
                    self.files.append(kf)
                except Exception as e:
                    self.logger.warning(f"Failed to parse {md_file}: {e}")

        # Sort by category then title
        self.files.sort(key=lambda f: (f.category, f.title.lower()))
        self.logger.info(f"Collected {len(self.files)} files")
        return self.files

    def _convert_wiki_links(self, content: str, format: str, current_file: KnowledgeFile) -> str:
        """Convert [[wiki-links]] based on export format."""
        pattern = re.compile(r'\[\[([^\]]+)\]\]')

        def replace_link(match):
            name = match.group(1)
            slug = name.lower().replace(' ', '-')

            # Try to find the actual file
            for subdir in self.CATEGORIES:
                candidate = self.kb_dir / subdir / f"{slug}.md"
                if candidate.exists():
                    if format == 'html':
                        # Calculate relative path
                        depth = len(current_file.relative_path.parts) - 1
                        prefix = '../' * depth if depth > 0 else ''
                        return f'<a href="{prefix}{subdir}/{slug}.html">{name}</a>'
                    elif format == 'markdown':
                        depth = len(current_file.relative_path.parts) - 1
                        prefix = '../' * depth if depth > 0 else ''
                        return f'[{name}]({prefix}{subdir}/{slug}.md)'
                    elif format == 'obsidian':
                        return f'[[{slug}]]'
                    elif format == 'pdf':
                        return f'<a href="#{slug}">{name}</a>'

            # Not found - return as plain text with indication
            self.logger.debug(f"Wiki link not found: [[{name}]]")
            return name

        return pattern.sub(replace_link, content)

    def _convert_relative_links(self, content: str, format: str, current_file: KnowledgeFile) -> str:
        """Convert relative markdown links based on format."""
        pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')

        def replace_link(match):
            text = match.group(1)
            path = match.group(2)

            if format == 'html':
                html_path = path.replace('.md', '.html')
                return f'[{text}]({html_path})'
            elif format == 'pdf':
                # Convert to anchor link
                slug = Path(path).stem
                return f'[{text}](#{slug})'
            else:
                return match.group(0)

        return pattern.sub(replace_link, content)

    def _markdown_to_html(self, content: str, frontmatter: dict = None) -> str:
        """Convert markdown content to HTML."""
        if markdown is None:
            raise ImportError("markdown library is required for HTML export. Install with: pip install markdown")

        # Extensions for better markdown support
        extensions = [
            'tables',
            'fenced_code',
            'toc',
            'nl2br',
            'sane_lists',
        ]

        if PYGMENTS_AVAILABLE:
            extensions.append('codehilite')

        md = markdown.Markdown(extensions=extensions)
        html = md.convert(content)

        return html

    def _generate_navigation(self, format: str = 'html', current_file: KnowledgeFile = None) -> str:
        """Generate navigation sidebar HTML."""
        nav_html = []

        # Group files by category
        by_category = {}
        for f in self.files:
            if f.category not in by_category:
                by_category[f.category] = []
            by_category[f.category].append(f)

        for category in self.CATEGORIES:
            if category not in by_category:
                continue

            files = by_category[category]
            title = self.CATEGORY_TITLES.get(category, category.title())

            nav_html.append(f'<div class="nav-section">')
            nav_html.append(f'<h2>{title} ({len(files)})</h2>')
            nav_html.append('<ul>')

            for f in files:
                # Calculate relative path
                if current_file:
                    depth = len(current_file.relative_path.parts) - 1
                    prefix = '../' * depth if depth > 0 else ''
                else:
                    prefix = ''

                href = f'{prefix}{f.category}/{f.path.stem}.html'
                active = ' class="active"' if current_file and f.path == current_file.path else ''
                nav_html.append(f'<li><a href="{href}"{active}>{f.title}</a></li>')

            nav_html.append('</ul>')
            nav_html.append('</div>')

        return '\n'.join(nav_html)

    def _generate_search_index(self) -> list[dict]:
        """Generate JSON search index for HTML export."""
        index = []

        for f in self.files:
            # Get first 200 chars of content for preview
            preview = f.content[:200].replace('\n', ' ').strip()
            if len(f.content) > 200:
                preview += '...'

            entry = {
                'title': f.title,
                'url': f'{f.category}/{f.path.stem}.html',
                'category': self.CATEGORY_TITLES.get(f.category, f.category.title()),
                'content': preview,
                'tags': f.frontmatter.get('tags', [])
            }
            index.append(entry)

        return index

    def _frontmatter_to_html(self, frontmatter: dict) -> str:
        """Convert frontmatter to displayable HTML."""
        if not frontmatter:
            return ''

        # Select important fields to display
        display_fields = ['type', 'status', 'date', 'assignee', 'priority', 'source', 'tags']
        rows = []

        for key in display_fields:
            if key in frontmatter:
                value = frontmatter[key]
                if isinstance(value, list):
                    value = ', '.join(str(v) for v in value)
                if key == 'status' and value:
                    value = f'<span class="status status-{value.lower().replace(" ", "-")}">{value}</span>'
                rows.append(f'<tr><th>{key.title()}</th><td>{value}</td></tr>')

        if not rows:
            return ''

        return f'<div class="frontmatter"><table>{"".join(rows)}</table></div>'

    def export_markdown(self) -> Path:
        """Export to markdown format with converted links and index."""
        timestamp = datetime.now().strftime('%Y-%m-%d')
        output_dir = self.output_dir / f'{timestamp}-export'
        output_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Exporting to markdown: {output_dir}")

        # Copy files with link conversion
        for f in self.files:
            # Create category directory
            category_dir = output_dir / f.category
            category_dir.mkdir(exist_ok=True)

            # Convert links
            content = self._convert_wiki_links(f.content, 'markdown', f)

            # Reconstruct file with frontmatter
            if f.frontmatter:
                output_content = f"---\n{yaml.dump(f.frontmatter, default_flow_style=False)}---\n\n{content}"
            else:
                output_content = content

            # Write file
            output_path = category_dir / f.path.name
            output_path.write_text(output_content, encoding='utf-8')

        # Generate index
        index_content = self._generate_markdown_index()
        (output_dir / 'README.md').write_text(index_content, encoding='utf-8')

        return output_dir

    def _generate_markdown_index(self) -> str:
        """Generate markdown index file."""
        lines = [
            '# Knowledge Base Export',
            '',
            f'**Exported:** {datetime.now().strftime("%B %d, %Y")}',
            f'**Source:** {self.project_dir}',
            '',
            '## Contents',
            ''
        ]

        # Group files by category
        by_category = {}
        for f in self.files:
            if f.category not in by_category:
                by_category[f.category] = []
            by_category[f.category].append(f)

        for category in self.CATEGORIES:
            if category not in by_category:
                continue

            files = by_category[category]
            title = self.CATEGORY_TITLES.get(category, category.title())

            lines.append(f'### [{title}]({category}/) ({len(files)} entries)')
            lines.append('')
            for f in files[:5]:  # Show first 5
                lines.append(f'- [{f.title}]({f.category}/{f.path.name})')
            if len(files) > 5:
                lines.append(f'- *...and {len(files) - 5} more*')
            lines.append('')

        lines.extend([
            '---',
            '',
            '*Exported with Project Analysis Framework*'
        ])

        return '\n'.join(lines)

    def export_html(self) -> Path:
        """Export to HTML with navigation, CSS, and search."""
        if markdown is None:
            raise ImportError("markdown library is required for HTML export. Install with: pip install markdown")

        timestamp = datetime.now().strftime('%Y-%m-%d')
        output_dir = self.output_dir / f'{timestamp}-html'
        output_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Exporting to HTML: {output_dir}")

        # Create directories
        (output_dir / 'css').mkdir(exist_ok=True)
        (output_dir / 'js').mkdir(exist_ok=True)

        # Write CSS and JS
        (output_dir / 'css' / 'style.css').write_text(CSS_STYLES, encoding='utf-8')
        (output_dir / 'js' / 'search.js').write_text(SEARCH_JS, encoding='utf-8')

        # Generate navigation
        nav_for_index = self._generate_navigation('html', None)

        # Process each file
        for f in self.files:
            # Create category directory
            category_dir = output_dir / f.category
            category_dir.mkdir(exist_ok=True)

            # Convert content
            content = self._convert_wiki_links(f.content, 'html', f)
            content = self._convert_relative_links(content, 'html', f)
            html_content = self._markdown_to_html(content, f.frontmatter)

            # Calculate paths
            depth = len(f.relative_path.parts) - 1
            prefix = '../' * depth if depth > 0 else ''

            # Generate navigation for this file
            nav = self._generate_navigation('html', f)

            # Render template
            html = HTML_TEMPLATE.format(
                title=f.title,
                css_path=f'{prefix}css/style.css',
                js_path=f'{prefix}js/search.js',
                index_path=f'{prefix}index.html',
                category_path=f'{prefix}{f.category}/index.html',
                category=self.CATEGORY_TITLES.get(f.category, f.category.title()),
                navigation=nav,
                frontmatter_html=self._frontmatter_to_html(f.frontmatter),
                content=html_content,
                export_date=datetime.now().strftime('%B %d, %Y')
            )

            # Write file
            output_path = category_dir / f'{f.path.stem}.html'
            output_path.write_text(html, encoding='utf-8')

        # Generate category index pages
        by_category = {}
        for f in self.files:
            if f.category not in by_category:
                by_category[f.category] = []
            by_category[f.category].append(f)

        for category, files in by_category.items():
            self._generate_category_index(output_dir, category, files)

        # Generate search index
        search_index = self._generate_search_index()
        (output_dir / 'search-index.json').write_text(
            json.dumps(search_index, indent=2), encoding='utf-8'
        )

        # Generate main index
        sections_html = self._generate_index_sections()
        index_html = INDEX_TEMPLATE.format(
            navigation=nav_for_index,
            export_date=datetime.now().strftime('%B %d, %Y'),
            source_path=str(self.project_dir),
            sections=sections_html
        )
        (output_dir / 'index.html').write_text(index_html, encoding='utf-8')

        return output_dir

    def _generate_category_index(self, output_dir: Path, category: str, files: list[KnowledgeFile]):
        """Generate index page for a category."""
        title = self.CATEGORY_TITLES.get(category, category.title())

        items = []
        for f in files:
            items.append(f'<li><a href="{f.path.stem}.html">{f.title}</a></li>')

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Knowledge Base</title>
    <link rel="stylesheet" href="../css/style.css">
</head>
<body>
    <nav class="sidebar">
        <h1><a href="../index.html">Knowledge Base</a></h1>
        <div class="search-container">
            <input type="text" id="search-input" class="search-input" placeholder="Search...">
            <div id="search-results" class="search-results"></div>
        </div>
        {self._generate_navigation('html', None)}
    </nav>
    <main class="content">
        <div class="breadcrumb">
            <a href="../index.html">Home</a> / {title}
        </div>
        <h1>{title}</h1>
        <p>{len(files)} entries</p>
        <ul>
            {"".join(items)}
        </ul>
        <footer class="footer">
            Exported with Project Analysis Framework on {datetime.now().strftime('%B %d, %Y')}
        </footer>
    </main>
    <script src="../js/search.js"></script>
</body>
</html>
'''
        (output_dir / category / 'index.html').write_text(html, encoding='utf-8')

    def _generate_index_sections(self) -> str:
        """Generate sections HTML for main index."""
        sections = []

        by_category = {}
        for f in self.files:
            if f.category not in by_category:
                by_category[f.category] = []
            by_category[f.category].append(f)

        for category in self.CATEGORIES:
            if category not in by_category:
                continue

            files = by_category[category]
            title = self.CATEGORY_TITLES.get(category, category.title())

            items = []
            for f in files[:5]:
                items.append(f'<li><a href="{f.category}/{f.path.stem}.html">{f.title}</a></li>')
            if len(files) > 5:
                items.append(f'<li><a href="{category}/index.html"><em>...and {len(files) - 5} more</em></a></li>')

            sections.append(f'''
<h3><a href="{category}/index.html">{title}</a> ({len(files)} entries)</h3>
<ul>
    {"".join(items)}
</ul>
''')

        return '\n'.join(sections)

    def export_pdf(self) -> Path:
        """Export to single PDF document."""
        if not WEASYPRINT_AVAILABLE:
            raise ImportError(
                "weasyprint is required for PDF export.\n"
                "Install with: pip install weasyprint\n"
                "Note: weasyprint requires system dependencies. See: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html"
            )

        if markdown is None:
            raise ImportError("markdown library is required for PDF export. Install with: pip install markdown")

        timestamp = datetime.now().strftime('%Y-%m-%d')
        output_dir = self.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f'{timestamp}-knowledge-base.pdf'

        self.logger.info(f"Exporting to PDF: {output_path}")

        # Generate TOC
        toc_items = []
        by_category = {}
        for f in self.files:
            if f.category not in by_category:
                by_category[f.category] = []
            by_category[f.category].append(f)

        for category in self.CATEGORIES:
            if category not in by_category:
                continue

            files = by_category[category]
            title = self.CATEGORY_TITLES.get(category, category.title())

            toc_items.append(f'<li><strong>{title}</strong><ul>')
            for f in files:
                slug = f.path.stem
                toc_items.append(f'<li><a href="#{slug}">{f.title}</a></li>')
            toc_items.append('</ul></li>')

        toc_html = f'<ul>{"".join(toc_items)}</ul>'

        # Generate content
        content_sections = []
        for category in self.CATEGORIES:
            if category not in by_category:
                continue

            files = by_category[category]
            title = self.CATEGORY_TITLES.get(category, category.title())

            content_sections.append(f'<h2 class="section-header">{title}</h2>')

            for f in files:
                slug = f.path.stem

                # Convert content
                content = self._convert_wiki_links(f.content, 'pdf', f)
                content = self._convert_relative_links(content, 'pdf', f)
                html_content = self._markdown_to_html(content, f.frontmatter)

                content_sections.append(f'''
<div class="article" id="{slug}">
    <h3>{f.title}</h3>
    {html_content}
</div>
''')

        # Render full PDF HTML
        pdf_html = PDF_TEMPLATE.format(
            css=CSS_STYLES,
            export_date=datetime.now().strftime('%B %d, %Y'),
            source_path=str(self.project_dir),
            toc=toc_html,
            content='\n'.join(content_sections)
        )

        # Generate PDF
        html_doc = WeasyHTML(string=pdf_html)
        html_doc.write_pdf(output_path)

        return output_path

    def export_obsidian(self) -> Path:
        """Export to Obsidian vault format."""
        timestamp = datetime.now().strftime('%Y-%m-%d')
        output_dir = self.output_dir / f'{timestamp}-obsidian'
        output_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Exporting to Obsidian: {output_dir}")

        # Create .obsidian config
        obsidian_dir = output_dir / '.obsidian'
        obsidian_dir.mkdir(exist_ok=True)

        for filename, config in OBSIDIAN_CONFIG.items():
            config_path = obsidian_dir / filename
            config_path.write_text(json.dumps(config, indent=2), encoding='utf-8')

        # Copy files with Obsidian formatting
        for f in self.files:
            # Create category directory (Title Case for Obsidian)
            category_title = self.CATEGORY_TITLES.get(f.category, f.category.title())
            category_dir = output_dir / category_title
            category_dir.mkdir(exist_ok=True)

            # Keep wiki links as-is (Obsidian native)
            content = f.content

            # Convert tags to Obsidian format if needed
            if 'tags' in f.frontmatter and isinstance(f.frontmatter['tags'], list):
                # Ensure tags are in #tag format in content
                pass  # Tags in frontmatter work in Obsidian

            # Reconstruct file with frontmatter
            if f.frontmatter:
                output_content = f"---\n{yaml.dump(f.frontmatter, default_flow_style=False)}---\n\n{content}"
            else:
                output_content = content

            # Write file
            output_path = category_dir / f.path.name
            output_path.write_text(output_content, encoding='utf-8')

        # Generate Index.md
        index_content = self._generate_obsidian_index()
        (output_dir / 'Index.md').write_text(index_content, encoding='utf-8')

        return output_dir

    def _generate_obsidian_index(self) -> str:
        """Generate Obsidian index file with wiki links."""
        lines = [
            '# Knowledge Base',
            '',
            f'**Exported:** {datetime.now().strftime("%B %d, %Y")}',
            f'**Source:** `{self.project_dir}`',
            '',
            '## Contents',
            ''
        ]

        # Group files by category
        by_category = {}
        for f in self.files:
            if f.category not in by_category:
                by_category[f.category] = []
            by_category[f.category].append(f)

        for category in self.CATEGORIES:
            if category not in by_category:
                continue

            files = by_category[category]
            title = self.CATEGORY_TITLES.get(category, category.title())

            lines.append(f'### {title} ({len(files)})')
            lines.append('')
            for f in files:
                # Use Obsidian wiki-link format
                lines.append(f'- [[{title}/{f.path.stem}|{f.title}]]')
            lines.append('')

        return '\n'.join(lines)

    def export(self, format: str) -> Path:
        """Export to specified format."""
        format = format.lower()

        if not self.files:
            self.collect_files()

        if format == 'markdown':
            return self.export_markdown()
        elif format == 'html':
            return self.export_html()
        elif format == 'pdf':
            return self.export_pdf()
        elif format == 'obsidian':
            return self.export_obsidian()
        else:
            raise ValueError(f"Unknown format: {format}")

    def get_summary(self) -> dict:
        """Get export summary statistics."""
        by_category = {}
        for f in self.files:
            if f.category not in by_category:
                by_category[f.category] = 0
            by_category[f.category] += 1

        return {
            'total_files': len(self.files),
            'by_category': by_category
        }


# =============================================================================
# CLI Interface
# =============================================================================

def setup_logging(log_dir: Optional[Path] = None, verbose: bool = False):
    """Configure logging."""
    level = logging.DEBUG if verbose else logging.INFO

    handlers = [logging.StreamHandler()]

    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f'export-{datetime.now().strftime("%Y-%m-%d")}.log'
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )


def main():
    parser = argparse.ArgumentParser(
        description='Export knowledge base to various formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s /path/to/project                  # Markdown export to exports/
  %(prog)s /path/to/project html             # HTML static site
  %(prog)s /path/to/project pdf              # Single PDF document
  %(prog)s /path/to/project obsidian         # Obsidian vault
  %(prog)s /path/to/project html -o ~/Desktop
  %(prog)s /path/to/project --include=wiki,definitions
'''
    )

    parser.add_argument('project_dir', type=Path, help='Project directory containing knowledge/')
    parser.add_argument('format', nargs='?', default='markdown',
                        choices=['markdown', 'html', 'pdf', 'obsidian'],
                        help='Export format (default: markdown)')
    parser.add_argument('-o', '--output', type=Path, help='Output directory (default: exports/)')
    parser.add_argument('--include', type=str,
                        help='Comma-separated directories to include (e.g., wiki,definitions)')
    parser.add_argument('--exclude', type=str,
                        help='Comma-separated directories to exclude')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Parse include/exclude
    include_dirs = args.include.split(',') if args.include else None
    exclude_dirs = args.exclude.split(',') if args.exclude else None

    # Setup logging
    log_dir = args.project_dir / 'logs' if args.project_dir.exists() else None
    setup_logging(log_dir, args.verbose)

    logger = logging.getLogger('export')

    try:
        # Create exporter
        exporter = KnowledgeBaseExporter(
            project_dir=args.project_dir,
            output_dir=args.output,
            include_dirs=include_dirs,
            exclude_dirs=exclude_dirs
        )

        # Collect files
        print(f"Collecting files from {exporter.kb_dir}...")
        exporter.collect_files()

        if not exporter.files:
            print("No files found in knowledge base.")
            return 1

        # Export
        print(f"Exporting to {args.format}...")
        output_path = exporter.export(args.format)

        # Summary
        summary = exporter.get_summary()

        print()
        print("Export Complete!")
        print()
        print(f"Format: {args.format.upper()}")
        print(f"Location: {output_path}")
        print(f"Files: {summary['total_files']}")
        print()
        print("Contents:")
        for category, count in summary['by_category'].items():
            title = KnowledgeBaseExporter.CATEGORY_TITLES.get(category, category.title())
            print(f"  - {count} {title.lower()}")
        print()

        if args.format == 'html':
            print("Open in browser:")
            print(f"  open {output_path / 'index.html'}")
        elif args.format == 'pdf':
            print("Open PDF:")
            print(f"  open {output_path}")
        elif args.format == 'obsidian':
            print("Open in Obsidian:")
            print(f"  Open {output_path} as vault")

        return 0

    except ImportError as e:
        print(f"Error: {e}")
        return 1
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        logger.exception("Export failed")
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())

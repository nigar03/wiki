import re
import markdown2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
from django.conf import settings

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry (title, content):
    # Save the content of a specific entry
    entries_dir = os.path.join(settings.BASE_DIR, 'entries')
    if not os.path.exists(entries_dir):
        os.makedirs(entries_dir)

    file_path = os.path.join(entries_dir, f"{title}.md")
    with open(file_path, 'w') as file:
        file.write(content)



def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
# utils.py

def get_entry_content(title):
    # Get the content of a specific entry
    file_path = os.path.join(settings.BASE_DIR, 'entries', f"{title}.md")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    return ""
# utils.py
def get_all_entries():
    # Return a list of all entry titles
    entries_dir = os.path.join(settings.BASE_DIR, 'entries')
    if not os.path.exists(entries_dir):
        return []
    entries = [filename[:-3] for filename in os.listdir(entries_dir) if filename.endswith('.md')]
    return entries

def convert_markdown_to_html(markdown_text):
    return markdown2.markdown(markdown_text)


def convert_markdown_to_html(markdown_text):
    # Convert Markdown headings
    html = re.sub(r'^(#{1,6})\s*(.+)$', lambda m: f'<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>',
                  markdown_text, flags=re.MULTILINE)

    # Convert Markdown bold text
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)

    # Convert Markdown unordered lists
    html = re.sub(r'^\*\s*(.+)$', r'<ul><li>\1</li></ul>', html, flags=re.MULTILINE)
    html = re.sub(r'</ul>\s*<ul>', '', html)

    # Convert Markdown links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)

    # Convert Markdown paragraphs
    html = re.sub(r'\n\n', '</p>\n<p>', html)
    html = f'<p>{html}</p>'

    return html

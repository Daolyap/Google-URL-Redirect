from flask import Flask, render_template, abort
import markdown
import os

app = Flask(__name__)

# Configuration
MARKDOWN_FILE_PATH = 'site.md' # Path to your markdown file
# For more advanced Markdown features like tables, fenced code blocks:
MARKDOWN_EXTENSIONS = ['extra', 'fenced_code', 'tables', 'codehilite']
# To use 'codehilite', you might also need Pygments: pip install Pygments
# And corresponding CSS for code highlighting (see static/style.css for basic example)

@app.route('/')
def index():
    try:
        with open(MARKDOWN_FILE_PATH, 'r', encoding='utf-8') as f:
            md_text = f.read()
    except FileNotFoundError:
        print(f"Error: Markdown file not found at {os.path.abspath(MARKDOWN_FILE_PATH)}")
        abort(404, description="Markdown file not found.")
    except Exception as e:
        print(f"Error reading markdown file: {e}")
        abort(500, description="Error reading markdown file.")

    html_content = markdown.markdown(md_text, extensions=MARKDOWN_EXTENSIONS)
    return render_template('view_markdown.html', content=html_content)

@app.route('/<path:filename>')
def serve_markdown_dynamically(filename):
    # Basic security: ensure filename ends with .md and is in a safe directory
    # For a production app, you'd want more robust path validation!
    if not filename.endswith('.md'):
        abort(404, "Only .md files are allowed.")

    # Construct the full path. Be careful with user-provided paths.
    # For simplicity, assume files are in the same directory as app.py
    # Or a designated 'markdown_docs' subdirectory.
    file_path = os.path.join('.', filename) # Adjust if your .md files are elsewhere

    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        print(f"Error: Markdown file not found at {os.path.abspath(file_path)}")
        abort(404, description=f"Markdown file '{filename}' not found.")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            md_text = f.read()
    except Exception as e:
        print(f"Error reading markdown file {filename}: {e}")
        abort(500, description=f"Error reading markdown file '{filename}'.")

    html_content = markdown.markdown(md_text, extensions=MARKDOWN_EXTENSIONS)
    return render_template('view_markdown.html', title=filename, content=html_content)


if __name__ == '__main__':
    # Check if the markdown file exists before starting
    if not os.path.exists(MARKDOWN_FILE_PATH):
        print(f"Warning: Default markdown file '{MARKDOWN_FILE_PATH}' not found.")
        print("Please create it or ensure the path is correct.")
        # You could create a dummy file here for testing:
        # with open(MARKDOWN_FILE_PATH, 'w') as f:
        #     f.write("# Default File\n\nThis is a placeholder.")

    app.run(debug=True, host='192.168.1.99', port=5000)
    # host='0.0.0.0' makes it accessible from other devices on your network
    # debug=True is for development, disable for production
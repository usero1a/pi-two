from flask import Flask, render_template_string  # type: ignore
import re

app = Flask(__name__)

def render_pyx(pyx_file_path):
    with open(pyx_file_path, 'r') as f:
        content = f.read()

    # Extract and separate HTML, CSS, and Python components
    html_content = re.search(r"<html>(.*?)</html>", content, re.DOTALL).group(1)
    css_content = re.search(r"<css>(.*?)</css>", content, re.DOTALL).group(1)
    python_code = re.search(r"<python>(.*?)</python>", content, re.DOTALL).group(1)

    # Execute Python code and get variables for the HTML rendering
    exec_globals = {}
    exec(python_code, exec_globals)
    
    # Render HTML with injected Python variables
    template = f"""
    <html>
      <style>{css_content}</style>
      {html_content}
    </html>
    """
    return render_template_string(template, **exec_globals)

@app.route('/')
def home():
    return render_pyx('index.pyx')

if __name__ == '__main__':
    app.run(debug=True)

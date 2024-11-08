import re

def parse_pyx(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Extract the HTML, CSS, and Python sections
    html_match = re.search(r"<html>(.*?)</html>", content, re.DOTALL)
    css_match = re.search(r"<css>(.*?)</css>", content, re.DOTALL)
    python_code_match = re.search(r"<python>(.*?)</python>", content, re.DOTALL)

    # Prepare dictionary for Python variables
    local_vars = {}

    # Execute Python code if found
    if python_code_match:
        python_code = python_code_match.group(1)
        exec(python_code, {}, local_vars)  # Executes Python code and stores variables in local_vars

    # Replace placeholders in HTML with Python variables
    if html_match:
        html_content = html_match.group(1)
        for key, value in local_vars.items():
            placeholder = f"{{{{ {key} }}}}"  # Matches {{ key }}
            html_content = html_content.replace(placeholder, str(value))  # Replace with variable value

    # Combine HTML and CSS content
    css_content = css_match.group(1) if css_match else ""
    result = f"<style>{css_content}</style>{html_content}" if html_match else "No content found."

    return result

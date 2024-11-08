import re

def parse_pyx(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

  
    html_match = re.search(r"<html>(.*?)</html>", content, re.DOTALL)
    css_match = re.search(r"<css>(.*?)</css>", content, re.DOTALL)
    python_code_match = re.search(r"<python>(.*?)</python>", content, re.DOTALL)


    local_vars = {}

    if python_code_match:
        python_code = python_code_match.group(1)
        exec(python_code, {}, local_vars)  

  
    if html_match:
        html_content = html_match.group(1)
        for key, value in local_vars.items():
            placeholder = f"{{{{ {key} }}}}"  
            html_content = html_content.replace(placeholder, str(value)) 


    css_content = css_match.group(1) if css_match else ""
    result = f"<style>{css_content}</style>{html_content}" if html_match else "No content found."

    return result

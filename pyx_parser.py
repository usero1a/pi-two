import re

def parse_pyx(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    html = re.search(r"<html>(.*?)</html>", content, re.DOTALL)
    css = re.search(r"<css>(.*?)</css>", content, re.DOTALL)
    python_code = re.search(r"<python>(.*?)</python>", content, re.DOTALL)
    
    # Execute Python code if found
    if python_code:
        exec(python_code.group(1))

    return f"<style>{css.group(1)}</style>{html.group(1)}" if html and css else html.group(1)

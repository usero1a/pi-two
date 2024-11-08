import re

class PyxTemplate:
    def __init__(self, file_path):
        self.file_path = file_path
        self.html_content = ""
        self.css_content = ""
        self.python_code = ""
        self.context = {}

    def load_file(self):
        """Loads the .pyx file and extracts <html>, <css>, and <python> sections."""
        with open(self.file_path, 'r') as f:
            content = f.read()

        # Extract HTML, CSS, and Python sections using regex
        self.html_content = re.search(r"<html>(.*?)</html>", content, re.DOTALL)
        self.css_content = re.search(r"<css>(.*?)</css>", content, re.DOTALL)
        self.python_code = re.search(r"<python>(.*?)</python>", content, re.DOTALL)

        # Use the matched groups or default to empty strings if not found
        self.html_content = self.html_content.group(1).strip() if self.html_content else ""
        self.css_content = self.css_content.group(1).strip() if self.css_content else ""
        self.python_code = self.python_code.group(1).strip() if self.python_code else ""

    def execute_python_code(self):
        """Executes the <python> section and stores the results in a context dictionary."""
        exec_globals = {}
        try:
            exec(self.python_code, exec_globals)
        except Exception as e:
            print(f"Error executing Python code in .pyx file: {e}")

        # Update the context with the variables defined in the Python section
        self.context.update(exec_globals)

    def render(self):
        """Renders the HTML with CSS and context variables."""
        # Embed CSS into the HTML
        full_html = f"""
        <html>
            <head>
                <style>{self.css_content}</style>
            </head>
            <body>
                {self.html_content}
            </body>
        </html>
        """
        return

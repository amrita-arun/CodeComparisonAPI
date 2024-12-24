import re
import pymupdf  # PyMuPDF
import ast
from rich.console import Console
from rich.text import Text
import difflib
from .function_extractor import parse_all_functions, get_code


def extract_text_with_pymupdf(file_path):
    doc = pymupdf.open(file_path)
    text = ""
    for page_num, page in enumerate(doc):
        text += page.get_text("text")
       # print(f"Page {page_num + 1} content:\n{page_text}\n{'-' * 40}")
        #text += page.get_text("text")  # Extracts text from the page
    #print("TEXT" + text)
    lines = text.split("\n")
    doc.close()
    return lines

def extract_code_snippets(lines):
    #print(lines)
    tags = ["def", "class", "import", "from", "#", "@", ":", "if", "elif", "else", "for", "while", "try", "except", "with", "return", "yield", "raise", "lambda", "pass", "(", ")", ]
    code_snippets = []
#    doc = pymupdf.open(file_path)
 #   for line in lines:
  #      lines = page.get_text().split("\n")
    for line in lines:
        line = line.split()
        #print(line)
        if re.match(r"^def\s+\w+\(.*\):", str(line)):  # Function definition
            #print(line)
            code_snippets.append(line)
        elif re.match(r"^class\s+\w+(\(.*\))?:", str(line)):  # Class definition
            #print(line)
            code_snippets.append(line)
        elif re.match(r"^(import|from)\s+\w+", str(line)):  # Import statements
            #print(line)
            code_snippets.append(line)
        elif re.match(r"^#.*", str(line)):  # Comments
            #print(line)
            code_snippets.append(line)
        elif re.match(r"^@.*", str(line)):  # Decorators
            #print(line)
            code_snippets.append(line)
        elif re.match(r"^\s*\w+\s*=", str(line)) and not re.match(
                r"^\s*(if|for|while|try|except|return|with|else|elif|class|def)", str(line)):  # Assignments
            #print(line)
            code_snippets.append(line)
        elif re.match(r"^\s*(if|for|while|try|except|with|return|yield|raise)\b", str(line)):  # Python keywords
            #print(line)
            code_snippets.append(line)
        elif "()" in str(line) or str(line).endswith(":"):  # Generic function calls or code blocks
            #print(line)
            code_snippets.append(line)
    return code_snippets

def parse_user_code(file_path):
    func_calls = parse_all_functions(file_path)
    return func_calls

def get_user_code(file_path):
    code = get_code(file_path)
    return code

def compare_snippets(snippets, user_code):
    '''
    unmatched_functions = [
        func for func in user_code["functions"] if func not in snippets
    ]
    unmatched_classes = [
        cls for cls in user_code["classes"] if cls not in snippets
    ]
    '''
    #print("snippets: " + str(snippets))
    foundSnippet = False
    unmatched_functions = []
    for func in user_code:
        if not foundSnippet:
            for snippetArray in snippets:
                if not foundSnippet:
                    for snippet in snippetArray:
                        if func in snippet:
                            foundSnippet = True
        if not foundSnippet:
            unmatched_functions.append(func)
        foundSnippet = False

    '''
    unmatched_functions = [
        func for func in user_code if func not in snippets.
    ]
    '''
    #return {"functions": unmatched_functions, "classes": unmatched_classes}
    return {"functions": unmatched_functions}
'''
def highlight_unmatched_code(unmatched):
    print("\nUnmatched Functions: ")
    for func in unmatched["functions"]:
        print(f"- {func}")
'''


'''
    print("\nUnmatched Classes: ")
    for cls in unmatched["classes"]:
        print(f"-{cls}")
        '''

'''
def highlight_diffs_in_terminal(unmatched):
    console = Console()

    #console.print("\n[bold red] Unmatched Functions:[\nbold red[")
    for func in unmatched["functions"]:
        text=Text(func, style="bold yellow")
        #console.print(text)

    console.print("\n[bold red]Unmatched Classes:[\bold red]")
    for cls in unmatched["classes"]:
        text = Text(cls, style="bold green")
        #console.print(text)

def generate_diff_report(extracted_snippets, user_code, output_file="diff_report.html"):
    """
    Generates a side-by-side HTML diff report comparing extracted snippets to user code.

    :param extracted_snippets: List of function/class names extracted from the PDF.
    :param user_code: Dictionary of functions and classes from the user's code.
    :param output_file: Path to save the diff report.
    """
    # Combine extracted snippets into one list
    pdf_snippets = [str(snippet) for snippet in extracted_snippets]  # Ensure strings

    # Combine user-defined code into one list
    #user_snippets = [str(snippet) for snippet in (user_code["functions"] + user_code["classes"])]  # Ensure strings
    user_snippets = [str(snippet) for snippet in user_code]  # Ensure strings

    # Generate HTML diff
    diff = difflib.HtmlDiff().make_file(
        fromlines=pdf_snippets,
        tolines=user_snippets,
        fromdesc="Extracted from PDF",
        todesc="User Code"
    )


    # Save the diff to an HTML file
    with open(output_file, "w") as f:
        f.write(diff)

    print(f"HTML diff report saved to {output_file}")
    '''

def get_unmatched_code(snippets, user_code_file_path):
    user_code = parse_user_code(user_code_file_path)
    unmatched = compare_snippets(snippets, user_code)
    return unmatched


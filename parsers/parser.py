import re
import pymupdf  # PyMuPDF
import ast
from .function_extractor import parse_all_functions, get_code


def extract_text_with_pymupdf(file_path):
    doc = pymupdf.open(file_path)
    text = ""
    for page_num, page in enumerate(doc):
        text += page.get_text("text")
    lines = text.split("\n")
    doc.close()
    return lines

def extract_code_snippets(lines):
    tags = ["def", "class", "import", "from", "#", "@", ":", "if", "elif", "else", "for", "while", "try", "except", "with", "return", "yield", "raise", "lambda", "pass", "(", ")", ]
    code_snippets = []

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

    #return {"functions": unmatched_functions, "classes": unmatched_classes}
    return {"functions": unmatched_functions}



def get_unmatched_code(snippets, user_code_file_path):
    user_code = parse_user_code(user_code_file_path)
    unmatched = compare_snippets(snippets, user_code)
    return unmatched


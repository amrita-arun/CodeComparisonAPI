from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from parsers.parser import extract_code_snippets, extract_text_with_pymupdf, get_user_code, get_unmatched_code

app = FastAPI()


@app.post("/parse-files")
async def parse_files(pdf: UploadFile = File(...), code: UploadFile = File(...)):
    pdf_path = f"/tmp/{pdf.filename}"
    code_path = f"/tmp/{code.filename}"

    with open(pdf_path, "wb") as f:
        f.write(await pdf.read())
    with open(code_path, "wb") as f:
        f.write(await code.read())

    pdf_lines = extract_text_with_pymupdf(pdf_path)
    pdf_snippets = extract_code_snippets(pdf_lines)
    #print(pdf_snippets)
    user_code = get_user_code(code_path)
    unmatched_code = get_unmatched_code(pdf_snippets, code_path)

    return {
        "pdfSnippets": pdf_snippets,
        "userCode": user_code,
        "unmatchedCode": unmatched_code
    }


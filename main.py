from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import uvicorn
from model import pdf_reader,analyze_resume

app=FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload_pdf/")
async def upload_pdf(text: str = Form(...), file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return {"error": "Only PDF files are allowed"}

    file_location = "uploaded_resume.pdf"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    resume=pdf_reader(file_location)
    ans=analyze_resume(text,resume)
    return ans

if __name__ == "__main__":
    while True:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    
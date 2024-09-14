from fastapi import FastAPI, File, UploadFile
import shutil
import uvicorn
import model

app=FastAPI()

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return {"error": "Only PDF files are allowed"}

    file_location = "uploaded_resume.pdf"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    resume=model.pdf_reader(file_location)
    ans=model.analyze_resume(resume)
    return ans

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
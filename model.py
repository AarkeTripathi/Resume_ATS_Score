from groq import Groq
import os
from pypdf import PdfReader

def pdf_reader(pdf):
    reader=PdfReader(pdf)
    print(reader)
    page=reader.pages[0]
    resume=page.extract_text()
    return resume

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def analyze_resume(resume):
    completion = client.chat.completions.create(
        model="llama3-groq-70b-8192-tool-use-preview",
        messages=[
            {
                "role": "user",
                "content": f"Give me the ATS score of the resume {resume} out of 100 (just the numerical answer dont show the analysis), and also some suggestions to improve the resume"
            }
        ],
        temperature=0.5,
        max_tokens=1024,
        top_p=0.65,
        stream=True,
        stop=None,
    )

    lst=[]
    for chunk in completion:
        lst.append(chunk.choices[0].delta.content or "")

    text=""
    for chunk in lst:
        text=text+chunk
    
    return text



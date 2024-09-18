from groq import Groq
import os
from pypdf import PdfReader
from dotenv import load_dotenv

def pdf_reader(pdf):
    reader=PdfReader(pdf)
    page=reader.pages[0]
    resume=page.extract_text()
    return resume

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def analyze_resume(job_desc,resume):
    completion = client.chat.completions.create(
        model="llama3-groq-70b-8192-tool-use-preview",
        messages=[
            {
                "role": "user",
                "content": f"Give me the ATS score of the resume {resume} out of 100 (just the numerical answer dont show the analysis) by takng the job description {job_desc}, and also give some suggestions to improve the resume"
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


# sample_job_desc="""Job Title: Flutter Developer

# Location: Gurugram Remote

# Job Type: Full-time

# About Us: Atreos is a dynamic and innovative tech company dedicated to building seamless and engaging mobile applications. We are looking for a talented Flutter Developer to join our team and contribute to the development of our next-generation mobile solutions.

# Key Responsibilities:

#     Develop and maintain high-performance mobile applications for both Android and iOS platforms using Flutter.
#     Collaborate with cross-functional teams to define, design, and ship new features.
#     Optimize applications for maximum performance, scalability, and user experience.
#     Debug, troubleshoot, and fix bugs in existing Flutter applications.
#     Write clean, well-documented, and efficient code that follows best practices and coding standards.
#     Stay up-to-date with the latest trends in mobile development, Flutter SDK updates, and related technologies.
#     Participate in code reviews and contribute to continuous improvements in the development process.

# Qualifications:

#     Proven experience as a Flutter Developer or in mobile development with Flutter.
#     Strong proficiency in Dart programming language.
#     Experience with third-party libraries and APIs integration.
#     Solid understanding of the full mobile development lifecycle.
#     Familiarity with RESTful APIs, JSON, and mobile app architectures (MVC, MVVM).
#     Knowledge of version control systems like Git.
#     Strong problem-solving and debugging skills.
#     Experience with native development (Android or iOS) is a plus.

# Nice-to-Have:

#     Experience with state management solutions like Provider, Bloc, or Riverpod.
#     Knowledge of Firebase services (Firestore, Authentication, Cloud Functions, etc.).
#     Understanding of Material Design principles and platform-specific design guidelines.
#     Experience working in an Agile/Scrum environment.

# Perks and Benefits:

#     Competitive salary and benefits package.
#     Flexible working hours and the option to work remotely.
#     Opportunity to work on exciting projects with cutting-edge technologies.
#     Professional growth opportunities and a collaborative work environment.

# How to Apply: Please submit your resume, portfolio, and a brief cover letter to [email address] with the subject line "Flutter Developer Application - [Your Name]".

# We look forward to hearing from you!"""

# sample_resume=pdf_reader("Resume.pdf")
# print(analyze_resume(sample_job_desc,sample_resume))

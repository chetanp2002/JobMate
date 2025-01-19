import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import matplotlib.pyplot as plt
from io import BytesIO
from time import sleep
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

# Configure GenAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini
def get_gemini_response(resume_text, job_description):
    input_prompt = f"""
    Act like a skilled ATS. Evaluate the resume against the job description considering the competitive market.
    Provide the output in this exact JSON format:
    {{
        "JD Match": "<Percentage>",
        "MissingKeywords": ["<Keyword1>", "<Keyword2>"],
        "Profile Summary": "<Summary>",
        "Suggestions": ["<Tip1>", "<Tip2>"]
    }}

    Resume: {resume_text}
    Job Description: {job_description}
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(input_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to extract text from PDF
def extract_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.strip()
    except Exception as e:
        return f"Error extracting PDF text: {str(e)}"

# Function to generate PDF report
def generate_pdf_report(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(50, 750, "Smart ATS Resume Evaluation Report")
    c.drawString(50, 730, f"JD Match: {data.get('JD Match', 'N/A')}")
    c.drawString(50, 710, "Missing Keywords:")
    y = 690
    for keyword in data.get("MissingKeywords", []):
        c.drawString(70, y, f"- {keyword}")
        y -= 20
    c.drawString(50, y - 10, "Profile Summary:")
    c.drawString(70, y - 30, data.get("Profile Summary", "N/A"))
    y -= 60
    c.drawString(50, y, "Suggestions:")
    for tip in data.get("Suggestions", []):
        c.drawString(70, y - 20, f"- {tip}")
        y -= 20
    c.save()
    buffer.seek(0)
    return buffer

# Function to send results via email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_email_results(to_email, subject, body):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_APP_PASSWORD")  # Use the App Password here
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.set_debuglevel(1)  # Show debug output for troubleshooting
            server.starttls()  # Secure the connection with TLS
            server.login(sender_email, sender_password)  # Use App Password
            server.sendmail(sender_email, to_email, msg.as_string())
            print("Email sent successfully!")
            return "Email sent successfully!"
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return f"Error sending email: {str(e)}"


# Streamlit App
st.set_page_config(page_title="Smart ATS", page_icon="📄", layout="wide")

# Header Section with Custom Font and Color
st.markdown("""
    <style>
    h1 {
        font-family: 'Arial', sans-serif;
        color: #2C3E50;
    }
    h2 {
        color: #16A085;
    }
    .stTextInput>div>input {
        font-size: 18px;
    }
    .stButton>button {
        background-color: #16A085;
        color: white;
        font-size: 16px;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #1abc9c;
    }
    .stFileUploader>label {
        font-size: 14px;
        color: #555;
    }
    .stTextArea>div>textarea {
        font-size: 16px;
    }
    .stAlert {
        background-color: #f5f5f5;
        color: #555;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.title(" JOBMATE: The Ultimate Resume Optimizer 🌟")
st.markdown("#### Transform your resume to stand out in the competitive job market.")

# Sidebar with Tips
st.sidebar.header("💡 Quick Tips")
st.sidebar.markdown("""
- Ensure your resume is in PDF format.
- Paste a detailed job description for better results.
- Use this tool to find missing keywords and optimize for ATS systems.
""")
st.sidebar.markdown("---")
st.sidebar.write("🚀 Powered by Google Gemini AI")

# Input Section
st.subheader("📄 Step 1: Provide Job Details")
job_description = st.text_area("Paste the Job Description", height=150, help="Copy and paste the job description here.")

st.subheader("📤 Step 2: Upload Your Resume")
uploaded_file = st.file_uploader("Upload Your Resume (PDF only)", type="pdf", help="Upload a PDF version of your resume.")

email = st.text_input("📧 Optional: Enter your email to receive results")

# File Size Limitation
if uploaded_file and uploaded_file.size > 20 * 1024 * 1024:
    st.warning("🚨 File is too large. Please upload a file smaller than 20MB.")

# Submission Button with Progress Bar
if st.button("🔍 Analyze Resume"):
    if uploaded_file and job_description.strip():
        resume_text = extract_pdf_text(uploaded_file)
        
        if "Error" in resume_text:
            st.error(resume_text)
        else:
            st.info("⏳ Analyzing your resume... Please wait.")
            with st.spinner('Processing...'):
                sleep(2)
                response = get_gemini_response(resume_text, job_description)
                
                if response.startswith("Error"):
                    st.error(f"Failed to process your request: {response}")
                else:
                    try:
                        response_json = json.loads(response)
                        
                        # Display Results
                        st.success("✅ Resume Analysis Completed!")
                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric("🔍 JD Match", response_json.get("JD Match", "N/A"))
                            st.markdown("### 🔑 Missing Keywords")
                            st.write(response_json.get("MissingKeywords", []))
                        
                        with col2:
                            st.markdown("### 📝 Profile Summary")
                            st.write(response_json.get("Profile Summary", "N/A"))
                            st.markdown("### 💡 Suggestions")
                            st.write(response_json.get("Suggestions", []))
                        
                        # Keyword Visualization
                        if response_json.get("MissingKeywords"):
                            st.markdown("### 📊 Missing Keywords Visualization")
                            fig, ax = plt.subplots()
                            keywords = response_json.get("MissingKeywords", [])
                            ax.barh(keywords, [1] * len(keywords), color="skyblue")
                            ax.set_xlabel("Importance")
                            ax.set_title("Missing Keywords")
                            st.pyplot(fig)
                        
                        # Download Report
                        pdf_data = generate_pdf_report(response_json)
                        st.download_button(
                            label="📥 Download Report",
                            data=pdf_data,
                            file_name="ATS_Report.pdf",
                            mime="application/pdf"
                        )
                        
                        # Email Results Option
                        if email:
                            email_status = send_email_results(
                                email,
                                "Smart ATS Resume Evaluation Report",
                                f"JD Match: {response_json.get('JD Match', 'N/A')}\n\n"
                                f"Missing Keywords: {response_json.get('MissingKeywords', [])}\n\n"
                                f"Profile Summary: {response_json.get('Profile Summary', 'N/A')}\n\n"
                                f"Suggestions: {response_json.get('Suggestions', [])}\n"
                            )
                            st.success(email_status)

                    except json.JSONDecodeError:
                        st.error("Failed to decode the AI response. Please ensure the AI returns valid JSON.")
    else:
        st.warning("Please provide both the job description and upload a resume to proceed.")

# Footer Section
st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #f8f8f8;">
        <p style="font-size: 14px; color: #777;">Made with ❤️ by Chetan. Follow me for more updates.</p>
    </div>
""", unsafe_allow_html=True)

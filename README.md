
# JOBMATE: The Ultimate Resume Optimizer

![My Image](https://raw.githubusercontent.com/chetanp2002/images/main/jobmate.png)
![My Image](https://raw.githubusercontent.com/chetanp2002/images/main/jobmate%20(2).png)

**JOBMATE** is an AI-powered tool designed to help job seekers optimize their resumes for better performance in **Applicant Tracking Systems (ATS)**. The tool evaluates resumes against job descriptions, analyzes ATS compatibility, identifies missing keywords, and provides actionable suggestions for improvement.

## Features

- **ATS Keyword Matching**: Automatically scans your resume and compares it with a given job description to identify missing keywords and optimize your resume for ATS.
- **Resume Parsing**: Upload your resume in PDF format, and the tool will extract relevant content to analyze and compare with job descriptions.
- **AI-Powered Suggestions**: Powered by **Google Gemini AI**, the tool generates personalized tips and suggestions for improving your resume's ATS compatibility.
- **Visual Analytics**: Visualizes the missing keywords to give you insights into where your resume needs improvement.
- **PDF Report Generation**: After the analysis, download a detailed **ATS evaluation report** in PDF format with **ATS scores**, **missing keywords**, **profile summaries**, and **suggestions**.
- **Email Notifications**: Option to receive your evaluation results directly to your email, with personalized feedback for improving your resume.

## Technologies Used

- **Streamlit**: For building an interactive web interface.
- **Google Gemini AI**: To analyze and generate ATS evaluation content.
- **PyPDF2**: For extracting text from uploaded PDF resumes.
- **SMTP**: To send email notifications with ATS evaluation reports.
- **Matplotlib**: For visualizing missing keywords and their importance in the ATS matching process.
- **Python**: The core language used for building the application.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/chetanp2002/JOBMATE.git
   cd JOBMATE
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Windows, use `venv\Scriptsctivate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** to store your Google API key for Gemini AI:
   ```bash
   GOOGLE_API_KEY=your_api_key_here
   ```

5. **Run the application**:
   ```bash
   streamlit run streamlit_app.py
   ```

## Usage

1. **Step 1**: Provide the **Job Description** by pasting it into the text area.
2. **Step 2**: Upload your **Resume (PDF)** file.
3. Click **Analyze Resume** to evaluate your resume against the job description.
4. Review the results, including the **ATS score**, **missing keywords**, and **improvement suggestions**.
5. Optionally, enter your **email address** to receive a detailed ATS evaluation report.
6. Download the **ATS Report** in PDF format for later reference.

## Contributing

If you'd like to contribute to this project, feel free to open an **issue** or create a **pull request** with your improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Google Gemini AI**: For providing powerful AI capabilities for ATS resume analysis.
- **Streamlit**: For enabling the development of an easy-to-use web interface.
- **PyPDF2**: For PDF text extraction functionality.
- **SMTP**: For sending email notifications and reports.

---

**JOBMATE** is the ultimate tool to optimize your resume and ensure it stands out in today's competitive job market by passing through **ATS systems** successfully.

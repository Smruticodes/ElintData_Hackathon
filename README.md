# Automated CV Scoring and Feedback System

## 📌 Objective
Design and implement an automated system that collects resumes, scores them based on predefined criteria, and sends personalized feedback and scores to candidates via email.

---

## 🛠️ Features

- 📥 Resume collection from a specified folder or email inbox  
- 📊 Intelligent Resume Scoring based on:
  - Work experience
  - Education
  - Skills
  - Formatting
  - JD-CV match
- 📧 Personalized Email Feedback to each candidate

---

## 🔍 Scope of Work

### Step 1: Resume Collection
- Accept resumes in PDF/DOCX formats
- Ensure unique naming and organization
- Extract key details:
  - Masked Name & Email
  - Batch Years
  - Relevant AI Experience
  - JD-CV Match Score

### Step 2: Resume Scoring
- Implement a scoring algorithm based on:
  - Work experience
  - Education
  - Skills
  - Formatting and clarity
  - Keywords relevance
- Output a final CV Score with optional tags like years of experience, soft skills, etc.

### Step 3: Email Feedback
- Extract email address from resume or other sources
- Send personalized email containing:
  - CV Score
  - Score breakdown
  - Notable feedback (strengths/weaknesses)
  - Optional: next steps or motivation

---
####
![image](https://github.com/user-attachments/assets/56f5d635-081a-45a6-9f31-ad3ee8ae25a6)

![image](https://github.com/user-attachments/assets/546ddf0b-ec13-44ac-9dce-6f8d44cd42ea)
![image](https://github.com/user-attachments/assets/36fae886-658b-439b-8bb4-177bd4f895a3)

## 📆 Deliverables

1. Script to collect and process resumes
2. CV scoring model with documented logic
3. Automated email sender with customizable template
4. Logging mechanism for processed resumes
5. Code repository (to be pushed to Elint’s GitLab)

---

## ⚙️ Tech Stack

- **Programming Language:** Python
- **Libraries:** os, pandas, sklearn, docx, PyPDF2, smtplib
- **Email Server:** Gmail API / SMTP


---

---

## 🚀 Getting Started

1. Clone the repository  
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up secure email credentials  
4. Run the script to begin processing resumes

---


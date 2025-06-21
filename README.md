# 📝 Quiz Website 📚🎓

Hi! I'm **Amit Subhash Agrahari**, and I proudly led the development of this **Quiz Website** project as part of our college coursework. This project was not just an academic exercise — it was a chance for me to lead a team, distribute responsibilities based on skills and interests, and build a meaningful, full-stack web application integrating frontend, backend, AI components, and cloud deployment.

---

## 👥 Team Members & Roles

| Name                     | Role                                              |
|:------------------------|:-------------------------------------------------|
| **Amit Subhash Agrahari** | Project Leader, Frontend, Backend, ML Integration, Deployment |
| Tanish R. Sonkusare       | Documentation & Architecture Diagram             |
| Mr. Atharva S. Nimkar     | Quality Assurance (QA) Tester                    |

---

## 📖 Project Overview

This web-based quiz platform allows **teachers to create virtual classes**, assign quizzes, and manage students securely. The platform includes AI-based proctoring capabilities and cloud deployment for live use.

---

## 🚀 How It Works

- **Teacher Registration & Login**
  - Teachers sign up and log into the platform.
  - They can **create a virtual class** for any subject or batch and receive a **unique class code**.
  - This code is shared with students to join the class.

- **Student Registration & Login**
  - Students register and log in.
  - Using the **class code provided by their teacher**, students can join the class and participate in quizzes.

- **Quiz Creation by Teachers**
  - Teachers have two options:
    1. **Manually add questions and options.**
    2. **Upload a formatted file** containing the quiz.

  **File Format Example:**
    ``` base
    question_open
    What is C?
    question_close
    Option1
    Option2
    Option3
    Option4
    Answer

**Taking Tests**
- Students attempt quizzes in a secure interface.
- **Restrictions enforced:**
  - Text cannot be selected.
  - `Ctrl+P` (Print Screen) is disabled.
  - If a student attempts to use a mobile phone, the integrated **ML model detects it and terminates the test**.

- **Results & Reporting**
- Students can view their personal results.
- Teachers can view results of all students per class and **download the results as an Excel file**.

---

## 📦 Deployment & Hosting

This project was containerized using **Docker** for easy deployment and scalability.  

It’s currently deployed live on **Render**:

🌐 **Live Demo:** [https://quiz-app-v6-9.onrender.com/](https://quiz-app-v6-9.onrender.com/)

**Note:** As Render spins down free-tier applications when idle, the site may take **a few seconds to load** initially when accessed after a period of inactivity.

---

## 📐 Project Architecture

- **Type:** Monolithic Architecture  
- Combines frontend, backend, ML services, and Docker containerization within a unified application.

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript, GSAP (for UI animations)
- **Backend:** Django (Python)
- **ML Integration:** Custom ML model for device detection (anti-cheating)
- **Containerization:** Docker
- **Cloud Hosting:** Render

---

## 📊 Features Summary

- Teacher and student login systems
- Enhanced mobile responsiveness
- Class and quiz creation workflows
- Upload quiz via text file with custom format
- AI-powered anti-cheating detection
- Downloadable quiz results in Excel
- Clean, animated, responsive UI
- Docker containerized deployment on Render
- Basic exam security controls (disable text selection, disable print screen)

---

## ⚙️ Future Roadmap

Planned future features include:

- AI-based face detection for impersonation checks
- Quiz scheduling and automated result analysis
- Live proctoring using webcam monitoring
- Student leaderboard per class
- Dark mode

---

## 📝 Final Thoughts

Leading this project not only strengthened my technical skills across **full-stack development, AI integration, containerized deployment, and cloud hosting** but also taught me how to coordinate a team by assigning roles based on individual interests and strengths.

Though there are minor bugs and features yet to be implemented, this project stands as a strong demonstration of my ability to build, lead, deploy, and maintain real-world tech solutions under academic deadlines.

---

## 📌 About Me

I'm **Amit Subhash Agrahari**, an aspiring **full-stack ML engineer and software developer** passionate about building scalable, secure, and user-friendly applications.

**GitHub:** [BlackIIIWhite](https://github.com/BlackIIIWhite)

---



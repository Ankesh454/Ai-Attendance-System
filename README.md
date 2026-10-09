# 🤖 AiAttendance — AI-Powered Attendance Management System

**AiAttendance** is an AI-powered attendance management system built using Python, Streamlit, Machine Learning, Computer Vision, Voice Recognition, and Supabase. It aims to simplify student identification, subject enrollment, and attendance management through AI-based technologies.

The application provides separate interfaces for students and teachers, with face-based student identification, optional voice-based identification, and teacher account authentication.

---

## ✨ Features

### 👨‍🎓 Student Module

- Face-based student login and identification
- Capture face using the device camera
- Register a new student profile
- Optional voice enrollment during registration
- Voice-based student identification
- View enrolled subjects
- Join subjects using a unique subject code
- View personal attendance records

### 👨‍🏫 Teacher Module

- Teacher registration using an invite code
- Teacher login and authentication
- Dedicated teacher dashboard
- Create and manage subjects
- Generate unique subject enrollment codes
- View students enrolled in a subject
- View class statistics
- Monitor attendance information
- Reset teacher password using phone OTP verification

### 🔐 Authentication and Authorization

- Separate authentication flows for students and teachers
- Face-based student identification
- Teacher authentication using login credentials
- Invite-code-based teacher registration
- Password hashing using bcrypt, where configured
- Session-based authentication state management
- Role-based access to student and teacher dashboards
- Phone OTP verification for teacher password recovery

### 🤖 AI-Based Identification

- Face detection using Dlib
- Facial landmark detection
- Face embedding generation
- Student identification using machine learning
- Support for SVM, Logistic Regression, and KNN
- Face-distance-based verification
- Voice embedding generation using Resemblyzer
- Voice similarity-based student identification

---

## 🔑 Authentication System

AiAttendance provides separate authentication workflows for students and teachers.

### Student Authentication

Students can access their dashboard through face-based identification.

```text
Student
   ↓
Student Login
   ↓
Capture Face
   ↓
Generate Face Embedding
   ↓
Identify Registered Student
   ↓
Verify Face Match
   ↓
Student Dashboard
```

If a student's face is not recognized, the student can proceed to profile registration.

### Teacher Authentication

Teachers use their registered credentials to access the teacher dashboard.

```text
Teacher
   ↓
Teacher Login
   ↓
Enter Credentials
   ↓
Verify Credentials
   ↓
Authenticate Teacher
   ↓
Teacher Dashboard
```

### Teacher Registration Using Invite Code

Teacher registration uses an invite code to restrict account creation to authorized users.

```text
Teacher Registration
        ↓
Enter Teacher Details
        ↓
Enter Invite Code
        ↓
Validate Invite Code
        ↓
Create Teacher Account
        ↓
Teacher Login
        ↓
Teacher Dashboard
```

The invite code is intended to prevent unauthorized teacher registration. It should be validated securely, and sensitive codes must not be exposed in public source code.

### Teacher Password Recovery

The application supports a phone OTP-based password recovery flow.

```text
Forgot Password
       ↓
Enter Registered Phone Number
       ↓
Verify Teacher Account
       ↓
Send OTP
       ↓
Verify OTP
       ↓
Set New Password
       ↓
Update Teacher Credentials
```

OTP delivery depends on the configured messaging service.

---

## 🧠 Face Recognition

The face recognition system uses computer vision and machine learning to identify registered students.

### Face Recognition Pipeline

```text
Camera Input
     ↓
Face Detection using Dlib
     ↓
Facial Landmark Detection
     ↓
Face Embedding Generation
     ↓
Compare with Registered Students
     ↓
Machine Learning Prediction
     ↓
Distance-Based Verification
     ↓
Student Identification
```

### How It Works

1. The camera captures the student's face.
2. Dlib detects the face in the image.
3. Facial landmarks are identified.
4. A face recognition model generates a numerical representation called a **face embedding**.
5. The system compares the captured face with registered student data.
6. A trained machine learning classifier helps identify the student.
7. Distance-based verification helps reject uncertain or invalid matches.

The verification threshold is important because a classifier prediction alone does not guarantee that a detected face belongs to a registered student.

---

## 🎙️ Voice Recognition

AiAttendance also supports optional voice-based student identification.

### Voice Recognition Pipeline

```text
Voice Input
     ↓
Audio Processing
     ↓
Voice Embedding Generation
     ↓
Compare with Registered Voice Data
     ↓
Calculate Similarity
     ↓
Student Identification
```

### How It Works

1. The student provides a voice sample.
2. Audio data is processed as required.
3. Resemblyzer generates a voice embedding.
4. The generated embedding is compared with registered voice data.
5. A similarity score helps determine whether the voice matches a registered student.

Voice recognition is an optional identification method. Its availability depends on the configured registration and verification flow.

---

## 🧪 Machine Learning

The project uses Scikit-learn for machine learning-based student identification.

### Algorithms and Components

- **Support Vector Machine (SVM):** Classifies face embeddings into student identities.
- **Logistic Regression:** Provides an alternative classification approach.
- **K-Nearest Neighbors (KNN):** Identifies students based on nearby feature vectors.
- **Face-distance verification:** Helps reject faces that do not sufficiently match registered data.
- **Embedding similarity:** Supports voice-based identification.

The project uses numerical embeddings as input features for identification. The selected classifier and verification thresholds affect recognition accuracy.

---

## 🏫 Subject Management

Teachers can manage their subjects through the teacher dashboard.

### Features

- Create new subjects
- View created subjects
- Generate unique subject codes
- View enrolled students
- Check class-related statistics
- Monitor subject-related attendance information

### Subject Enrollment Workflow

```text
Teacher Creates Subject
          ↓
Generate Subject Code
          ↓
Share Code with Students
          ↓
Student Enters Subject Code
          ↓
Verify Subject Code
          ↓
Enroll Student in Subject
          ↓
Subject Appears in Student Dashboard
```

The subject code connects students to the appropriate subject and helps organize attendance information by class.

---

## 📊 Attendance Management

AiAttendance connects student identification with subject and attendance information stored in Supabase.

### Features

- Retrieve student attendance records
- Display attendance information in the student dashboard
- Associate attendance records with students and subjects
- View class-related statistics
- Monitor attendance information through the teacher dashboard

Attendance information is linked to student and subject data to support subject-wise attendance management.

---

## 🗄️ Database

The application uses **Supabase** as its database backend.

### Database Entities

| Table / Entity | Purpose |
|---|---|
| `students` | Stores student profiles and identification data |
| `teachers` | Stores teacher account information and authentication data |
| `subjects` | Stores subject details and teacher associations |
| `subject_students` | Manages student enrollment in subjects |
| Attendance records | Stores student attendance information |

The exact attendance table name and database columns depend on the configured Supabase schema.

### Database Relationships

```text
Teachers
   |
   | Create subjects
   ↓
Subjects
   |
   | Student enrollment
   ↓
subject_students
   |
   ↓
Students
   |
   ↓
Attendance Records
```

Face and voice embeddings may be stored with student identification data to support recognition.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| UI Framework | Streamlit |
| Machine Learning | Scikit-learn |
| Classification Algorithms | SVM, Logistic Regression, KNN |
| Computer Vision | Dlib, Face Recognition Models |
| Image Processing | NumPy, Pillow |
| Voice Recognition | Resemblyzer, Librosa |
| Database | Supabase |
| Authentication | Session State, bcrypt |
| Deployment | Streamlit Community Cloud |

---

## 📁 Project Structure

The following is a representative structure. Adjust filenames to match the actual repository.

```text
AiAttendance/
│
├── app.py
├── db.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── services/
│   ├── auth/
│   │   ├── login.py
│   │   └── teacher_auth.py
│   │
│   ├── face_recognition/
│   │   ├── detection.py
│   │   ├── embeddings.py
│   │   └── classifier.py
│   │
│   ├── voice_recognition/
│   │   ├── audio_processing.py
│   │   └── voice_embeddings.py
│   │
│   ├── students/
│   │   └── student_service.py
│   │
│   ├── teachers/
│   │   └── teacher_service.py
│   │
│   ├── subjects/
│   │   └── subject_service.py
│   │
│   └── attendance/
│       └── attendance_service.py
│
├── models/
│   └── trained_model_files
│
├── assets/
│   └── application_assets
│
└── .streamlit/
    └── secrets.toml
```

### Directory Responsibilities

- **`app.py`** — Application entry point and Streamlit interface.
- **`db.py`** — Database operations and Supabase integration.
- **`services/auth/`** — Authentication, teacher registration, invite-code verification, and login logic.
- **`services/face_recognition/`** — Face detection, embedding generation, and classification.
- **`services/voice_recognition/`** — Audio processing and voice embeddings.
- **`services/students/`** — Student registration and student-related operations.
- **`services/teachers/`** — Teacher account and dashboard operations.
- **`services/subjects/`** — Subject creation and enrollment management.
- **`services/attendance/`** — Attendance-related operations.
- **`models/`** — Trained models or related model files, if stored locally.
- **`.streamlit/`** — Streamlit configuration and application secrets.

---

## ⚙️ Installation and Setup

### Prerequisites

- Python installed on your system
- Git
- A Supabase project
- A webcam for face capture
- A microphone if voice-based features are used

### 1. Clone the Repository

```bash
git clone https://github.com/Ankesh454/Ai-Attendance-System.git
cd Ai-Attendance-System
```

### 2. Create a Virtual Environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Dlib and some computer vision or audio packages may require additional system dependencies or a compatible Python version.

### 4. Configure Supabase

Create a Supabase project and configure the database tables required by the application.

Create `.streamlit/secrets.toml` for local development:

```toml
SUPABASE_URL = "your_supabase_project_url"
SUPABASE_KEY = "your_supabase_key"
```

Use the exact secret names expected by the application's database code.

**Important:** Never commit real database credentials, privileged API keys, passwords, or OTP credentials to GitHub.

### 5. Run the Application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

Replace `app.py` with the actual entry-point filename if your repository uses a different one.

---

## 🔐 Security and Privacy

AiAttendance processes student identity information and may process biometric data. Appropriate security measures are important.

- Store passwords using secure password hashing.
- Validate teacher invite codes securely.
- Protect OTP verification and password recovery workflows.
- Keep database credentials and API keys private.
- Use appropriate Supabase Row Level Security policies.
- Restrict access to student and teacher information.
- Protect stored face and voice embeddings.
- Obtain appropriate consent before collecting biometric information.
- Define suitable data retention and deletion policies.
- Consider face liveness detection and anti-spoofing to reduce fraudulent attendance.

These are recommended safeguards and do not imply that every measure is already implemented.

---

## 🚀 Deployment

AiAttendance can be deployed using Streamlit Community Cloud if the required packages and models are compatible with its runtime environment.

### Deployment Steps

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect the GitHub repository.
4. Select the application entry point.
5. Configure Supabase credentials and other required secrets.
6. Deploy the application.
7. Test authentication, camera access, database connectivity, and recognition functionality.

### Deployment Considerations

- Use compatible Python and package versions.
- Configure secrets through deployment settings.
- Verify webcam permissions in the browser.
- Confirm that database access policies are configured correctly.
- Ensure that required model files are available.
- Consider memory and processing requirements for face recognition.

---

## 🔄 Application Workflow

### Student Login Flow

```text
Student
   ↓
Student Login
   ↓
Face Capture
   ↓
Face Embedding Generation
   ↓
Student Identification
   ↓
Face Verification
   ↓
Student Dashboard
   ↓
View Subjects
   ↓
View Attendance
```

### New Student Registration Flow

```text
Student
   ↓
Student Login
   ↓
Face Not Recognized
   ↓
Register New Profile
   ↓
Enter Student Information
   ↓
Capture Face
   ↓
Optional Voice Enrollment
   ↓
Create Student Profile
```

### Teacher Workflow

```text
Teacher
   ↓
Register Using Invite Code
   ↓
Teacher Login
   ↓
Teacher Dashboard
   ↓
Create or Manage Subjects
   ↓
Generate Subject Code
   ↓
Students Enroll
   ↓
View Enrolled Students
   ↓
Monitor Attendance
```

---

## 🎯 Project Objectives

The main objective of AiAttendance is to automate student identification and simplify classroom attendance management using Artificial Intelligence.

The project combines:

- Computer Vision
- Face Recognition
- Voice Recognition
- Machine Learning
- Authentication and Authorization
- Database Management
- Streamlit Application Development

The system aims to provide a centralized platform for managing student identities, subjects, and attendance information.

---

## 🔮 Future Enhancements

Potential improvements include:

- Real-time attendance marking from classroom photographs
- Improved recognition in low-light environments
- Face liveness detection and anti-spoofing
- Better voice verification in noisy environments
- QR-code-based subject enrollment
- Attendance percentage analytics
- Export attendance reports to CSV or PDF
- Attendance notifications
- Improved false-match detection
- Enhanced security auditing and access controls
- Better scalability for large classrooms

These are potential improvements and may not be part of the current implementation.

---

## 👨‍💻 Author

**Ankesh Kumar**

AiAttendance — An AI-powered attendance management system built with Python, Machine Learning, Computer Vision, Voice Recognition, Streamlit, and Supabase.

- **GitHub:** [Ankesh454](https://github.com/Ankesh454)
- **Repository:** [AiAttendance — AI Attendance System](https://github.com/Ankesh454/Ai-Attendance-System)

---

⭐ If you find this project interesting, consider giving the repository a star on GitHub.

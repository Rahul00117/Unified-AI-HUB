#  Unified AI Hub  

**Unified AI Hub** is an all-in-one **Streamlit-based AI toolkit** that brings together multiple AI-powered modules into a single unified platform. Instead of juggling between different apps, this hub provides **automation, machine learning, computer vision, remote access, and personal assistance** — all accessible from one simple dashboard.  

---

##  Key Features  

- **AI Automation Hub** – Automate Emails, WhatsApp, and Social Media  
- **Live AI Camera** – Real-time face & object detection using OpenCV  
- **Study Hours vs Marks Predictor** – Predict marks using ML regression model  
- **SSH Assistant** – Connect to remote servers and execute commands securely  
- **AI File Manager** – Smart search and intelligent file organization  
- **AI Vehicle Recommender** – Personalized vehicle suggestions based on user preferences  
- **Saundarya Lite (Fashion Assistant)** – Outfit and style recommendations  
- **Motivation Buddy** – Track goals, progress, and stay motivated  
- **Desktop Assistant** – Perform system-level automation tasks  

---

##  Tech Stack  

- **Frontend/UI**: Streamlit  
- **Programming Language**: Python  
- **Machine Learning**: Scikit-learn, TensorFlow, PyTorch, Pandas, NumPy  
- **Computer Vision**: OpenCV  
- **Automation**: Selenium, Paramiko, smtplib, PyAutoGUI  
- **Database**: SQLite  

---

##  Project Structure  
UnifiedAIHub/
│
├── app.py # Main Dashboard
├── automation/ # AI Automation Hub
├── camera/ # Live AI Camera
├── predictor/ # Study Hours vs Marks Predictor
├── ssh_assistant/ # SSH Assistant
├── file_manager/ # AI File Manager
├── vehicle_recommender/ # Vehicle Recommender
├── fashion/ # Saundarya Lite
├── motivation/ # Motivation Buddy
├── desktop/ # Desktop Assistant
└── data/ # Database, ML Models, Configs


---

##  Installation  

1. Clone the repository  
   ```bash
   git clone https://github.com/your-username/UnifiedAIHub.git
   cd UnifiedAIHub

2. Create a virtual environment (optional but recommended)
   python -m venv venv
   source venv/bin/activate   # For Linux/Mac
   venv\Scripts\activate      # For Windows

3. Install dependencies
   pip install -r requirements.txt
   
5. Run the app
   streamlit run app.py

 ---

##Future Enhancements
-Add User Authentication & personalized profiles
-Deploy on Cloud Platforms (for global access)
-Expand modules with Voice Assistant & NLP tools
-Mobile-friendly responsive design

---

---

##  requirements.txt  

```txt
streamlit
scikit-learn
tensorflow
torch
pandas
numpy
opencv-python
selenium
paramiko
pyautogui
matplotlib
smtplib  # (builtin, mention for clarity)
sqlite3   # (builtin, mention for clarity)




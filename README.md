🏥 Health Chatbot with Prediction & Calculation

A smart health-assistant chatbot built using Python and Machine Learning, allowing users to chat, enter symptoms or health data, and receive disease predictions, health calculations, and recommendations instantly.

🚀 Project Overview

This project integrates a chatbot interface, ML-based predictions, and health metric calculations.
It helps users check common conditions, calculate health scores, and get simple recommendations.

Note: This project is for educational purposes only and is not a replacement for professional medical advice.

✨ Features
🤖 Chatbot Interaction

Interactive chat-style question–answer system

Collects symptoms and health-related inputs

Provides friendly responses

🧠 Disease Prediction

Predicts conditions such as:

Diabetes

Heart Disease

Kidney Disease

Liver Disorder

Anemia

Thyroid Issues

Hypertension

PCOS

Normal Health Evaluation

📊 Health Calculations

BMI calculation

Risk level classification (Good / Average / Bad)

Basic health do’s and don’ts

🛠️ Modular Code

Separate modules for chatbot, ML predictions, and calculations

Easy to expand with new diseases or calculations

🧰 Tech Stack

Python 3.x

Pandas, NumPy

Scikit-learn (ML Models)

Flask (if using web interface)

Pickle / Joblib for saving models

📁 Folder Structure
health_chatbot_with_prediction_and_calculation/
│
├── chatbot.py               # Chat interaction logic
├── prediction_model.py      # Prediction functions & ML model loading
├── calculations.py          # Health calculation functions
├── data/                    # CSV datasets
├── models/                  # Saved ML models
├── requirements.txt         # Dependencies
└── README.md                # Documentation


(Modify this to match your actual file names.)

🔧 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/rajeshwari-s-9360/health_chatbot_with_prediction_and_calculation.git
cd health_chatbot_with_prediction_and_calculation

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run the Application

If running as a simple script:

python chatbot.py


If running as a Flask app:

python app.py

🧠 How the Prediction Works

User enters symptoms or health metrics

Input is cleaned, encoded, and preprocessed

ML model predicts the most likely condition

System returns:

Prediction result

Risk category

Recommendations

📝 Sample Output
Prediction: High chance of Diabetes
Risk Level: Bad
Recommendations:
✔ Maintain diet control
✔ Reduce sugar intake
✔ Regular physical exercise
✔ Consult a medical professional

📌 Future Improvements

Add multi-language support

Add deep-learning models

Add charts, reports, and PDF download

Add a full web UI

Add voice-based health chat

⚠️ Disclaimer

This project is for learning, academic, and demo purposes.
Not intended for real medical diagnosis.

🤝 Contribution

Feel free to fork, submit issues, or send pull requests.

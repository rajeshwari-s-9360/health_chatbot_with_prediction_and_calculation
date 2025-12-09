from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pickle, os, json
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from models import db, User, ChatMessage

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# SQLite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# Load chatbot model
try:
    chatbot_model = pickle.load(open("chatbot_model.pkl", "rb"))
    chatbot_vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
except Exception as e:
    chatbot_model = None
    chatbot_vectorizer = None
    print("❌ Error loading chatbot model:", e)

# Load PAC models
pac_conditions = ["normal", "diabetes", "heart", "kidney", "liver",
                  "anemia", "hypertension", "thyroid", "pcos"]

pac_models = {}
for cond in pac_conditions:
    model_path = f"ml_models/pkl_models/{cond}_model.pkl"
    try:
        pac_models[cond] = pickle.load(open(model_path, "rb"))
        print(f"✅ Loaded PAC model: {cond}")
    except Exception as e:
        pac_models[cond] = None
        print(f"❌ Error loading {cond} model:", e)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful. Please login.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash("Invalid credentials.")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/api/predict')
@login_required
def predict():
    message = request.args.get("message", "").strip()
    if not message:
        return jsonify({"response": "Please enter a valid message."})
    try:
        if chatbot_model is None or chatbot_vectorizer is None:
            raise Exception("Model not loaded.")
        
        user_msg = ChatMessage(user_id=current_user.id, message=message, sender="user")
        db.session.add(user_msg)
        db.session.commit()

        X = chatbot_vectorizer.transform([message])
        pred = chatbot_model.predict(X)[0]
        conf = chatbot_model.predict_proba(X).max()

        response = f"🤖 Possible Disease: {pred} ({round(conf*100, 2)}% confidence)"

        try:
            with open("static/data/recommendations.json") as f:
                recs = json.load(f)
            disease_recs = recs.get(pred.lower(), ["Consult a doctor for more advice."])
            response += "\n💡 Recommendations:\n" + "\n".join(f"- {r}" for r in disease_recs)
        except Exception:
            response += "\n💡 Recommendations: Consult a doctor for more advice."

        bot_msg = ChatMessage(user_id=current_user.id, message=response, sender="bot")
        db.session.add(bot_msg)
        db.session.commit()

        return jsonify({"response": response})
    except Exception as e:
        print("❌ Error in chatbot prediction:", e)
        return jsonify({"response": "⚠️ Error getting response from the bot."})

@app.route('/history')
@login_required
def history():
    messages = ChatMessage.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', messages=messages)

@app.route('/pac')
@login_required
def pac_dashboard():
    return render_template('pac.html')

@app.route("/predict_pac/<condition>", methods=["POST"])
@login_required
def predict_pac(condition):
    try:
        model = pac_models.get(condition)
        if not model:
            return jsonify({"result": "❌ Model not found."})

        input_data = request.get_json()
        input_values = [float(val) for val in input_data.values()]
        prediction = model.predict([input_values])[0]

        # Define prediction interpretation
        if prediction == 0:
            status = "✅ Your condition seems good."
        elif prediction == 1:
            status = "⚠️ Your condition seems average."
        else:
            status = "❌ Your condition seems bad."

        # Load condition-specific recommendations
        try:
            with open("static/data/pac_recommendations.json") as f:
                recs = json.load(f)
            condition_recs = recs.get(condition.lower(), {})
            pred_recs = condition_recs.get(str(prediction), ["Consult a doctor for more advice."])
        except Exception as e:
            print("Error loading pac_recommendations.json:", e)
            pred_recs = ["Consult a doctor for more advice."]

        rec_text = "\n💡 Recommendations:\n" + "\n".join([f"- {r}" for r in pred_recs])
        return jsonify({"result": f"{status}{rec_text}"})
    except Exception as e:
        print("❌ PAC prediction error:", e)
        return jsonify({"result": "⚠️ Something went wrong during prediction."})

@app.route('/api/diseases')
@login_required
def diseases():
    try:
        with open("static/data/diseases.json") as f:
            return jsonify(json.load(f))
    except:
        return jsonify({"error": "Unable to load diseases.json"})

@app.route('/api/faqs')
@login_required
def faqs():
    try:
        with open("static/data/faqs.json") as f:
            return jsonify(json.load(f))
    except:
        return jsonify({"error": "Unable to load faqs.json"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("🚀 Server running at http://127.0.0.1:5000")
    app.run(debug=False)

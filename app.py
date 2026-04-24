from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Dummy login
USER = {"username": "admin", "password": "1234"}

model = pickle.load(open("model.pkl", "rb"))

# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if (request.form['username'] == USER['username'] and 
            request.form['password'] == USER['password']):
            session['user'] = request.form['username']
            return redirect(url_for('home'))
        else:
            error = "Invalid Credentials ❌"
    return render_template('login.html', error=error)


# ---------------- HOME ----------------
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    return render_template('index.html')


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# ---------------- PREDICT ----------------
@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect('/')

    try:
        studytime = int(request.form['studytime'])
        failures = int(request.form['failures'])
        absences = int(request.form['absences'])
    except:
        return "Invalid Input ❌"

    features = np.array([[studytime, failures, absences]])
    prediction = model.predict(features)[0]

    data = pd.read_csv("student-mat.csv", sep=';')

    # GRAPH 1
    plt.figure()
    plt.scatter(data['studytime'], data['G3'])
    plt.xlabel("Study Time")
    plt.ylabel("Marks")
    plt.title("Study vs Marks")
    plt.savefig("static/graph1.png")
    plt.close()

    # GRAPH 2
    plt.figure()
    plt.scatter(data['absences'], data['G3'])
    plt.xlabel("Absences")
    plt.ylabel("Marks")
    plt.title("Absences vs Marks")
    plt.savefig("static/graph2.png")
    plt.close()

    # GRAPH 3
    plt.figure()
    plt.scatter(data['failures'], data['G3'])
    plt.xlabel("Failures")
    plt.ylabel("Marks")
    plt.title("Failures vs Marks")
    plt.savefig("static/graph3.png")
    plt.close()

    # Result Logic
    if prediction > 15:
        result = "Excellent 🏆"
        tip = "Keep up the great work!"
    elif prediction > 10:
        result = "Average 👍"
        tip = "Focus more on study time."
    else:
        result = "Poor ⚠"
        tip = "Reduce absences and improve consistency."

    return render_template("result.html",
                           prediction=round(prediction,2),
                           result=result,
                           tip=tip)


if __name__ == "__main__":
    app.run(debug=True)
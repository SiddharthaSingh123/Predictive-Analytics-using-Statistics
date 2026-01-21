import os
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage

# Explicit template path (fixes blank page issue)
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), "templates"))

def topsis(df, weights, impacts):
    data = df.iloc[:, 1:].astype(float)
    weights = np.array(weights, dtype=float)

    norm = np.sqrt((data ** 2).sum())
    weighted = (data / norm) * weights

    best = []
    worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            best.append(weighted.iloc[:, i].max())
            worst.append(weighted.iloc[:, i].min())
        else:
            best.append(weighted.iloc[:, i].min())
            worst.append(weighted.iloc[:, i].max())

    d_pos = np.sqrt(((weighted - best) ** 2).sum(axis=1))
    d_neg = np.sqrt(((weighted - worst) ** 2).sum(axis=1))

    score = d_neg / (d_pos + d_neg)
    df["Topsis Score"] = score
    df["Rank"] = score.rank(ascending=False).astype(int)

    return df


@app.route("/")
def home():
    template_path = os.path.join(os.getcwd(), "templates", "index.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


@app.route("/submit", methods=["POST"])
def submit():
    file = request.files["file"]
    weights = request.form["weights"].split(",")
    impacts = request.form["impacts"].split(",")
    email = request.form["email"]

    # validations
    if len(weights) != len(impacts):
        return "Weights and impacts count must be same"

    for i in impacts:
        if i not in ['+', '-']:
            return "Impacts must be + or -"

    df = pd.read_csv(file)
    result = topsis(df, weights, impacts)

    output_file = "result.csv"
    result.to_csv(output_file, index=False)

    # email result
    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result"
    msg["From"] = "yourgmail@gmail.com"
    msg["To"] = email
    msg.set_content("Please find attached TOPSIS result file.")

    with open(output_file, "rb") as f:
        msg.add_attachment(f.read(), filename="result.csv")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("yourgmail@gmail.com", "APP_PASSWORD")
        server.send_message(msg)

    return "Result sent to email successfully"

if __name__ == "__main__":
    app.run(debug=True)

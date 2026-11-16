from flask import Flask, request, jsonify, send_from_directory
from database import get_db
import os

FRONTEND = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)

app = Flask(
    __name__,
    static_folder=FRONTEND,
    static_url_path=""
)


@app.route("/")
def home():
    return send_from_directory(FRONTEND, "index.html")


# Calculate result
@app.route("/calculate", methods=["POST"])
def calculate():

    data = request.get_json()

    num1 = data.get("num1")
    operator = data.get("operator")
    num2 = data.get("num2")

    if (isinstance(num1, bool) or
        not isinstance(num1, (int, float)) or
        isinstance(num2, bool) or
        not isinstance(num2, (int, float)) or
        operator not in ["+", "-", "*", "/"]):

        return jsonify({"error": "Invalid input"}), 400

    if operator == "+":
        result = num1 + num2

    elif operator == "-":
        result = num1 - num2

    elif operator == "*":
        result = num1 * num2

    elif operator == "/":

        if num2 == 0:
            return jsonify({"error": "Cannot divide by zero"}), 400

        result = num1 / num2

    # Save calculation in MySQL
    db = get_db()
    cursor = db.cursor()

    sql = """
    INSERT INTO history (num1, operator, num2, result)
    VALUES (%s, %s, %s, %s)
    """

    values = (num1, operator, num2, result)

    cursor.execute(sql, values)
    db.commit()

    cursor.close()
    db.close()

    return jsonify({"result": result})


# Get calculation history
@app.route("/history")
def history():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM history ORDER BY id DESC LIMIT 20"
    )

    records = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(records)


if __name__ == "__main__":
    app.run(debug=True)

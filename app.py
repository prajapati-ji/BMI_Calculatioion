from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

# Function to initialize the database connection
def data_connection():
    try:
        conn = mysql.connector.connect(
            user='root',
            password='root123',
            host='localhost',
            database='db_name'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling the BMI calculation and saving data to the database
@app.route('/calculate', methods=['POST'])
def calculate():
    id = request.form['id']
    name = request.form['name']
    course = request.form['course']
    age = request.form['age']
    gender = request.form['gender']
    height = float(request.form['height'])
    weight = float(request.form['weight'])

    # BMI Calculation
    bmi = weight / ((height / 100) ** 2)
    bmi = round(bmi, 2) # Round to two decimal places

    # Save the data to the database
    conn = data_connection()
    if conn is None:
        print("Error: Unable to connect to database")
        return "Error: Unable to connect to database", 500

    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO user_enter (id, Name, Course, Age, Gender, Height, Weight, BMI) values(%s,%s,%s,%s,%s,%s,%s,%s)', (id,name, course, age, gender, height, weight, bmi))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"SQL Error: {err}")
        return f"Database error: {err}",400
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return render_template('result.html',id=id ,name=name, course=course, age=age, gender=gender, height=height, weight=weight, bmi=bmi)
if __name__ == '__main__':
    app.run(debug=True)
import os.path 
import sys
import sqlite3
import jinja2
from flask import Flask, render_template, url_for, session, request, flash, redirect, json, jsonify
from datetime import datetime


from lib.tablemodel import DatabaseModel
# This demo glues a random database and the Flask framework. If the database file does not exist,
# a simple demo dataset will be created.
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
app.secret_key = "super secret key"

database_file = "Databases/PawnCoders.DB"
dbm = DatabaseModel(database_file)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    table_name="Users"

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        account = dbm.validate_login(username, password)
    
    
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            return redirect(url_for('homepagina'))

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('loginpage.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/')
def homepagina():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('base_side_bar.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/slcer', methods = ['GET'])
def SLCer_Checker():
    UserID = session['id']

    if request.method == "GET":
        print(UserID)
        try:
            conn = sqlite3.connect("databases/Pawncoders.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT IsSLC FROM Users WHERE id=?", (UserID,))
            SLCer_data = cursor.fetchall()
            conn.close

            converted_SLCer_data = []
            for row_result in SLCer_data:
                converted_result = {}
                for key in row_result.keys():
                    value = row_result[key]
                    converted_result[key] = value
                converted_SLCer_data.append(converted_result)
                       
            return jsonify({'SLCer': converted_SLCer_data})
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve SLCer data from the database.'}), 500

@app.route('/class', methods=['GET'])
def get_class():
    if request.method == "GET":
        #We use a try block in the app.route for error handling. In particular,
        #we use it to catch any errors that might occur when executing our SQL query to fetch the class data 
        #from the database.
        try:
            query = request.args.get('q')
            conn = sqlite3.connect("databases/Pawncoders.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if query:
                cursor.execute("SELECT * FROM Class WHERE className LIKE ?", ('%' + query + '%',))
                print('Search query:', query)
            else:
                cursor.execute('SELECT * FROM class')
            class_data = cursor.fetchall()
            conn.close()
            
            converted_class_data = []
            for row_result in class_data:
                converted_result = {}
                for key in row_result.keys():
                    value = row_result[key]
                    converted_result[key] = value
                converted_class_data.append(converted_result)


            return jsonify({'class': converted_class_data})
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve class data from the database.'}), 500
    else:
        return jsonify({'error': 'Invalid request method.'}), 405
    
@app.route('/class_name', methods=['GET'])
def get_class_name():
    if request.method == "GET":
        try:
            conn = sqlite3.connect("databases/Pawncoders.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT ClassName FROM class')
            className_data = cursor.fetchall()
            conn.close()

            converted_className_data = []
            for row_result in className_data:
                converted_result = {}
                for key in row_result.keys():
                    value = row_result[key]
                    converted_result[key] = value
                converted_className_data.append(converted_result)
            return jsonify({'className': converted_className_data})
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve class names from the database.'}), 500
    else:
        return jsonify({'error': 'Invalid request method.'}), 405

@app.route('/upcoming_meetings', methods = ["GET"])
def get_upcoming_meetings():
    if request.method == "GET": 
        Name = session['username']
        try:
            conn = sqlite3.connect("databases/Pawncoders.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Meetings WHERE datetime(date || ' ' || end_time) > datetime('now') AND teacher = ?", (Name,))
            upcoming_meeting_data = cursor.fetchall()
            conn.close()

            converted_upcoming_meeting_data = []
            for row_result in upcoming_meeting_data:
                converted_result = {}
                for key in row_result.keys():
                    value = row_result[key]
                    converted_result[key] = value
                converted_upcoming_meeting_data.append(converted_result)
                       
            return jsonify({'upcoming_meetings': converted_upcoming_meeting_data})
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve upcoming meeting data from the database.'}), 500
    else:
        return jsonify({'error': 'Invalid request method.'}), 405

@app.route('/previous_meetings', methods = ["GET"])
def get_previous_meetings():
    if request.method == "GET": 
        Name = session['username']
        try:
            conn = sqlite3.connect("databases/Pawncoders.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Meetings WHERE datetime(date || ' ' || end_time) < datetime('now') AND teacher = ?", (Name,))
            previous_meeting_data = cursor.fetchall()
            conn.close()

            converted_previous_meeting_data = []
            for row_result in previous_meeting_data:
                converted_result = {}
                for key in row_result.keys():
                    value = row_result[key]
                    converted_result[key] = value
                converted_previous_meeting_data.append(converted_result)
                       
            return jsonify({'previous_meetings': converted_previous_meeting_data})
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve previous meeting data from the database.'}), 500
    else:
        return jsonify({'error': 'Invalid request method.'}), 405

@app.route("/students", methods =['GET'])
def get_students():
    if request.method == "GET":
        try:
            class_name = request.args.get('class_name')
            conn = sqlite3.connect("databases/Pawncoders.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT Name FROM students WHERE Class=?", (class_name,))
            students_data = cursor.fetchall()
            conn.close()

            converted_students_data = []
            for row_result in students_data:
                converted_result = {}
                for key in row_result.keys():
                    value = row_result[key]
                    converted_result[key] = value
                converted_students_data.append(converted_result)
                    
            return jsonify({'students': converted_students_data})
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve student data from the database.'}), 500
    else:
        return jsonify({'error': 'Invalid request method.'}), 405
    
@app.route("/attendance", methods=['GET'])
def get_attendance():
    if request.method == "GET":
        try:
            meeting_id = request.args.get('meeting_id')
            conn = sqlite3.connect("databases/Pawncoders.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Attendance WHERE meeting_id = ?",(meeting_id,))
            attendance_data = cursor.fetchall()
            conn.close()

            converted_attendance_data = []
            for row_result in attendance_data:
                converted_result = {}
                for key in row_result.keys():
                    value = row_result[key]
                    converted_result[key] = value
                converted_attendance_data.append(converted_result)
                    
            return jsonify({'attendance': converted_attendance_data})
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve attendance data from the database.'}), 500
    else:
        return jsonify({'error': 'Invalid request method.'}), 405


@app.route('/create_meeting', methods=['POST'])
def create_meeting():
    meeting_data = json.loads(request.data)
    # Extract the values from the meeting data JSON object
    class_name = meeting_data['class_name']
    start_time = meeting_data['start_time']
    end_time = meeting_data['end_time']
    date = meeting_data['date']
    subject = meeting_data['subject']
    teacher = meeting_data['teacher']
    classroom = meeting_data['classroom']
    password = meeting_data['password']

    if request.method == "POST":
        # Insert the meeting data into the database
        conn = sqlite3.connect("databases/Pawncoders.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Meetings (class, start_time, end_time, date, subject, teacher, classroom, Password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (class_name, start_time, end_time, date, subject, teacher, classroom, password))
        meeting_id = cursor.lastrowid
        conn.commit()

        cursor.execute("SELECT id FROM Students WHERE class = ?", (class_name,))
        student_ids = [row[0] for row in cursor.fetchall()]

        # Insert absence rows for each student
        cursor.executemany("INSERT INTO Attendance (meeting_id, student_id, present) VALUES (?, ?, ?)", [(meeting_id, student_id, 0) for student_id in student_ids])
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Meeting created successfully'})


#temporary student section

@app.route('/studentpage/student', methods=["GET"])
def get_students_forstudentpage():
    if request.method == "GET":
        try:
            conn = sqlite3.connect("databases/Pawncoders.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            students_data = cursor.fetchall()
            conn.close()

            converted_students_data = []
            for row_result in students_data:
                converted_result = {}
                for key in row_result.keys():
                    value = row_result[key]
                    converted_result[key] = value
                converted_students_data.append(converted_result)
                    
            return jsonify({'students': converted_students_data})
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve student data from the database.'}), 500
    else:
        return jsonify({'error': 'Invalid request method.'}), 405

@app.route('/studentpage/upcoming_meetings', methods=["GET"])
def studentpage_get_upcoming_meetings():
    if request.method == "GET":
        try:
            student_id = request.args.get('student_id')
            if student_id is None:
                return jsonify({'error': 'Missing student_id parameter.'}), 400
            
            conn = sqlite3.connect("databases/Pawncoders.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get the Class of the selected student from the students table
            cursor.execute("SELECT Class FROM students WHERE id=?", (student_id,))
            class_data = cursor.fetchone()
            
            # If the student_id is invalid or not found, return an error message
            if class_data is None:
                return jsonify({'error': 'Invalid student_id.'}), 400
            
            selected_class = class_data['Class']
            
            # Filter the meetings based on the selected class
            cursor.execute("SELECT meeting_id, date, start_time, end_time, subject, teacher, class, classroom FROM Meetings WHERE Class=? AND datetime(date || ' ' || end_time) > datetime('now')", (selected_class,))
            upcoming_meeting_data = cursor.fetchall()
            conn.close()

            converted_upcoming_meeting_data = []
            for row_result in upcoming_meeting_data:
                converted_result = {}
                for key in row_result.keys():
                    value = row_result[key]
                    converted_result[key] = value
                converted_upcoming_meeting_data.append(converted_result)

            return jsonify({'upcoming_meetings': converted_upcoming_meeting_data})
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve upcoming meeting data from the database.'}), 500
    else:
        return jsonify({'error': 'Invalid request method.'}), 405

@app.route('/studentpage')
def studentpage():
   return render_template('student.html')


@app.route('/studentpage/attendance', methods=['POST'])
def studentpage_update_attendance():
    # Get the data from the request
    student_id = request.form.get('student_id')
    meeting_id = request.form.get('meeting_id')
    password = request.form.get('password')


    # Check if the password is correct
    conn = sqlite3.connect("databases/Pawncoders.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Password FROM meetings WHERE meeting_id = ?", (meeting_id,))
    row = cursor.fetchone()
    if not row or row[0] != password:
        conn.close()
        return jsonify({'error':'Wrong Password'}), 500

    # Update the attendance table
    cursor.execute("UPDATE Attendance SET present = 1 WHERE student_id = ? AND meeting_id = ?", (student_id, meeting_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'attendance working successfully'})


if __name__ == '__main__':
    app.run(debug=True, port=8001)


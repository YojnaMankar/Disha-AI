from flask import Flask, request,jsonify # flask 
import json
import os

app = Flask(__name__)  #(__name__) in ko ham dunder method kahte hai  file ko name se strore karne ke liye


DATA_FILE = "students.json" #capital me is liye likhte h kyu ki is ka name aage chal ke change nhi honga 


#_______________________
#Helper Function
#--------------------------
def load_students(): # purani file load karne ke liye
    if not os.psth.exists(DATA_FILE): #file na mile to use error bata de
        return []
    if os.path.getsize(DATA_FILE) == 0:
        return []
    with open(DATA_FILE, "r") as file:
        data= json.load(file)
    if isinstance(data,dict):
        return[data]
    if isinstance(data,list):
        return data
    return[]

def save_students(students):
    with open(DATA_FILE, "w") as file: # data file ka path milenga , opne se opne honga , w ka means write karo mode h ek 
        json.dump(students, file, indent=4)      
#---------------------
#Home API
#---------------------
@app.route("/")
def home():
    return "student API is running"
#--------------------------------------
# GET ALL Students
# ---------------
@app.route("/students",methods=["GET"])
def get_students():
    students = load_students() 
    return jsonify(students)
#---------------------------------
#GET Students By ID
#---------------------------------
@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    student = load_students()
    for students in student:
        if student["id"]==id:
            return jsonify(student)
    return jsonify({"message":"student not found"}),404
#---------------------------
#POST Students
#---------------------------

@app.route("/students", methods=["POST"])
def add_student():
    students = load_students()
    data = request.json

    new_student = {
        "id": len(students)+1,
        "name":data["name"],
        "age":data ["age"],
        "course":data["course"]
    }
    students.append(new_student)

    save_students(students)

    return jsonify({
        "message":"student Added successfully",
        "student": new_student
    }), 201

#---------------------
#Run Server
#---------------------
if __name__ == "__main__":
    app.run(debug=True)   
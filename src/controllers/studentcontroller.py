from src.app import app
from src.database import db
from flask import request
from bson.json_util import dumps 

@app.route("/student/create/<student_name>")
def create_student(student_name):
    new_student = {
        "User":student_name
    }
    result = db.ranking.insert_one(new_student)
    return{"_id":str(result.inserted_id)}

@app.route("/student/search/<name>")
def list_students(name):
    new_student = {
        "User":name
    }
    result = db.ranking.find(new_student)
    return dumps(result)
    
@app.route("/student/all")
def list_student():
    result = db.ranking.distinct("User")
    return dumps(result)

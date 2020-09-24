from src.app import app
from src.database import db
from flask import request
from bson.json_util import dumps 
import random
from datetime import datetime
import numpy as np

@app.route("/lab/create/<lab>")
def create_lab(lab):
    lab = {
        "Lab":lab
    }
    result = db.ranking.insert_one(lab)
    return{"_id":str(result.inserted_id)}

    
@app.route("/lab/<lab_prefix>/search")
def searchLab(lab_prefix):
    """
    Purpose: Search student submissions on specific lab
    Params: lab_prefix
    Returns: Number of open PR
            Number of closed PR
            Percentage of completeness (closed vs open)
            List number of missing pr from students
            The list of unique memes used for that lab
            Instructor grade time in hours: (pr_close_time-last_commit_time)
"""
        
    #projection = {"_id":0,"pull_request_status": 1}
    opened_pr=db.ranking.find({"$and":[{"Lab":lab_prefix},{"State": "open"}]}).count()
    closed_pr=db.ranking.find({"$and":[{"Lab":lab_prefix},{"State": "closed"}]}).count()
    grade_time = db.ranking.find({"Lab":lab_prefix},{'Creado':1,'Closed':1})
    grade_time_list=[]
    for i in grade_time:
        op = datetime.fromisoformat(i['Creado'].replace('Z',''))
        cl = datetime.fromisoformat(i['Closed'].replace('Z',''))
        grade_time_list.append((cl-op).total_seconds())

    result={'-El numero de PR abiertas es:': opened_pr,
    '-El numero de PR cerradas es:': closed_pr,
    '-El porcentaje de PR cerradas es': f'{int((closed_pr/(opened_pr+closed_pr)*100))}%',
    '-Lista de estudiantes con PR pendiente (labs individuales)':23-(closed_pr+opened_pr),   
    '-Maximum grade time': (f'{str(round(max(grade_time_list)/3600,2))}h'),
    '-Minimum grade time': (f'{str(round(min(grade_time_list)/3600,2))}h'),
    '-Mean grade time': (f'{str(round(np.mean(grade_time_list)/3600,2))}h')
    }

    return dumps(result)

@app.route("/lab/memeranking")
def meme_ranking():

    pass

@app.route("/lab/<lab>/meme")
def random_meme(lab):
    result=db.ranking.aggregate([
        { "$match": {"$and": [{"Lab":lab},{"State": "closed"}]}},
        { "$sample": {"size": 1} }, 
        { "$project" : { "InstructorCommentImage" : 1, "_id": 0}}
      ])
    return dumps(result)


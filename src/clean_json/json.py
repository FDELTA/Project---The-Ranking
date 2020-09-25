import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
import re
import pandas as pd
from datetime import datetime
from cleaning_regex_functions import *

def getpull (x,token= os.getenv("TOKEN"), query_params = {}):
        headers = {
            "Authorization": f"token {token}"}
        res = requests.get(f'https://api.github.com/repos/ironhack-datalabs/datamad0820/pulls/{x}', headers=headers)

        data = res.json()
        comment=getcomments(x)
        if res.status_code == 404:
            return 'exit'
        else:
            return {
                #"Title":cleantitle(data['title']),
                "Id":data['number'],
                "Lab":lab(data['title']),
                "State":data['state'],
                "User":data['user']['login'],
                "Creado":data['created_at'],
                "Closed":data['closed_at'],
                "Comentario":data['body'],
                "Instructor":instructor(comment),
                "InstructorComment":instructorcomment(comment),
                "InstructorCommentImage":https(comment),
                "InstructorGrades":putasnotas(comment)
        }

data=[]
for i in range(1,600):
    if getpull(i) == 'exit':
        pass
    else:
        data.append(getpull(i))

proyectito = json.dumps(data)
jsn = pd.DataFrame(data)
jsn.to_json('output/pull.json',orient="records")

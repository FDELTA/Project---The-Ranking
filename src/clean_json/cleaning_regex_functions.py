import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
import re
import pandas as pd
from datetime import datetime

def getcomments(comment,token= os.getenv("TOKEN")):
    headers = {"Authorization": f"token {token}"}
    res=requests.get(f'https://api.github.com/repos/ironhack-datalabs/datamad0820/issues/{comment}/comments',headers=headers)
    data=res.json()
    return data
def regex(x):
    return re.findall('@\w*-?\w+', x)
def image(x):
    return re.sub(re.findall('\((.*?)\)',x))
def cleantitle(x):
    return ((str(re.findall('\[(.*?)\]',x)).split('['))[1].split("'"))[1]
def instructorcomment(comment):
    try:
        return re.findall('@\w*-?\w+',comment[0]['body'])
    except:
        return None
    
def https(comment):
    try:
        try:
            z = re.findall(r'https:.*jpg|.*png|.*jpeg',comment[0]['body'])
            z = str(z).split('(')
            z = z[1].split("'")
            return z[0]
        except: 
            z = re.findall(r'https:.*jpg|.*png|.*jpeg',comment[0]['body'])
            z = str(z).split('(')
            return z[0]
    except:
        return None 
def instructor(comment):
    try:
        return comment[0]['user']['login']
    except:
        return None
def putasnotas(comment):
    try:
        z= re.findall(r'grade:.*-',comment[0]['body'])
        z = str(z).split(':')
        z = z[1].split("-")
        return z[0]
    except:
        return None
def lab(data):
    try:
        return re.findall(r'\[(.*?)\]',data)[0]
    except: return None
    
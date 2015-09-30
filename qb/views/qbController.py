import json
import sys

__author__ = 'gaurav'

import re
from compiler.ast import  flatten
from qb import app
from flask import Flask, request, render_template, redirect
import requests.packages.urllib3
from qb.models import QuickBooks
import qb.database.mongohelper as database

# 405455666
# 1425017975

map = {'consumer_key': 'qyprdMYtVFGlwgkX15mGXVb1CLRpuz',
       'consumer_secret': 'ZfQ6wJRrOj4F4NhcHTfopiffxK1wwv0WdJVQXu7T'
       }

map2 = {'consumer_key': 'qyprdMYtVFGlwgkX15mGXVb1CLRpuz',
        'consumer_secret': 'ZfQ6wJRrOj4F4NhcHTfopiffxK1wwv0WdJVQXu7T'
        }
requests.packages.urllib3.disable_warnings()


@app.route("/main", methods=['GET', 'POST'])
def main():
    if request.method == "GET":
        return render_template('main.html')
    if request.method == 'POST':
        try:
            data = request.form
            map.update({'access_token': data.get('qbaccesstoken_1')})
            map.update({'access_token_secret': data.get('qbaccesstokensecret_1')})
            map.update({'company_id': data.get('companyid_1')})
            map2.update({'access_token': data.get('qbaccesstoken_2')})
            map2.update({'access_token_secret': data.get('qbaccesstokensecret_2')})
            map2.update({'company_id': data.get('companyid_2')})
            enities=data.getlist("entities")
            qb1 = QuickBooks.QuickBooks(**map)
            qb1.create_session()
            qb2 = QuickBooks.QuickBooks(**map2)
            qb2.create_session()
            theresult=[]
            for values in enities:
                list1 = qb1.query_objects(values)
                if list1:
                    database.mongohelper.insertindatabse("system_data","qb",list1)
                list2 = qb2.query_objects(values)
                if list2:
                    database.mongohelper.insertindatabse("system_data","qb",list2)
                if len(list1) < len(list2):
                    result = compare(list1, list2,values)
                else:
                    result = compare(list2, list1,values)
                filterresults(result)
                theresult.append(result)
            theresult=filter(None,theresult)
            return render_template('result.html', theresult=theresult)
        except :
            print  sys.exc_info()
            return redirect("/main")



def filterresults(inputlist):
    i=0
    while(i<len(inputlist)):
        inputlist[i]=[e for e in inputlist[i] if e]
        inputlist[i]=flatten(inputlist[i])
        i += 1


def compare(list1, list2,entity):
    i = 0
    mainlist = []
    while (i < len(list1)):
        comparelist = compareDictOfDict(list1[i], list2[i])
        comparelist.insert(0, "the "+entity + " ID is in qb1 is " + str(list1[i].get("Id")) + " and in qb2 is " + str(
            list2[i].get("Id")))
        mainlist.append(comparelist)
        i = i + 1
    return mainlist


def compareDictOfDict(dict1, dict2):
    resultList = []
    for keys in dict1:
        # ignoring Time Stampe
        if "id" in str(keys).lower() or ifTimeStamp(str(dict1.get(keys))) != None:
            continue
        if not isinstance(dict1.get(keys), dict):
            if dict1.get(keys) != dict2.get(keys):
                resultList.append(
                    "the value of " + str(keys).upper() + " in qb1 is " + str(dict1.get(keys)).upper() + " but in qb2 is " + str(
                        dict2.get(keys)).upper())
        elif isinstance(dict1.get(keys), dict) and dict2.get(keys) != None:
            resultList.append(compareDictOfDict(dict1.get(keys), dict2.get(keys)))
        else:
            resultList.append("the value of " + keys + " is present in qb1 but not in qb2")
    return resultList


def ifTimeStamp(str):
    pattern = re.compile('\d\d\d\d-\d\d-\d\d(T)\d\d:\d\d:\d\d-\d\d:\d\d')
    return re.match(pattern, str)

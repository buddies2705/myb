import json

__author__ = 'root'

from qb import app
from qb.views.Comparehelper import Comparehelper
from flask import Flask, request, render_template, redirect
import requests.packages.urllib3

comparehelper=Comparehelper()
output=[]

@app.route('/shopifymain', methods=['GET', 'POST'])
def shopifymain():
    if request.method == 'GET':
        return render_template("shopify.html")
    elif request.method == 'POST':
        data = request.form
        data.getlist('shopname_1')
        shopname1 = data.get('shopname_1')
        shoptoken1 = data.get('shoptoken_1')
        shopname2 = data.get('shopname_2')
        shoptoken2 = data.get('shoptoken_2')
        enities = data.getlist("entities")
        if shopname1 is not None and shoptoken1 is not None and shopname2 is not None and shoptoken2 is not None:
            resultlist=[]
            for values in enities:
                list1=prepareAndMakeRequest(shopname1,shoptoken1,values)
                list2=prepareAndMakeRequest(shopname2,shoptoken2,values)
                i=0
                mainlist=[]
                if(len(list1)<=len(list2)):
                    while (i<len(list1)):
                        mainlist.append(comparehelper.compareDictOfDict(list1[i],list2[i]))
                        i+=1
                else:
                    while (i<len(list2)):
                        mainlist.append(comparehelper.compareDictOfDict(list2[i],list1[i]))
                        # comparehelper.filterresults(mainlist[i])
                        global output
                        output=[]
                        filter(mainlist[i])
                        mainlist[i]=output
                        i+=1
                resultlist.append(mainlist)
        return render_template("result.html",theresult=resultlist)

def prepareAndMakeRequest(shopname, headerValue,entity):
    s = requests.Session()
    response = s.get('https://' + shopname + '.myshopify.com/admin/'+entity+'.json',
                     headers={'X-Shopify-Access-Token': headerValue})
    json_data = json.loads(response.text)
    list = json_data[entity]
    return list


def filter(inputlist):
    for values in inputlist:
            if isinstance(values,list):
                filter(values)
            else:
                output.append(values)

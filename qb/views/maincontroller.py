from flask import Flask, request, render_template, redirect
from qb import app
import requests.packages.urllib3

@app.route("/", methods=['GET', 'POST'])
def maincontrol():
    if request.method=="GET":
        return render_template('index.html')
    if request.method=="POST":
        try:
            data=request.form
            if "shopify" in data:
                return redirect("/shopifymain")
            elif "quickbook" in data:
                return redirect("/qbmain")
        except:
            return redirect("/")
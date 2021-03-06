# -*- coding: utf-8 -*-
from flask import Flask,render_template,request
from jinja2 import Template
import data, unicodedata

app = Flask(__name__)

@app.route("/")
def home_page():
    """Home Page"""
    #Initiate DataFile 
    db = data.init()
    #Code for Last Updated projects
    sorted_list = data.search(db, sort_by="end_date")
    x = 0
    udb = []
    for proj in sorted_list:
        udb.append(proj)
        x += 1
        #Only add three last updated then break
        if x == 3:
            break
    return render_template("home.html", dataB = db, updatedPro = udb)

@app.route("/list", methods=['GET', 'POST'])
def list_page():
    """List Page"""
    db = data.init()
    fields = data.get_fields(db)
    #If user is searhing (POST)
    if request.method == 'POST':
        search_list = []
        for x in data.get_fields(db):
            #only add to list if x exists otherwise pass
            try:
                search_list.append(request.form[x])
            except:
                pass
        if search_list == []:
            search_list = None
        #Selects how it should sort the list
        sort_order = request.form["sort_order"]
        db = data.search(db, search=request.form["search"],sort_order=sort_order, search_fields=search_list)
    return render_template("list.html",dataB = db, _fields = fields)

@app.route("/techniques", methods=['GET', 'POST'])
def list_tech():
    """ Techniques page """
    db = data.init()
    techs = data.get_techniques(db)
    all_techniques = techs
    #If user is searching (post)
    if request.method == 'POST':
        tech_list = []
        for x in all_techniques:
            #only add to list if x exist otherwise pas
            try:
                if not request.form[x] in tech_list:
                    tech_list.append(request.form[x])
            except:
                pass
        if not tech_list == []:
            #To display all the techniques in a good way
            db = data.search(db, techniques = tech_list)
            techs = data.get_techniques(db)
            return render_template("list_techniques.html", dataB = db, techniques = techs, all_tech = all_techniques, selected_tech = tech_list)
    return render_template("list_techniques.html", dataB = db, techniques = techs, all_tech = all_techniques, selected_tech = techs)


@app.route("/portfolio/<id>")
def id_page(id):
    """ Portfolio id page """
    db = data.init()
    #loads the given id
    project = data.get_project(db,id)
    #if project dont exist, display 404 error
    if project == None:
        return render_template("404.html")
    return render_template("portfolio.html",dataB = project)

@app.errorhandler(404)
def error_404(e):
    """ 404 Error Handler """
    return render_template("404.html"),404

if __name__ == "__main__":
    app.debug = True
    app.run()



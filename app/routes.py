from app import app

from flask import make_response, render_template, request, jsonify
from app.engine.searchingKeyword_webFunc import search_keyword_function
import pandas as pd

df_rep_Keyword = pd.read_excel("./keyword_table/xlsx/Table_RepKeyword_xlsx.xlsx", header=0)
df_searching_keyword = pd.read_excel("./keyword_table/xlsx/Table_SearchingKeyword_xlsx.xlsx", header=0)
print("Read Keyword Data Success!!!!")


@app.route("/")
@app.route('/index')
def index():
    headers = {'Content-Type': 'text/html'}
    templates = render_template("index.html")
    return make_response(templates, 200, headers)


@app.route('/search', methods=["GET", "POST"])
def search():
    headers = {'Content-Type': 'text/html'}

    if request.method == "GET":
        templates = render_template("search.html")
        return make_response(templates, 200, headers)
    else:
        input_keyword = request.form["inputText"]
        result = search_keyword_function(input_keyword, 5, df_rep_Keyword, df_searching_keyword)
        return jsonify({"result": result})


@app.route('/test')
def test():
    return search_keyword_function('Tensorf', 5, df_rep_Keyword, df_searching_keyword)

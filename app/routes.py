from app import app

from flask import make_response, render_template, request, jsonify
from app.engine.searchingKeyword_webFunc import searchKeywordFunction
import pandas as pd

df_RepKeyword = pd.read_excel("./keyword_table/xlsx/Table_RepKeyword_xlsx.xlsx", header=0)
df_SearchingKeyword = pd.read_excel("./keyword_table/xlsx/Table_SearchingKeyword_xlsx.xlsx", header=0)
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
        result = searchKeywordFunction(input_keyword, 5, df_RepKeyword, df_SearchingKeyword)
        return jsonify({"result": result})


@app.route('/test')
def test():
    return searchKeywordFunction('Tensorf', 5)[4]

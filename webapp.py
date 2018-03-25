from flask import Flask, render_template, request
from posfixa import infixa_posfixa

app = Flask(__name__)


@app.route("/")
def index():
    expressao_regular = request.args.get("expressao_regular", "")
    posfixa = infixa_posfixa(expressao_regular)
    return render_template("index.html", posfixa=posfixa, expressao_regular=expressao_regular)
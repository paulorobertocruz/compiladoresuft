from flask import Flask, render_template, request

from posfixa import infixa_posfixa
from KenThompson import ken_thompson

app = Flask(__name__)


@app.route("/")
def index():
    expressao_regular = request.args.get("expressao_regular", None)
    posfixa = ""
    afd = None
    afn = None
    if expressao_regular is not None:
        posfixa = infixa_posfixa(expressao_regular)
        afn = ken_thompson(posfixa)
        afd = afn.afd_from_afn()
        print(afd)

    return render_template("index.html", posfixa=posfixa, expressao_regular=expressao_regular, afd=afd, afn=afn)
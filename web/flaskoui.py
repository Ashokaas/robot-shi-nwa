# Librairie(s) utilisée(s)
from flask import *
from bdd import bdd as db

app = Flask(__name__)
database = db.BDD("bdd/identifier.sqlite")


@app.errorhandler(404)
def not_found(error):
    """Gestionnaire d'erreur 404"""
    """ -> REDIRECTION VERS LA PAGE D'ACCUEIL"""
    return redirect(url_for("index"))


@app.route("/story")
def story():
    """Page d'accueil"""
    return render_template("story.html")


@app.route("/")
@app.route("/index")
def index():
    """Page d'accueil"""
    return render_template("index.html",
                           explorations=database.request("get_all_exploration", []) ,
                           pilotes=database.request("get_all_pilote", []))


@app.route("/rechercher", methods=["GET"])
def rechercher():
    datas = request.args
    reponse = database.request("get", [datas["pilote"], datas["nom"], datas["date"]])
    print(reponse)
    return render_template("tableau.html", campagnes=reponse)


@app.route("/donnees", methods=["GET"])
def donnees():
    datas = request.args
    reponse = database.request("get_datas", [datas["pilote"], datas["nom"], datas["date"]])
    print(reponse)
    return render_template("donnees.html", campagne=reponse)





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1664, threaded=True, debug=True)

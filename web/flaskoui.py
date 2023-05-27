# Librairie(s) utilisée(s)
from flask import *
from bdd import bdd as db


# Initialisation de l'application Flask
app = Flask(__name__)
#database = db.BDD("bdd/identifier.sqlite")
database = db.BDD(r"c:\Users\antot\Desktop\robot-shi-nwa\web\bdd\identifier.sqlite")


# Gestionnaire d'erreur 404
@app.errorhandler(404)
def not_found(error):
    """Gestionnaire d'erreur 404"""
    """ -> REDIRECTION VERS LA PAGE D'ACCUEIL"""
    return redirect(url_for("index"))


# Route pour la page "story"
@app.route("/story")
def story():
    """Page d'accueil"""
    return render_template("story.html")


# Routes pour la page d'accueil
@app.route("/")
@app.route("/index")
def index():
    """Page d'accueil"""
    return render_template("index.html",
                           explorations=database.request("get_all_exploration", []),
                           pilotes=database.request("get_all_pilote", []))


# Route pour la recherche
@app.route("/rechercher", methods=["GET"])
def rechercher():
    datas = request.args
    reponse = database.request("get", [datas["pilote"], datas["nom"], datas["date"]])
    print(reponse)
    return render_template("tableau.html", campagnes=reponse)


# Route pour les données
@app.route("/donnees", methods=["GET"])
def donnees():
    datas = request.args
    reponse = database.request("get_datas", [datas["pilote"], datas["nom"], datas["date"]])
    print(reponse)
    return render_template("donnees.html", campagne=reponse)


# Lancement de l'application Flask
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1664, threaded=True, debug=True)

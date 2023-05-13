import secrets

# Librairie(s) utilisée(s)
from flask import *


# Module(s) utilisé(s)


# Initialisation de l'application Flask
app = Flask(__name__, template_folder="templates", static_folder="static")





@app.errorhandler(404)
def not_found(error):
    """Gestionnaire d'erreur 404"""
    """ -> REDIRECTION VERS LA PAGE D'ACCUEIL"""
    return redirect(url_for("index"))


@app.route("/")
def index():
    """Page d'accueil"""
    return render_template("index.html")


@app.route("/about")
def about():
    """Page à propos"""
    return render_template("about.html")



@app.route('/my_route', methods=['POST'])
def my_route():
    myList = request.get_json()
    print(myList)
    return jsonify({'result': myList})



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1664, threaded=True, debug=True)
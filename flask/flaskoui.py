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


@app.route("/story")
def story():
    """Page d'accueil"""
    return render_template("story.html")


@app.route("/")
@app.route("/index")
def index():
    """Page d'accueil"""
    return render_template("index.html")






@app.route('/my_route', methods=['POST'])
def my_route():
    global client
    myList = request.get_json()
    client.send("start_drive".encode())
    if myList == "avancer":
        print(1)
        client.send("start_drive".encode())
    elif myList == "stop_avancer":
        client.send("stop_drive".encode("utf8"))
    print(myList)
    return jsonify({'result': myList})



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1664, threaded=True, debug=True)
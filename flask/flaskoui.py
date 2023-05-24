import secrets

# Librairie(s) utilisée(s)
from flask import *
import socket
import atexit


def exit_handler():
    client.close()


atexit.register(exit_handler)

# POST /d HTTP/1.1
# ....

# Module(s) utilisé(s)


# Initialisation de l'application Flask
app = Flask(__name__, template_folder="templates", static_folder="static")


# Adresse IP et port TCP d'écoute du serveur
HOST = "127.0.0.1"
PORT = 2004

# Création de la socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion au serveur
client.connect((HOST, PORT))
client.send("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA".encode())
print(f"Connexion vers {HOST}:{PORT} reussie.")



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
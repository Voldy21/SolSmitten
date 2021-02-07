from flask import Flask
import ss_db as db

application = Flask(__name__)


@application.route("/")
def hello():
    details = db.get_details()
    string = ""
    for i in range(len(details)):
        string += "".join(str(details[i]))
        string += "\n"
    return string


if __name__ == "__main__":
    application.run()

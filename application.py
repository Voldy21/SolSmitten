from flask import Flask
import ss_db as db

application = Flask(__name__)


@application.route("/")
def hello():
    # details = db.get_details()
    # print(details)
    return "Hello World"


if __name__ == "__main__":
    application.run()

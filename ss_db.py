import pymysql

conn = pymysql.connect(
    host='aa1wroi7lsdck1e.cblj8nprhubx.us-east-2.rds.amazonaws.com',
    port=3306,
    user='admin',
    password='solsmitten',
    db='Users',

)

# # Table Creation
# cursor = conn.cursor()
# create_table = """
# create table User_Profile (user_email VARCHAR(30) PRIMARY KEY,
# user_id INT,
# user_name VARCHAR(30),
# user_password VARCHAR(30),
# user_score INT )

# """
# cursor.execute(create_table)
# hello


def insert_details(args):
    email = args.email
    firstName = args.firstName
    lastName = args.lastName
    password = args.password
    skinType = args.skinType
    skinFeel = args.skinFeel
    sensitivty = args.sensitivity
    goals = args.goals
    age = args.age
    stress = args.stress
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Sign_Up2 (FirstName, LastName, email, morningSkin, userPassword, sensitivity, goals, age, stress, skinType) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)",
                   (firstName, lastName, email, skinFeel, password, sensitivty, goals, age, stress, skinType))
    conn.commit()
    cursor.close()


def get_user_profile():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Sign_Up2")
    details = cursor.fetchall()
    cursor.close()
    return details


def delete_user_profile(name):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Sign_Up2 WHERE firstName=%s", [name])
        cursor.close()
        return "Success"
    except:
        return "Failure"

# read the data


def get_details():
    cursor = conn.cursor()
    cursor.execute("SELECT *  FROM Sign_Up2")
    details = cursor.fetchall()
    cursor.close()
    return details


def login(args):
    email = args.email
    password = args.password
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT * FROM Sign_Up2 WHERE email=%s AND userPassword=%s", [email, password])
    details = cursor.fetchall()
    cursor.close()
    return details

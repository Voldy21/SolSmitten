import pymysql

conn = pymysql.connect(
    host='solsmitten.cxlp2fnydlpe.us-east-1.rds.amazonaws.com',
    port=3306,
    user='admin',
    password='jdtgr9704',
    db='Solsmitten',
    cursorclass=pymysql.cursors.DictCursor

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
    username = args.username
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (FirstName, LastName, email, skinFeel, password, sensitivity, goals, age, stress, skinType, username) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s)",
                   (firstName, lastName, email, skinFeel, password, sensitivty, goals, age, stress, skinType, username))
    conn.commit()
    cursor.close()


def delete_user_profile(name):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Users WHERE firstName=%s", [name])
        cursor.close()
        return "Success"
    except:
        return "Failure"

# read the data


def get_details():
    cursor = conn.cursor()
    cursor.execute("SELECT *  FROM Users")
    details = cursor.fetchall()
    cursor.close()
    return details


def login(args):
    username = args.username
    password = args.password
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT * FROM Users WHERE username=%s AND password=%s", [username, password])
    details = cursor.fetchall()
    cursor.close()
    return details

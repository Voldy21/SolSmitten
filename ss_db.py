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
    email = args['Email']
    firstName = args['First name']
    lastName = args['Last name']
    password = args['Password']
    skinType = args['Skin type']
    skinFeel = args['Skin feel']
    sensitivty = args['Sensitivity']
    goals = args['Goals']
    age = args['Age']
    stress = args['Stress']
    username = args['Username']
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (FirstName, LastName, email, skinFeel, password, sensitivity, goals, age, stress, skinType, username) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s)",
                   (firstName, lastName, email, skinFeel, password, sensitivty, goals, age, stress, skinType, username))
    conn.commit()
    cursor.execute(
        "SELECT * FROM Users WHERE username=%s", (username))
    user_id = cursor.fetchone()
    conn.commit()
    cursor.close()
    return user_id


def update_details(args):
    email = args['Email']
    firstName = args['First name']
    lastName = args['Last name']
    password = args['Password']
    skinType = args['Skin type']
    skinFeel = args['Skin feel']
    sensitivty = args['Sensitivity']
    goals = args['Goals']
    age = args['Age']
    stress = args['Stress']
    username = args['Username']
    user_id = args['user_id']
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET FirstName = %s, LastName = %s, email = %s, skinFeel =%s, password =%s, sensitivity = %s, goals =%s, age =%s, stress =%s, skinType =%s, username =%s) WHERE primary_key = %s)",
                   (firstName, lastName, email, skinFeel, password, sensitivty, goals, age, stress, skinType, username, user_id))
    conn.commit()
    cursor.execute(
        "SELECT * FROM Users WHERE username=%s", (username))
    user_id = cursor.fetchone()
    conn.commit()
    cursor.close()
    return user_id


def insert_image_details(wrinkleUrl, originalUrl, wrinkleScore, userID, ):
    # try:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO images (user_id, wrinkle_link, original_link, wrinkle_score) VALUES (%s, %s, %s, %s)",
                   (userID, wrinkleUrl, originalUrl, wrinkleScore))
    conn.commit()
    cursor.close()
    return "succcess"
    # except:
    #     return "failure"


def delete_user_profile(name):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Users WHERE lastName=%s", [name])
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


def get_Image_details():
    cursor = conn.cursor()
    cursor.execute("SELECT *  FROM images")
    details = cursor.fetchall()
    cursor.close()
    return details


def get_user_Image_details(user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT *  FROM images WHERE user_id=%s", [user_id])
    details = cursor.fetchall()
    cursor.close()
    return details


def insertImageDetails():
    cursor = conn.cursor()
    cursor.execute("SELECT *  FROM Users")
    details = cursor.fetchall()
    cursor.close()
    return details


def getUser_ID(username):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT primary_key FROM Users WHERE username=%s", (username))
        details = cursor.fetchone()
        cursor.close()
        return details
    except:
        return "failure"


def login(args):
    username = args.username
    password = args.password
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(
        "SELECT * FROM Users WHERE username=%s AND password=%s", [username, password])
    details = cursor.fetchall()
    cursor.close()
    return details


def delete_all():
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Users WHERE firstName=%s", ["b%"])
        cursor.close()
        return "Success"
    except:
        return "Failure"


def delete_all_images():
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM images")
        cursor.close()
        return "Success"
    except:
        return "Failure"


def getData(args):
    user_id = int(args['user_id'])
    print(user_id)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images WHERE user_id=%s", [user_id])
    details = cursor.fetchall()
    cursor.close()
    return details


def getName(args):
    user_id = int(args['user_id'])
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Users WHERE primary_key=%s", [user_id])
    details = cursor.fetchone()
    cursor.close()
    return details

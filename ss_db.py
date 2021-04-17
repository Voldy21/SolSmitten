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

def add_image_details(args):
    file_id = args['File Id']
    image_link = args['Image Link']
    blackspots_score = args['Blackspots Score']
    acne_score = args['Acne Score']
    wrinkles_score = args['Wrinkles Score']
    name = args['Name']
    user_id = args['User Id']
    date = args['Date']
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Images (file_id, name, image_link, blackspots_score, acne_score, wrinkles_score, user_id, date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                   (file_id, name, image_link, blackspots_score, acne_score, wrinkles_score, user_id, date))
    conn.commit()
    cursor.execute(
        "SELECT * FROM Users WHERE username=%s", (user_id))
    file_id = cursor.fetchone()
    conn.commit()
    cursor.close()
    return file_id

def insert_image_details(wrinkleUrl, originalUrl, wrinkleScore, userID, ):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Images (user_id, wrinkle_link, original_link, wrinkles_score) VALUES (%s, %s, %s, %s)",
                       (userID, wrinkleUrl, originalUrl, wrinkleScore))
        conn.commit()
        cursor.close()
        return "succcess"
    except:
        return "failure"


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
    cursor.execute("SELECT *  FROM Image")
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

# def assign_image_name(acne_score, blackspots_score, wrinkles_score, user_name):
#     if acne_score > blackspots_score and acne_score > wrinkles_score:
#         # Give name "acne*UserName**ImageNumber*"
#         image_name = "acne"
#     elif blackspots_score > acne_score and blackspots_score > wrinkles_score:
#         # Give name "blackspots*UserName**ImageNumber*"
#         image_name = "Blackspots"
#     else:
#         # Give name "wrinkles*UserName**ImageNumber*"
#         image_name = "wrinkles"
#     return image_name


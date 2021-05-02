import pymysql

conn = pymysql.connect(
    host='solsmitten.cblj8nprhubx.us-east-2.rds.amazonaws.com',
    port=3306,
    user='admin',
    password='jdtgr9704',
    db='Solsmitten',
    cursorclass=pymysql.cursors.DictCursor

)


def insert_details(args):
    try:
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
        # See if user currently exists
        cursor.execute(
            "SELECT * FROM Users WHERE username=%s", (username))
        user_id = cursor.fetchone()
        conn.commit()
        if not user_id:
            cursor.execute("INSERT INTO Users (FirstName, LastName, email, skinFeel, password, sensitivity, goals, age, stress, skinType, username) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s)",
                        (firstName, lastName, email, skinFeel, password, sensitivty, goals, age, stress, skinType, username))
            conn.commit()
            cursor.execute(
                "SELECT * FROM Users WHERE username=%s", (username))
            conn.commit()
            return "success"
        else:
            return "username taken"
    except Exception as e:
        return {"message": e}
    finally:
        cursor.close()


def update_details(args):
    try:
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
        exists = check_if_user_exists(user_id)
        cursor = conn.cursor()
        if exists:
            cursor.execute("UPDATE Users SET FirstName = %s, LastName = %s, email = %s, skinFeel =%s, password =%s, sensitivity = %s, goals =%s, age =%s, stress =%s, skinType =%s, username =%s) WHERE primary_key = %s)",
                        (firstName, lastName, email, skinFeel, password, sensitivty, goals, age, stress, skinType, username, user_id))
            conn.commit()
            return "success"
        else:
            return "User does not exist."
    except Exception as e:
        return "Failed to update."
    finally:
        cursor.close()


def insert_image_details(wrinkleUrl, originalUrl, wrinkleScore, userID):
    try:
        exists = check_if_user_exists(userID)
        print(exists)
        cursor = conn.cursor()
        if exists: 
            cursor.execute("INSERT INTO images (user_id, wrinkle_link, original_link, wrinkle_score ) VALUES (%s, %s, %s, %s)",
                        (userID, wrinkleUrl, originalUrl, wrinkleScore))
            conn.commit()
            return "success"
        else:
            return "Failure. User ID is invalid"
    except Exception as e:
        return e
    finally:
        cursor.close()

def check_if_user_exists(user_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE primary_key=%s", (user_id))
        user_id = cursor.fetchone()
        conn.commit()
        return user_id
    except Exception as e:
        return e
    finally: 
        cursor.close()    

def update_image_details_acne(fileID, acneURL, acneScore):
    cursor = conn.cursor()
    cursor.execute("UPDATE images SET acne_link=%s, acne_score=%s WHERE file_id=%s",
                   (acneURL, acneScore, fileID))
    conn.commit()
    cursor.close()


def delete_user_profile(name):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Users WHERE lastName=%s", [name])
        return "Success"
    except:
        return "Failure"
    finally:
        cursor.close()

# read the data


# def get_details():
#     cursor = conn.cursor()
#     cursor.execute("SELECT *  FROM Users")
#     details = cursor.fetchall()
#     cursor.close()
#     return details


# def get_Image_details():
#     cursor = conn.cursor()
#     cursor.execute("SELECT *  FROM images")
#     details = cursor.fetchall()
#     cursor.close()
#     return details


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
    try:
        username = args.username
        password = args.password
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM Users WHERE username=%s AND password=%s", [username, password])
        details = cursor.fetchall()
        conn.commit()
        return details
    except:
        return None
    finally:
        cursor.close()


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
    except Exception as e:
        return str(e)


# def getData(args):
#     user_id = args['user_id']
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM images WHERE user_id=%s", [user_id])
#     details = cursor.fetchall()
#     cursor.close()
#     return details


# def getName(args):
#     user_id = args['user_id']
#     cursor = conn.cursor()
#     cursor.execute(
#         "SELECT * FROM Users WHERE primary_key=%s", [user_id])
#     details = cursor.fetchone()
#     cursor.close()
#     return details

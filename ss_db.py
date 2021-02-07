import pymysql

conn = pymysql.connect(
        host= 'aa1wroi7lsdck1e.cblj8nprhubx.us-east-2.rds.amazonaws.com', 
        port = 3306,
        user = 'admin', 
        password = 'solsmitten',
        db = 'Users',
        
        )

# Table Creation
# cursor=conn.cursor()
# create_table="""
# create table User_Profile (user_email VARCHAR(30) PRIMARY KEY,
# user_id INT,
# user_name VARCHAR(30),
# user_password VARCHAR(30),
# user_score INT )

# """
# cursor.execute(create_table)

def insert_details(user_email, user_id, user_name, user_password, user_score):
    cursor=conn.cursor()
    cursor.execute("INSERT INTO User_Profile (user_email, user_id, user_name, user_password, user_score) VALUES (%s,%s,%s,%s,%s)", (user_email, user_id, user_name, user_password, user_score))
    conn.commit()

def get_user_profile():
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM User_Profile")
    details = cursor.fetchall()
    return details
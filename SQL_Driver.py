from sqlalchemy import dialects, create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import Session
from datetime import datetime
import os
import pandas as pd

def CreateSignUpTable():
    engine = create_engine('mysql+mysqlconnector://root:K#general10@localhost:3306/tholaspaan').connect()
    conn = engine.connect()
    query = f'''CREATE TABLE `new_user` (
                `user_id` INT AUTO_INCREMENT PRIMARY KEY,
                `firstname` varchar(250) NOT NULL,
                `lastname` varchar(250) NOT NULL,
                `phonenumber` varchar(250) NOT NULL,
                `email` varchar(250) NOT NULL,
                `password` varchar(250) NOT NULL,
                `datetime_signup` datetime NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            '''
    conn.execute(query)
    conn.close()

def CreateUserUsage():
    engine = create_engine('mysql+mysqlconnector://root:K#general10@localhost:3306/tholaspaan').connect()
    conn = engine.connect()
    query = f'''CREATE TABLE `user_usage` (
                `user_id` INT,
                `last_login` datetime NOT NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            '''
    conn.execute(query)
    conn.close()

def UpdateUserUsage(user,now):
    engine = create_engine('mysql+mysqlconnector://root:K#general10@localhost:3306/tholaspaan').connect()
    conn = engine.connect()
    query = f'''INSERT INTO user_usage 
                (user_id,last_login)
                VALUES ('{user['user_id'].iloc[0]}','{now}');
            '''
    conn.execute(query)
    conn.close()

def AppendSignUpTable(self):
    engine = create_engine('mysql+mysqlconnector://root:K#general10@localhost:3306/tholaspaan').connect()
    conn = engine.connect()
    query = f'''INSERT INTO new_user 
                (firstname, lastname, phonenumber, email, password)
                VALUES ('{str(self.email.text)}');
            '''
    conn.execute(query)
    conn.close()

def Check_Email(email):
    engine = create_engine('mysql+mysqlconnector://root:K#general10@localhost:3306/tholaspaan').connect()
    query = f'''SELECT phonenumber, email 
                    FROM new_user 
                    where email ='{email}'
                    '''
    check_email = pd.read_sql_query(query, engine)
    return check_email

def Check_User(email, phonenumber):
    engine = create_engine('mysql+mysqlconnector://root:K#general10@localhost:3306/tholaspaan').connect()
    query = f'''SELECT phonenumber, email 
                    FROM new_user 
                    where phonenumber ='{phonenumber}' 
                    and email ='{email}'
                    '''
    check_user = pd.read_sql_query(query, engine)
    return check_user



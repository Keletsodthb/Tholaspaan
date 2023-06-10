from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.toast import toast
from kivy.uix.floatlayout import FloatLayout
from sqlalchemy import dialects, create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import Session
from datetime import datetime
import os
import pandas as pd
import SQL_Driver

# class to accept user info and validate it
class loginWindow(Screen):
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)
    def validate(self):
        DB_USER = os.environ.get('DB_USER')
        engine = create_engine('mysql+mysqlconnector://root:K#general10@localhost:3306/tholaspaan').connect()
        #run query to check email/password
        query = f'''SELECT user_id 
                    FROM new_user 
                    where email ='{str(self.email.text)}' 
                    and password ='{str(self.pwd.text)}'
                '''

        user = pd.read_sql_query(query, engine)
        # check if email and password exist
        if user.empty:
            toast('Invalid Email/Password')
            # reset TextInput widget
            self.email.text = ""
            self.pwd.text = ""
        #else, if valid
        else:
            toast('SUCCESSFULLY LOGGED IN!')
            now = datetime.now()
            SQL_Driver.UpdateUserUsage(user, now)
            # reset TextInput widget
            self.email.text = ""
            self.pwd.text = ""

class signupWindow(Screen):
    firstname = ObjectProperty(None)
    lastname = ObjectProperty(None)
    phonenumber = ObjectProperty(None)
    email = ObjectProperty(None)
    pwd = ObjectProperty(None)
    def signupbtn(self):
        existing_user = SQL_Driver.Check_User(self.email.text, self.phonenumber.text)
        if self.firstname.text != "" and self.lastname.text != ""  and self.phonenumber.text != "" and self.email.text != "" and self.pwd.text != "":
            if self.email.text not in existing_user['email'].unique() and self.phonenumber.text not in existing_user['phonenumber'].unique():
                # if email and phone number do not exist already then insert into the user table
                # change current screen to log in the user now 
                engine = create_engine('mysql+mysqlconnector://root:K#general10@localhost:3306/tholaspaan').connect()
                conn = engine.connect()
                query = f'''INSERT INTO new_user 
                            (firstname, lastname, phonenumber, email, password, datetime_signup)
                            VALUES ('{self.firstname.text}', '{self.lastname.text}', '{self.phonenumber.text}', '{self.email.text}', 
                            '{self.pwd.text}', '{datetime.now()}');
            '''
                conn.execute(query)
                toast('Successfully created account')
                sm.current = 'login'
                self.firstname.text = ""
                self.lastname.text = ""
                self.phonenumber.text = ""
                self.email.text = ""
                self.pwd.text = ""
            elif str(self.phonenumber.text) in existing_user['phonenumber'].unique() or str(self.email.text) in existing_user['email'].unique():
                toast('User Already Exists!')

# class to display validation result
class forgotpasswordWindow(Screen):
    def forgotpwdbtn(self):
        existing_email = SQL_Driver.Check_Email(self.email.text)
        if self.email.text != "":
            if self.email.text in existing_email['email'].unique():
                msg = MIMEMultipart("alternative")
                msg['Subject'] = subject
                msg['From'] = 'piecejobmzansi@gmail.com'
                msg['To'] = ", ".join(test_recipients)

                conn.execute(query)
                toast('Successfully created account')
                sm.current = 'login'
                self.firstname.text = ""
                self.lastname.text = ""
                self.phonenumber.text = ""
                self.email.text = ""
                self.pwd.text = ""
            elif str(self.phonenumber.text) in existing_user['phonenumber'].unique() or str(self.email.text) in existing_user['email'].unique():
                toast('User Already Exists!')


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("login.kv")
sm = WindowManager()

# adding screens
sm.add_widget(loginWindow(name='login'))
sm.add_widget(signupWindow(name='signup'))
sm.add_widget(forgotpasswordWindow(name='forgotpassword'))

class loginMain(MDApp):
    def build(self):
        return sm

if __name__ == "__main__":
    loginMain().run()
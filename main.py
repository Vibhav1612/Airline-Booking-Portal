import mysql.connector
import login
import home
import search


file1=open('airline.txt','w')
str='WELCOME TO AIRLINE BOOKING PORTAL \n This is a portal that makes your flight booking process streamline and also offers other features such as a user login interface and also viewing of your prior bookings! Ready to begin? Press Y to continue!'
file1.write(str)
file1.close()
def inputscreen():
    while True:
        file1=open('airline.txt','r')
        r=file1.read()
        print(r)
        inp=input()
        if inp=='Y':
            break
        else:
            print('Wrong input. Please read the instructions again')
            inputscreen()
inputscreen()
username = ''

db = mysql.connector.connect(user = 'root', password = '****', host = 'localhost', database = 'airline')
cn = db.cursor()    

query = 'create table if not exists Users(UID int primary key, username varchar(30), password varchar(20), bank_detail varchar(20), city varchar(50), passport_det varchar(20))'
cn.execute(query)
cn.close()


username = login.login_page(username)
home.home_page(username)

import mysql.connector

db=mysql.connector.connect(user = 'root', password = '****', host = 'localhost', database = 'airline')
cn = db.cursor()

def create_user():
    global db
    global uid
    cn = db.cursor()
    #inputting initial data to create a user
    username = input('Enter username  ')
    cn.execute("select username from Users")
    l1 = cn.fetchall()
    l = []
    for i in l1:
        l.append(i[0])
    flag = True
    while flag: #to check if username already exists
        if username not in l:
            print('Valid username!')
            flag = False
        else:
            print('Invalid username')
            username = input('Enter username')

    flag = True
    while flag: #to check if password and re entered password matches
        password = input('Enter Password  ')
        x = input('Re-enter password to confirm  ')
        if x == password:
            print('Matching password confirmed! Proceed.')
            flag = False
            
    print('Bank details, Address, passport details are optional. You can enter it at the time of booking too, press S to skip')
    bank_detail = input('Enter your card number ')
    if bank_detail == 's' or bank_detail == 'S':
        bank_detail = 'null'
    city = input('Enter city ')
    if city == 's' or city == 'S':
        city = 'null'
    passport_det = input('Enter passport number ')
    if passport_det == 's' or passport_det == 'S':
        passport_det = 'null'
    cn.execute('select max(UID) from Users')

    prevuser = cn.fetchone()[0]
    if prevuser == None:
        uid = 0
    else:
        uid = prevuser + 1
    s = "insert into users values({}, '{}', '{}', '{}', '{}', '{}')".format(uid, username, password, bank_detail, city, passport_det)
    cn.execute(s)
    db.commit()

    s = "create table if not exists user_{}(UID int, flightID varchar(10), date date, destination varchar(15), departure varchar(15), airline varchar(15))".format(uid)
    cn.execute(s)
    db.commit()     
    cn.close()
    return username

def login_page(username):
    global uid
    end_login_page = False   #A variable to provide exit point from the create user/log in page
    while not(end_login_page):
        print('1 - Log In as existing user')
        print('2 - Create Account')
        o = int(input(''))
        cn = db.cursor()
        if o == 1:
            username = input('Enter username  ')
            cn.execute("select username from Users")
            l1 = cn.fetchall()
            l = []
            for i in l1:
                l.append(i[0])
            flag = True
            c = 0
            while flag: #to check if username exists
                if username in l:
                    print('Valid username!')
                    flag = False
                else:
                    print('This username does not exist. Try again.')
                    c += 1
                    username = input('Enter username  ')
                    if c > 5:
                        print('You have inputted the wrong username multiple times. Do you want to create a new account? (press Y)')
                        if input() in ['Y', 'y']:
                            username = create_user()
                            break
            if flag: #breaks out of outer loop also if user chooses to create a new acc
                break
            pw = input('Enter password ')
            cn.execute("select password from Users where username = '{}'".format(username))
            x = cn.fetchone()[0]
            c = 0
            flag = True
            while flag:
                if pw == x:
                    print('Welcome to AIRLINE booking portal')
                    flag = False
                    q = "select UID from Users where username = '{}'".format(username)
                    cn.execute(q)
                    uid = cn.fetchall()[0][0]
                    cn.close()
                else:
                    print('Invalid Password. Try Again.')
                    pw = input('Enter password ')
                    c += 1
                    if c > 5:
                        print('You have inputted the wrong password multiple times. Do you want to create a new account? (press Y)')
                        if input() in ['Y', 'y']:
                            username = create_user()
                            break
            end_login_page = True
        if o == 2:
            create_user()
            end_login_page = True
    
    return username

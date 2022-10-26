import search
import login
import mysql.connector
import smtplib, ssl

db=mysql.connector.connect(user = 'root', password = '*****', host = 'localhost', database = 'airline')

info = []
cla, pri, seat_no = 0,0,0
pay = ''

def history():
    global db
    cursor=db.cursor()
    qu="select * from user_{}".format(login.uid)
    cursor.execute(qu)
    tu=cursor.fetchall()
    if len(tu) == 0:
        print('You have not booked any flights yet!')
        return
    print('UID\tFlightID\tDate\t\tDeparture\tDestination\tAirline')
    for i in tu:
        print(i[0], end = '\t')
        for j in range(1,4):
            if len(str(i[j]))>=8:
                print(i[j], end = '\t')
            else:
                print(i[j], end = '\t\t')
        if len(str(i[4]))>=8:               
            print(i[4], end = '\t')
        else:
            print(i[4], end = '\t\t')
        print(i[5])
        print()

def send_mail(username):
    sender = 'abca86688@gmail.com'
    reciever = input('Enter your Email ID for confirmation of booking ')
    message = """
    Dear {},

    Thank You for choosing to fly with {}, 
    
    Your booking details are:
    FlightID:\t\t\t{}
    Date of Departure:{}, {}
    Departure:\t\t\t{}
    Destination:\t\t{}
    Class:\t\t\t{}
    Price:\t\t\t{}
    Seat Number:\t\t{}
    Payment Details:\t{}
    
    We hope to see you booking more flights with us. Bon Voyage. 

    """.format(username, info[0], info[4], search.date_dict[info[6]] , info[6], info[2], info[3], cla, pri, seat_no, pay)
    smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpObj.starttls
    smtpObj.login('abca86688@gmail.com', 'x0x0x0x0x0')
    smtpObj.sendmail(sender, reciever, message)
    print('Please Check your Email for a confirmation message. ')


def booking(username):
    global db
    global cla
    global pri
    global seat_no
    global pay
    search.menutable() #Shows the details of all the flights
    print()
    cn = db.cursor()
    cla=''
    pri=0
    print('Enter the flight number of the flight of your interest.')
    fligh = input()
    flag = False
    while not(flag):
        if fligh in search.matchedIDs:
            flag = True
        else:
            print('Invalid Flight number')
            print('Enter the flight number of the flight of your interest')
            fligh = input()

    q = 'select * from flight where FlightID = "{}"'.format(fligh)      #REM: Check condition for not entering right flight no.
    cn.execute(q)
    global info
    info = cn.fetchall()[0]
    col_seat = 0
    print('\t\t\tPrice\tSeats Available')
    print('Economy \t\t:', info[1], '\t', info[5])
    print('Premium Economy \t:', int(info[1]*1.1), '\t', info[7])
    print('Business class \t\t:', int(info[1]*1.3), '\t', info[8])
    print('First Class \t\t:', int(info[1]*1.8), '\t', info[9])
    print('1 - Economy')
    print('2 - Premium Economy')
    print('3 - Business')
    print('4 - First Class')
    cl = int(input('Which class would you like to fly in?'))
    
    if cl == 1:
        col_seat = 5    #To assign the column number in which the seats are saved for the given class
        cla='Economy'
        pri=info[1]
    elif cl == 2:
        cla='Premium Economy'
        col_seat = 7
        pri=info[1]*1.1
    elif cl == 3:
        cla='Business'
        col_seat = 8
        pri=info[1]*1.3
    elif cl == 4:
        cla='First'
        col_seat = 9
        pri=info[1]*1.8
    if info[col_seat] == 0:
        print('Sorry, there are no available seats on board for the class that you have chosen.')
        print('Do you want to choose another flight? (Y/N)')
        x = input()
        if x == 'Y':
            home_page(username)
        else:
            print('Thanks for visiting')
            return
    else:
        print('Flight Information:')
        print('')
        print('FlightID:\t\t', info[4])
        print('Airline:\t\t', info[0])
        print('Date of Departure:\t', search.date_dict[info[6]], ', ', info[6])
        print('Departure:\t\t', info[2])
        print('Destination:\t\t', info[3])
        print('Class:\t\t\t', cla)
        print('Price:\t\t\t', pri)
        if cl==1:
            print('Seats Remaining:\t:',info[5])
        elif cl==2:
            print('Seats Remaining\t:',info[7])    # PRINTING SEATS REMAINING
        elif cl==3:
            print('Seats Remaining\t:',info[8])
        elif cl==4:
            print('Seats Remaining\t:',info[9])
        
        flag = False
        x = input('Do you want to use your default payment options? (Y/N)')
        if x == 'Y':
            q = "select bank_detail from Users where UID = {}".format(login.uid)
            cn.execute(q)
            p = cn.fetchall()
            if len(p) != 0:
                print('Proceed to pay!')
                pay = p[0][0]
                flag = True
            else:
                print('You have not entered any payment details!')
                print('Enter your payment details')
                pay = input()
                q = "update Users set bank_detail = '{}' where UID = '{}'".format(pay, login.uid)
                cn.execute(q)
                db.commit()
                print('Proceed to Pay!')
                flag = True
                
        else:
            print('Enter your payment details')
            pay = input()
            chck = input('Do you want to set this as your default payment option? (Y/N)')
            if chck == 'Y':   
                q = 'update Users set bank_detail = {} where UID = {}'.format(pay, login.uid)
                cn.execute(q)
                db.commit()
            print('Proceed to Pay!')
            flag = True
            
        print('Are you sure you want to book this flight? (Y/N)')
        a = input()
        if a == 'Y':
            if cl==1:   #reducing seat number by 1
                qa="update {} set {}={}-1 where FlightID={}".format('flight','SeatsEconomy','SeatsEconomy',fligh)
                cn.execute(qa)
                db.commit()
                seat_no = 'E-' + str(info[5])
            elif cl==2:
                qa="update {} set {}={}-1 where FlightID={}".format('flight','SeatsPremiumEconomy','SeatsPremiumEconomy',fligh)
                cn.execute(qa)
                db.commit()
                seat_no = 'PE-' + str(info[7])
            elif cl==3:
                qa="update {} set {}={}-1 where FlightID={}".format('flight','SeatsBusiness','SeatsBusiness',fligh)
                cn.execute(qa)
                db.commit()
                seat_no = 'B-' + str(info[8])
            elif cl==4:
                qa="update {} set {}={}-1 where FlightID={}".format('flight','SeatsFirst','SeatsFirst',fligh)
                cn.execute(qa)
                db.commit()
                seat_no = 'F-' + str(info[9])
            print('Your seat number is -',seat_no) #printing seat number, E is used to signify economy as number of remaining seats, same for other classes as well
            print('Thank you for choosing ', info[0])
    
            
        if flag:
            que="insert into user_{} values({},'{}','{}','{}','{}','{}')".format(login.uid,login.uid,info[4],search.date_dict[info[6]],info[2],info[3],info[0])
            cn.execute(que)
            db.commit()
            cn.close()
            send_mail(username)
        else:
            o = input('Do you want to choose another flight? (Y/N)')
            if o == 'Y':
                booking(username)
            else:
                print('OK. BYE')
                return
        


def home_page(username):
    while True:
        print('1 - Book Flight')
        print('2 - View History')
        o = int(input())
        if o == 1:
            booking(username)
        if o == 2:
            print('Here is your booking history')
            history()
        else:
            print('Do you want to sign out and exit? (Y/N)')
            x = input()
            if x == 'Y' or x == 'y':
                print('Thank you for visiting')
                break

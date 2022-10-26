import mysql.connector
cnx= mysql.connector.connect(user = 'root', password = '****', host = 'localhost', database = 'airline')

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
month_dayno = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
month_dayno_leap = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]
jan1_2020 = 2
date_dict = {}

def leap(y):
    if y%4 != 0:
        return False
    else:
        if y%100 != 0:
            return True
        elif y%400 == 0:
            return True
        else:
            return False

def display(departure1,destination1,day1):
    global cnx
    cursor=cnx.cursor()
    global matchedIDs  #To save the flightIDs that are being displayed
    matchedIDs = []
    
    if (destination1 == 'all' and day1 == 'all'):
        q="select * from {} where Departure = '{}'".format('Flight',departure1)
        cursor.execute(q)
        tup=cursor.fetchall()
        if len(tup) == 0:
            print('Sorry there are no flights available')
            return 0
        print('Here are your required preferences:') 
        print('Company\t\tBase Cost\tDeparture\tDestination\tFlightID\tDeparture Date\tDay\t')
        for l in tup:
            for i in range(0, 5):
                if len(str(l[i]))>=8:
                    print(str(l[i]), end = '\t')
                else:
                    print(l[i], end = '\t\t')
            print(date_dict[l[6]], end = '\t')
            print(l[6])
            matchedIDs.append(l[4])

    elif departure1=='all' and day1 == 'all':
        q="select * from {} where Destination='{}'".format('Flight',destination1)
        cursor.execute(q)
        tup=cursor.fetchall()
        if len(tup) == 0:
            print('Sorry there are no flights available')
            return 0
        print('Here are your required preferences:') 
        print('Company\t\tBase Cost\tDeparture\tDestination\tFlightID\tDeparture Date\tDay\t')
        for l in tup:
            for i in range(0,5):
                if len(str(l[i]))>=8:
                    print(str(l[i]), end = '\t')
                else:
                    print(l[i], end = '\t\t')
            print(date_dict[l[6]], end = '\t')
            print(l[6])
            matchedIDs.append(l[4])

    elif day1 == 'all':
        q="select * from {} where Departure = '{}' and Destination = '{}'".format('Flight',departure1, destination1)
        cursor.execute(q)
        tup=cursor.fetchall()
        if len(tup) == 0:
            print('Sorry there are no flights available')
            return 0
        print('Here are your required preferences:') 
        print('Company\t\tBase Cost\tDeparture\tDestination\tFlightID\tDeparture Date\tDay\t')
        for l in tup:
            for i in range(0,5):
                if len(str(l[i]))>=8:
                    print(str(l[i]), end = '\t')
                else:
                    print(l[i], end = '\t\t')
            print(date_dict[l[6]], end = '\t')
            print(l[6])
            matchedIDs.append(l[4])

    else:
        q="select * from {} where Departure = '{}' and Destination = '{}' and DayOfDeparture = '{}'".format('Flight',departure1, destination1, day1)
        cursor.execute(q)
        tup=cursor.fetchall()
        if len(tup) == 0:
            print('Sorry there are no flights available')
            return 0
        print('Here are your required preferences:') 
        print('Company\t\tBase Cost\tDeparture\tDestination\tFlightID\tDeparture Date\tDay\t')
        for l in tup:
            for i in range(0,5):
                if len(str(l[i]))>=8:
                    print(str(l[i]), end = '\t')
                else:
                    print(l[i], end = '\t\t')
            print(date_dict[day1], end = '\t')
            print(l[6])
            matchedIDs.append(l[4])

def date(y,m,d):
    c = 0 #Effective(leap = 2) number of years ahead of 2020
    for i in range(2020, y):
        if leap(i):
            c += 2
        else:
            c += 1
    jan1_y = (jan1_2020 + c)%7

    if leap(y):
        day = month_dayno_leap[m-1] + d-1 #day is the Day number of the inputted date in its year
        x = (jan1_y + day)%7
    else:
        day = month_dayno[m-1] + d-1
        x = (jan1_y + day)%7
    day = days[x]
    return day
    
def date_dict_creation(y,m,d):
    global date_dict
    for i in range(-3, 4): #to iterate from 3 days before inputted date to 3 days after
        d1 = d+i
        m1 = m
        y1 = y
        if leap(y):
            msize = month_dayno_leap[m]-month_dayno_leap[m-1]
        else:
            msize = month_dayno[m]-month_dayno[m-1]
        if d1 <= 0:
            m1 = m - 1
            if m1 <= 0:
                y1 = y - 1
                m1 = 12
            if leap(y):                
                d1 = month_dayno_leap[m1] - month_dayno_leap[m1-1] + d1
            else:
                d1 = month_dayno[m1] - month_dayno[m1-1] + d1
        elif d1 > msize:
            m1 = m + 1
            d1 = d1 - msize
            if m1 > 12:
                y1 = y + 1
                m1 = 1
        date_dict[date(y1,m1,d1)] = str(y1) + '-' + str(m1) + '-' + str(d1)

#MENUTABLE
def menutable():
    from datetime import date as date1
    global cnx
    cnx=mysql.connector.connect(user = 'root', password = '***', host = 'localhost', database = 'airline')
    
    cur=date1.today()
    curda=str(cur)
    cursor=cnx.cursor()
    dat=input('Please enter your preferred date of departure in YYYY-MM-DD ')
    if dat>curda:
        y,m,d = dat.split('-')
        y,m,d = int(y), int(m), int(d)
        day = date(y,m,d)
        date_dict_creation(y,m,d)
        dest=input('Please enter your preffered destination ')
        depa=input('Please enter your city of departure ')
        t=(dest,depa,day)
        l=[]
        q="select Destination,Departure, DayOfDeparture from {}".format('Flight')
        cursor.execute(q)
        l.extend(cursor.fetchall())
        flag = True
        if t not in l:
            print('The exact preferences that you have entered have not been offered by our portal')
            q = "select * from Flight where Destination = '{}' and Departure = '{}'".format(dest, depa)
            cursor.execute(q)
            if len(cursor.fetchall()) == 0:
                flag = False
            if flag:
                print('Would you like to see other flights between', depa, 'and', dest, 'around the date that you have entered? (Y/N)')
                x = input()
                if x == 'Y' or x == 'y':
                    check = display(depa, dest, 'all')
            if not(flag) or x == 'N' or x == 'n':
                print('You can view the flight details for all the flights from the Departure city or to the Destination city.')
                print('Do you want to view based on:')
                print('1 - Departure')
                print('2 - Destination')
                print('3 - EXIT')
                o = int(input())
                if o == 1:
                    depa = input('Enter city of Departure ')
                    display(depa, 'all', 'all')
                elif o == 2:
                    dest = input('Enter Destination City ')
                    display('all', dest, 'all')
                else:
                    print('Thanks for Visiting')
                    return    
        else:
            print('The flights that match your requirements are')
            display(depa, dest, day)
    else:
        print('Please enter a valid date')
        menutable()
cnx.close()

#!/usr/bin/env python
import mysql.connector
import time
import sys
import select
import tty
import termios
import serial
import threading
from queue import Queue
from termios import tcflush, TCIOFLUSH
from escpos.printer import Usb
from mysql.connector import Error
from mysql.connector import errorcode


port='/dev/ttyUSB0'
s1=serial.Serial('/dev/ttyUSB0',9600)
s1.flushInput()

def up_database(database_up,q):
    owner_id = q.get()
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        passwd="qwerty123"
        )
        mycursor = mydb.cursor()
        mycursor.execute("Use ToolTax")
        if(owner_id>=1 and owner_id<=4):
            mycursor.execute("SELECT CAST(Curr_Credit AS INT) FROM Owner_Info WHERE owner_id=%s", (owner_id,))
            curr_amount = mycursor.fetchone()[0];
            if curr_amount<=0:
                q.put("false")
            else:
                q.put("true")
                #in_bill= "INSERT INTO Owner_Bill(Cr_Amount, Amount_Deducted, Arrival_time, owner_id) VALUES(%s,%s,CURTIME(),%s)"
                in_bill= "INSERT INTO Owner_Bill(Cr_Amount, Amount_Deducted,owner_id) VALUES(%s,%s,%s)"
                in_bill_val =(curr_amount-25,'25',owner_id)
                mycursor.execute(in_bill,in_bill_val)
                up_own_inf = "UPDATE Owner_Info SET Curr_Credit =%s WHERE owner_id =%s"
                up_own_val = (curr_amount-25,owner_id)
                mycursor.execute(up_own_inf,up_own_val)
                mydb.commit()
                print(mycursor.rowcount, "rows was inserted into Barcode Table.")
        else:
            print("Owner is not registered")
            
            
    except mysql.connector.Error as error:
        print("Failed to insert record {}".format(error))
    finally:
        if (mydb.is_connected()):
            mydb.close()
            print("MySQL connection is closed")


def printer_out(receipt_gen,q):
    owner_id = q.get()
    owner_name =""
    Vehicle_brand = ""
    Vehicle_No = ""
    Amount_in_Balance = ""
    bar_code = ""
    if(owner_id ==1):
        owner_name = "Mahwish Sheikh"
        Vehicle_brand = "Mitsubishi-Lancer"
        Vehicle_No = "ARW349"
        bar_code = "234953778376"
        
    elif (owner_id ==2):
        owner_name = "M.Sayeem Khan"
        Vehicle_brand = "Suzuki-Swift"
        Vehicle_No = "ABS472"
        bar_code = "247249535553"
        
    elif(owner_id ==3):
        owner_name = "Areeba Fatima"
        Vehicle_brand = "Toyota-Corolla"
        Vehicle_No = "IDM288"
        bar_code = "228853545947"
        
    else:
        owner_name = "Maheen Naz"
        Vehicle_brand = "Honda-Accord"
        Vehicle_No = "ABT950"
        bar_code = "295049484441"
        
    try:
        printer = Usb(0x0483,0x5743,0);
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        passwd="Apetite"
        )

        #Getting Amount in Balance from the database
        mycursor = mydb.cursor()
        mycursor.execute("Use ToolTax")
        mycursor.execute("SELECT CAST(Curr_Credit AS INT) FROM Owner_Info WHERE owner_id = %s", (owner_id,))
        Amount_in_Balance = mycursor.fetchone()[0]

        #Creating Printer Receipt
        printer.set(font='b', width=3, height=4, align='center', text_type='b')
        printer.image('logo.png', impl='bitImageColumn')
        printer.text('\n')
        now = time.strftime('%H:%M:%S')
        curr_date = time.strftime('%Y/%m/%d')
        printer.set(font='a',align='left');
        printer.text('Date: %s' % curr_date + '                 Time: %s\n' %now )
        printer.set(font='b',width=2, align='left', text_type='b')
        printer.text('--------------------------------')
        printer.set(font='a',align='left')
        printer.text('Owner Name:                %s\n' % owner_name)
        printer.text('Vehicle:                   %s\n' % Vehicle_brand)
        printer.text('Vehicle No:                %s\n' % Vehicle_No)
        printer.text('Station No:                M9 Motorway\n')
        printer.text('Tool Tax:                   Rs 25.00\n')
        printer.set(font='b',width=2, align='left', text_type='b')       
        printer.text('--------------------------------\n')
        printer.set(font='b' , width=2, align='left', text_type='b')
        printer.text('Amount In Balance:   RS %s.00\n' % Amount_in_Balance)
        printer.set(font='b',width=2, align='left', text_type='b')
        printer.text('--------------------------------')
        printer.text('\n')
        printer.text('\n')
        printer.set(text_type='b', align='center')
        printer.text('==========================\n')
        printer.set(font='a', align='center')
        printer.text('THIS IS YOUR OFFICIAL RECEIPT\n')
        printer.set(font='a', text_type='b', align='center')
        printer.text('Thank You Come Again!\n')
        printer.barcode('%s' % bar_code, 'UPC-A',64,2,'','')
        printer.text('\n')
        printer.text('\n')
        printer.cut()


    except mysql.connector.Error as error:
        print("Failed to query Amount in Balance{}".format(error))
    finally:
        if (mydb.is_connected()):
            mydb.close()
            print("MySQL connection is closed")


def readfromArd(readarduino , q):
    while True:
        val = int(s1.read().strip())
        if val == 1:
            print("Mahwish Here\n")
            #q.put(1)
            break;

def updateweb(queue, owner):
    queue.put(owner)
    my_thread=threading.Thread(target=up_database, name="database_up", args=("database_up", queue))
    my_thread.start()
    my_thread.join()
    isdbup = queue.get()
    if isdbup == "true":
        outfile = open ('/var/www/html/owner.txt','w')
        outfile.write(str(owner))
        outfile.close()
        queue.put(owner)
        receipt_thread = threading.Thread(target= printer_out, name="receipt_gen", args=("receipt_gen", queue))
        receipt_thread.start()
        receipt_thread.join()
        print("Receipt Generated Successfully")
        s1.write(str.encode("1"))
        time.sleep(10)
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)

def isData():
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
queue = Queue()
#my_thread=threading.Thread(target=readfromArd, name="readarduino", args=("readarduino", queue))
#my_thread.setDaemon(True)
#my_thread.start()        

while True:
    old_settings = termios.tcgetattr(sys.stdin)
    try:
        #tty.setcbreak(sys.stdin.fileno())
        while True:
            #print("inner loop")
            if isData():
                print("data is available")
                barcode= sys.stdin.readline().rstrip('\n')
                print("barcode:"+barcode)
                if barcode == '234953778376':  # Mahwish
                    print ("Mahwish Here\n")
                    updateweb(queue, 1)
                    break
                elif barcode =='247249535553': # Sayeem
                    print ("Mahwish Here\n")
                    updateweb(queue, 2)
                    break
                elif barcode =='228853545947': # Areeba
                    print("Areeba Here\n")
                    updateweb(queue, 3)
                    break
                else:                          # Maheen
                    print("Maheen Here\n")
                    updateweb(queue, 4)
            else:
                #print("reading arduino")
                if (s1.inWaiting()>0): #if incoming bytes are waiting to be read from the serial input buffer
                    arduino = s1.read(s1.inWaiting()).decode('ascii')
                    print(arduino)
                    if arduino == "3":
                        print ("Areeba detected through RFID")
                        updateweb(queue, 3)
                    elif arduino == "4":
                        print ("Maheen detected through RFID")
                        updateweb(queue, 4)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

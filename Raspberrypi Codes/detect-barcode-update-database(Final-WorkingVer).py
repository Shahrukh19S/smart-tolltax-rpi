
#!/usr/bin/env python
import mysql.connector
import threading
import time
import requests
from queue import Queue
from escpos.printer import Usb
from mysql.connector import Error
from mysql.connector import errorcode

def up_database(database_up,q):
    owner_id = q.get()
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        passwd="Apetite"
        )
        mycursor = mydb.cursor()
        mycursor.execute("Use ToolTax")
        if(owner_id>=1 and owner_id<=4):
            mycursor.execute("SELECT CAST(Curr_Credit AS INT) FROM Owner_Info WHERE owner_id=%s", (owner_id,))
            curr_amount = mycursor.fetchone()[0];
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
        owner_name = "Mahwish"
        Vehicle_brand = "Mitsubishi-Lancer"
        Vehicle_No = "ARW349"
        bar_code = "234953778376"
        
    elif (owner_id ==2):
        owner_name = "Sayeem"
        Vehicle_brand = "Suzuki-Swift"
        Vehicle_No = "ABS472"
        bar_code = "247249535553"
        
    elif(owner_id ==3):
        owner_name = "Areeba"
        Vehicle_brand = "Toyota-Corolla"
        Vehicle_No = "IDM288"
        bar_code = "228853545947"
        
    else:
        owner_name = "Maheen"
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

            
while True:
    barcode = input("Scan barcode_")
    queue=Queue()    
    print ("the barcode is:" + barcode)
    if barcode =='234953778376': # Mahwish
        print("Mahwish Here\n")
        queue.put(1)
        my_thread=threading.Thread(target=up_database, name="database_up", args=("database_up", queue))
        my_thread.start()
        my_thread.join()
        outfile = open ('/var/www/html/owner.txt','w')
        outfile.write("1")
        outfile.close()
        #queue.put(1)
        #receipt_thread = threading.Thread(target= printer_out, name="receipt_gen", args=("receipt_gen", queue))
        #receipt_thread.start()
        #receipt_thread.join()
        #print("Receipt Generated Successfully")
        
    elif barcode =='247249535553': # Sayeem
        print("Sayeem Here\n")
        queue.put(2)
        my_thread=threading.Thread(target=up_database, name="database_up", args=("database_up", queue))
        my_thread.start()
        my_thread.join()
        print("Database Updated for Sayeem")
        outfile = open ('/var/www/html/owner.txt','w')
        outfile.write("2")
        outfile.close()
    elif barcode =='228853545947': # Areeba
        print("Areeba Here\n")
        queue.put(3)
        my_thread=threading.Thread(target=up_database, name="database_up", args=("database_up", queue))
        my_thread.start()
        my_thread.join()
        print("Database Updated for Areeba")
        outfile = open ('/var/www/html/owner.txt','w')
        outfile.write("3")
        outfile.close()
    else:
        print("Maheen Here\n")
        queue.put(4)
        my_thread=threading.Thread(target=up_database, name="database_up", args=("database_up", queue))
        my_thread.start()
        my_thread.join()
        print("Database Updated for Maheen")
        outfile = open ('/var/www/html/owner.txt','w')
        outfile.write("4")
        outfile.close()
        

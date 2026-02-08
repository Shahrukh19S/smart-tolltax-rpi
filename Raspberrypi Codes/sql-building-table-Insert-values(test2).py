import mysql.connector
import time
from mysql.connector import Error
from mysql.connector import errorcode
try:
    mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    passwd="qwerty123"
    )
    mycursor = mydb.cursor()
    #mycursor.execute("CREATE DATABASE ToolTax DEFAULT CHARACTER SET utf8")
    mycursor.execute("Use ToolTax")
    #mycursor.execute("CREATE TABLE Owner (owner_id INT NOT NULL AUTO_INCREMENT, owner_name VARCHAR(255), barcode VARCHAR(255), INDEX USING BTREE(owner_name), PRIMARY KEY(owner_id))")
    #mycursor.execute("CREATE TABLE Owner_Info(o_info_id INT NOT NULL AUTO_INCREMENT, vehicle_Brand VARCHAR(255), vehicle_No VARCHAR(255), Curr_Credit INT, owner_id INT, INDEX USING BTREE(vehicle_Brand), PRIMARY KEY(o_info_id), CONSTRAINT FOREIGN KEY(owner_id) REFERENCES Owner(owner_id) ON DELETE CASCADE ON UPDATE CASCADE) ENGINE=InnoDB")
    #mycursor.execute("CREATE TABLE Owner_Bill(bill_No INT NOT NULL AUTO_INCREMENT, Cr_Amount INT, Amount_Deducted INT, Arrival_time TIME(0), Arrival TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, owner_id INT, INDEX USING BTREE(Arrival_time), PRIMARY KEY(bill_No), CONSTRAINT FOREIGN KEY(owner_id) REFERENCES Owner(owner_id) ON DELETE CASCADE ON UPDATE CASCADE) ENGINE=InnoDB")

    #in_Owner = "INSERT INTO Owner (owner_name, barcode) VALUES (%s,%s)"
    #Ownerbar = [('Mahwish','234953778376'),('Sayeem','247249535553'),('Areeba','228853545947'),('Maheen','295049484441')]    #mycursor.executemany(sql,val)
    #in_Owner_info ="INSERT INTO Owner_Info(vehicle_Brand,vehicle_No, Curr_Credit, owner_id) VALUES(%s,%s,%s,%s)" 
    #in_Owner_veh = [('Toyota-Corolla','IDM288','2000','3'),('Mitsubishi-Lancer','ARW349','2000','1'),('Honda-Accord','ABT950','2000','4'),('Suzuki-Swift','ABS472','2000','2')]
    #mycursor.executemany(in_Owner, Ownerbar)
    #mycursor.executemany(in_Owner_info, in_Owner_veh)
    #mycursor.execute("SELECT CAST(Curr_Credit AS INT) FROM Owner_Info WHERE owner_id=3")
    #curr_amount = mycursor.fetchone()[0];
    #ga = curr_amount -25;
    #now = time.strftime('%Y-%m-%S')
    #print(now)
    in_Owner_bill = "INSERT INTO Owner_Bill (Cr_Amount, Amount_Deducted, Arrival_time, owner_id) VALUES (%s,%s,CURTIME(),%s)"
    in_Owner_bival = [('2000','0','3'),('2000','0','1'),('2000','0','4'),('2000','0','2')]
    #mycursor.execute("INSERT INTO Owner_Bill(Arrival_time) VALUES(CURTIME())")
    #in_Owner_bival = [(curr_amount-25,'0',now,'3'),(curr_amount-25,'0',now,'1'),(curr_amount-25,'0',now,'4'),(curr_amount-25,'0',now,'2')] 
    #mycursor.execute("INSERT INTO Owner_Bill(Amount_Deducted, owner_id) VALUES('0','3')")
    #mycursor.execute("UPDATE Owner_Bill SET Amount_Deducted='25.00' WHERE owner_id='3'")
    mycursor.executemany(in_Owner_bill, in_Owner_bival)
    #sq= "UPDATE Owner_Info SET Curr_Credit=%s WHERE owner_id=%s"
    #va= (curr_amount-25,"3")
    #mycursor.execute(sq,va)
    #mycursor.execute("INSERT INTO Owner_Bill (Arrival,owner_id) VALUES('CONVERT(NVARCHAR,NOW(),100) AS [DD-MM-YYYY HH:MM:SS]','3')")
    mydb.commit()
    print(mycursor.rowcount, "rows was inserted into Barcode Table.")
    
except mysql.connector.Error as error:
    print("Failed to insert record into Barcode table {}".format(error))
finally:
    if (mydb.is_connected()):
        mydb.close()
        print("MySQL connection is closed")



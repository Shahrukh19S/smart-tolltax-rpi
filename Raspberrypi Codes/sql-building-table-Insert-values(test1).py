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
    #mycursor.execute("CREATE TABLE Owner_Info(o_info_id INT NOT NULL AUTO_INCREMENT, vehicle_Brand VARCHAR(255), vehicle_No VARCHAR(255), owner_id INT, INDEX USING BTREE(vehicle_Brand), PRIMARY KEY(o_info_id), CONSTRAINT FOREIGN KEY(owner_id) REFERENCES Owner(owner_id) ON DELETE CASCADE ON UPDATE CASCADE) ENGINE=InnoDB")
    #mycursor.execute("CREATE TABLE Owner_Bill(bill_No INT NOT NULL AUTO_INCREMENT, Cr_Amount INT, Amount_Deducted INT, Arrival_date DATE, Arrival TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, owner_id INT, INDEX USING BTREE(Arrival_date), PRIMARY KEY(bill_No), CONSTRAINT FOREIGN KEY(owner_id) REFERENCES Owner(owner_id) ON DELETE CASCADE ON UPDATE CASCADE) ENGINE=InnoDB")

    #in_Owner = "INSERT INTO Owner (owner_name, barcode) VALUES (%s,%s)"
    #Ownerbar = [('Mahwish','234953778376'),('Sayeem','247249535553'),('Areeba','228853545947'),('Maheen','295049484441')]    #mycursor.executemany(sql,val)
    #in_Owner_info ="INSERT INTO Owner_Info(vehicle_Brand,vehicle_No,owner_id) VALUES(%s,%s,%s)" 
    #in_Owner_veh = [('Toyota-Corolla','IDM288','3'),('Mitsubishi-Lancer','ARW349','1'),('Honda-Accord','ABT950','4'),('Suzuki-Swift','ABS472','2')]
    #mycursor.executemany(in_Owner, Ownerbar)
    #mycursor.executemany(in_Owner_info, in_Owner_veh)
    #now = time.strftime('%Y-%m-%d')
    #in_Owner_bill = "INSERT INTO Owner_Bill (Cr_Amount, Amount_Deducted, Arrival_Date, owner_id) VALUES (%s,%s,%s,%s)"
    #in_Owner_bival = [('2000','0',now,'3'),('2000','0',now,'1'),('2000','0',now,'4'),('2000','0',now,'2')] 
    #mycursor.execute("INSERT INTO Owner_Bill(Amount_Deducted, owner_id) VALUES('0','3')")
    #mycursor.execute("UPDATE Owner_Bill SET Amount_Deducted='25.00' WHERE owner_id='3'")
    mycursor.executemany(in_Owner_bill, in_Owner_bival)
    #mycursor.execute("INSERT INTO Owner_Bill (Arrival,owner_id) VALUES('CONVERT(NVARCHAR,NOW(),100) AS [DD-MM-YYYY HH:MM:SS]','3')")
    mydb.commit()
    print(mycursor.rowcount, "rows was inserted into Barcode Table.")
    
except mysql.connector.Error as error:
    print("Failed to insert record into Barcode table {}".format(error))
finally:
    if (mydb.is_connected()):
        mydb.close()
        print("MySQL connection is closed")



from escpos.printer import Usb
import time

printer = Usb(0x0483,0x5743,0);
printer.set(font='b', width=3, height=4, align='center', text_type='b');
printer.image('logo.png', impl='bitImageColumn');
printer.text('\n');
now = time.strftime('%H-%M-%S')
Curr_date = time.strftime('%Y-%m-%d')
printer.set(font='a',align='left')
#printer.text("%s" % now )
#printer.text('Date: 11/25/2019                 Time: 5:58 PM\n');
printer.text("Date: %s" % Curr_date + "                 Time: %s" %now);
#printer.text("                 Time: %s" % now)
printer.set(font='b',width=2, align='left', text_type='b');
printer.text('--------------------------------');
printer.set(font='a',align='left');
printer.text('Owner Name:                Abdullah Ansari\n');
printer.text('Vehicle:                   Toyota Corolla\n');
printer.text('Vehicle No:                KL14M5820\n');
printer.text('Station No:                M9 Motorway\n');
printer.text('Tool Tax:                   Rs 25.00\n');
printer.set(font='b',width=2, align='left', text_type='b');
printer.text('--------------------------------');
printer.set(font='b' , width=2, align='left', text_type='b');
printer.text('Amount In Balance:   RS 2000.00\n');
printer.set(font='b',width=2, align='left', text_type='b');
printer.text('--------------------------------');
printer.text('\n');
printer.text('\n');
printer.set(text_type='b', align='center');
printer.text('==========================\n');
printer.set(font='a', align='center');
printer.text('THIS IS YOUR OFFICIAL RECEIPT\n');
printer.set(font='a', text_type='b', align='center');
printer.text('Thank You Come Again!\n');
printer.barcode('1324354657687' , 'EAN13',64,2,'','');

printer.text('\n');
printer.text('\n');
printer.cut();

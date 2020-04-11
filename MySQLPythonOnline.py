#Online Database
from tkinter import *
from tkinter import messagebox
import sys,os

try:
    import mysql.connector
except:
    os.system("pip install mysql-connector-python")
    import mysql.connector
    os.system("clear")

def checkdb():
    #Connecting
    bool = TRUE
    while bool:
        bool,mydb,mycursor = checkinternet(FALSE)
    #Check for database
    mycursor.execute("SHOW DATABASES")
    flag = FALSE
    for x in mycursor:
        for i in x:
            if i == "sql12330813":
                flag = TRUE
                break

    #create databse if not exists
    if flag == FALSE:
        mycursor.execute("CREATE DATABASE sql12330813")

    mycursor.close()
    mydb.close()

def checktable(mydb, mycursor):
    #Check for Table
    mycursor.execute("SHOW TABLES")
    flag = FALSE
    for x in mycursor:
        for i in x:
            if i == 'Products':
                flag = TRUE
                break

    #Create table if it does not exist
    if flag == FALSE:
        mycursor.execute("CREATE TABLE Products (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255) NOT NULL, Price INT NOT NULL, Quantity INT NOT NULL)")

def checkentries(mydb, mycursor,buttons):
    mycursor.execute("SELECT * FROM Products")
    myresult = mycursor.fetchall()
    upd = buttons[1]
    dele = buttons[2]
    disp = buttons[3]
    if len(myresult) == 0:
        upd['state'] = DISABLED
        dele['state'] = DISABLED
        disp['state'] = DISABLED

    else:
        upd['state'] = NORMAL
        dele['state'] = NORMAL
        disp['state'] = NORMAL

def insertform(buttons):
      #used to show and hide the error label
    def insertformcheck():
        flag = 0
        if entname.get()== "" or entprice.get() == "" or entquantity.get() == "":
            flag = 1
            laberror.grid()

        if flag==0:
            try:
                float(entprice.get())
            except:
                flag = 1
                laberror.config(text = "*Please enter valid Price")
                laberror.grid()

        if flag==0:
            try:
                int(entquantity.get())
            except:
                flag = 1
                laberror.config(text = "*Please enter valid Quantity")
                laberror.grid()

        if flag==0:
            laberror.grid_remove()
            insertval(entname.get(),float(entprice.get()),float(entquantity.get()),buttons)
            inswin.grab_release()   #makes the root window active again
            inswin.destroy()


    inswin = Toplevel(root)
    inswin.grab_set()    #makes the root window inactive
    labtop = Label(inswin, text = "Insert Value")
    labtop.grid(row=0,column=1,columnspan = 3)

    labname = Label(inswin, text = "Name: ")
    labname.grid(row=1,column=1,pady=20,sticky=W)

    labprice = Label(inswin, text = "Price: ")
    labprice.grid(row=3,column=1,pady=20,sticky=W)

    labquantity = Label(inswin, text = "Quantity: ")
    labquantity.grid(row=5,column=1,pady=20,sticky=W)

    entname = Entry(inswin)
    entname.grid(row=1,column=3)

    entprice = Entry(inswin)
    entprice.grid(row=3,column=3)

    entquantity = Entry(inswin)
    entquantity.grid(row=5,column=3)

    laberror = Label(inswin, text = "*Please fill all details", fg = 'red')
    laberror.grid(row=6,column=1,columnspan=3)
    laberror.grid_remove()

    subbut = Button(inswin, text = "Submit", command = insertformcheck )
    subbut.grid(row=7,column=1, columnspan = 3,pady=20)

def insertval(Name,Price,Quantity,buttons):
    bool = TRUE
    while bool:
        bool,mydb,mycursor = checkinternet(TRUE)

    sql = "INSERT INTO Products (Name, Price, Quantity) VALUES (%s, %s, %s)"
    val = (Name,Price,Quantity)
    mycursor.execute(sql, val)
    mydb.commit()
    checkentries(mydb,mycursor,buttons)
    mydb.close()
    mycursor.close()

def updateform():

    def updateformcheck():
        flag1 = 0 #To check if all the details are proper in first half (1: Working, 0: Not Working)
        flag2 = 1  #to check if all the details are proper in second half (1: Working, 0: Not Working)

        bool = TRUE
        while bool:
            bool,mydb,mycursor = checkinternet(TRUE)

        if entname.get()== "" and entid.get() == "":
            flag1 = 0
            laberror.config(text = "*Please fill either of the details")
            laberror.grid()

        elif entid.get() != "":
            try:
                int(entid.get())
                sql = "SELECT * FROM Products WHERE id = %s"
                val = (entid.get())
                mycursor.execute(sql % val)
                myresult = mycursor.fetchall()

                if len(myresult) == 0:
                    flag1 = 0
                    laberror.config(text = "*No Entry with the ID entered. Please enter valid ID")
                    laberror.grid()

                else:
                    flag1 = 1
                    laberror.grid_remove()
            except:
                flag1 = 0
                laberror.config(text = "*Please enter valid ID")
                laberror.grid()

        elif flag1 == 0 and entname.get() != "":
            sql = "SELECT * FROM Products WHERE Name = '%s'"
            val = entname.get()
            mycursor.execute(sql % val)
            myresult = mycursor.fetchall()

            if len(myresult) == 0:
                laberror.config(text = "*No Record with the Name entered. Please enter valid Name")
                laberror.grid()

            elif len(myresult) >= 2:
                laberror.config(text = "*Multiple Records with the Name Entered. Please enter the ID instead.")
                laberror.grid()

            else:
                flag1 = 1
                laberror.grid_remove()


        if entname1.get()== "" or entprice1.get() == "" or entquantity1.get() == "":
            flag2 = 0
            laberror1.grid()

        if flag2 == 1:
            try:
                float(entprice1.get())
            except:
                print("Hello1")
                flag2 = 0
                laberror1.config(text = "*Please enter valid Price")
                laberror1.grid()

        if flag2 == 1:
            try:
                int(entquantity1.get())
            except:
                print("Hello2")
                flag2 = 0
                laberror1.config(text = "*Please enter valid Quantity")
                laberror1.grid()

        if flag2 == 1:
            flag2 = 1
            laberror1.grid_remove()

        if flag1 == 1 and flag2 == 1 and entid.get() != "":
            sql = "UPDATE Products SET Name = '%s', Price = %s, Quantity = %s WHERE id = %s"
            val = (entname1.get(),entprice1.get(),entquantity1.get(),entid.get())
            mycursor.execute(sql % val)
            mydb.commit()
            mycursor.close()
            mydb.close()
            updwin.grab_release()
            updwin.destroy()

        elif flag1 == 1 and flag2 == 1 and entname.get() != "":
            sql = "UPDATE Products SET Name = '%s', Price = %s, Quantity = %s WHERE Name = '%s'"
            val = (entname1.get(),entprice1.get(),entquantity1.get(),entname.get())
            mycursor.execute(sql % val)
            mydb.commit()
            mycursor.close()
            mydb.close()
            updwin.grab_release()
            updwin.destroy()

    updwin = Toplevel(root)
    updwin.grab_set()

    labtop = Label(updwin, text = "Enter either ID or Name of the record to be updated: ")
    labtop.grid(row=0,column=1,columnspan=3)

    labid = Label(updwin, text = "ID: ")
    labid.grid(row=1,column=1,pady=20,sticky=W)

    labname = Label(updwin, text = "Name: ")
    labname.grid(row=2,column=1,pady=20,sticky=W)

    entid = Entry(updwin)
    entid.grid(row=1,column=3)

    entname = Entry(updwin)
    entname.grid(row=2,column=3)

    laberror = Label(updwin, text = "*Please fill either of the details", fg = 'red')
    laberror.grid(row=3,column=1,columnspan=3,pady=20)
    laberror.grid_remove()

    Label(updwin).grid(row=6)

    labtwo = Label(updwin, text = "Enter the new values: ")
    labtwo.grid(row=5,column=1,columnspan=3,pady=20,sticky=W)

    labname1 = Label(updwin, text = "Name: ")
    labname1.grid(row=6,column=1,pady=20,sticky=W)

    labprice1 = Label(updwin, text = "Price: ")
    labprice1.grid(row=7,column=1,pady=20,sticky=W)

    labquantity1 = Label(updwin, text = "Quantity: ")
    labquantity1.grid(row=8,column=1,pady=20,sticky=W)

    entname1 = Entry(updwin)
    entname1.grid(row=6,column=3)

    entprice1 = Entry(updwin)
    entprice1.grid(row=7,column=3)

    entquantity1 = Entry(updwin)
    entquantity1.grid(row=8,column=3)

    laberror1 = Label(updwin, text = "*Please fill all details", fg = 'red')
    laberror1.grid(row=9,column=1,columnspan=3)
    laberror1.grid_remove()

    subbut = Button(updwin, text = "Submit", command = updateformcheck )
    subbut.grid(row=10,column=1, columnspan = 3,pady=20)

def deleteform(buttons):

    def deleteformcheck():
        bool = TRUE
        while bool:
            bool,mydb,mycursor = checkinternet(TRUE)

        try:
            int(entid.get())
        except:
            laberror.config(text = "*Please enter a valid ID")
            laberror.grid()
            return TRUE

        flag = 0
        if entid.get() == "" and entname.get() == "":
            laberror.config(text = "*Please fill either of the details")
            laberror.grid()

        elif entid.get() != "":
            sql = "SELECT * FROM Products WHERE id = %s"
            val = (entid.get())
            mycursor.execute(sql % val)
            myresult = mycursor.fetchall()

            if len(myresult) == 0:
                laberror.config(text = "*No Entry with the ID entered. Please enter valid ID")
                laberror.grid()

            else:
                flag = 1
                sql = "DELETE FROM Products WHERE id = %s"
                val = (entid.get())
                mycursor.execute(sql % val)
                laberror.grid_remove()
                mydb.commit()
                checkentries(mydb,mycursor,buttons)
                mycursor.close()
                mydb.close()
                delwin.grab_release()
                delwin.destroy()

        elif flag == 0 and entname.get() != "":
            sql = "SELECT * FROM Products WHERE Name = '%s'"
            val = entname.get()
            mycursor.execute(sql % val)
            myresult = mycursor.fetchall()

            if len(myresult) == 0:
                laberror.config(text = "*No Record with the Name entered. Please enter valid Name")
                laberror.grid()

            elif len(myresult) >= 2:
                laberror.config(text = "*Multiple Records with the Name Entered. Please enter the ID instead.")
                laberror.grid()

            else:
                flag = 1
                sql = "DELETE FROM Products WHERE Name = '%s'"
                val = (entname.get())
                mycursor.execute(sql % val)
                laberror.grid_remove()
                mydb.commit()
                checkentries(mydb,mycursor,buttons)
                mycursor.close()
                mydb.close()
                delwin.grab_release()
                delwin.destroy()


    delwin = Toplevel(root)
    delwin.grab_set()

    labtop = Label(delwin, text = "Enter either ID or Name of the record to be Deleted: ")
    labtop.grid(row=0,column=1,columnspan=3)

    labid = Label(delwin, text = "ID: ")
    labid.grid(row=1,column=1,pady=20,sticky=W)

    labname = Label(delwin, text = "Name: ")
    labname.grid(row=2,column=1,pady=20,sticky=W)

    entid = Entry(delwin)
    entid.grid(row=1,column=3)

    entname = Entry(delwin)
    entname.grid(row=2,column=3)

    laberror = Label(delwin, text = "*Please fill either of the details", fg = 'red')
    laberror.grid(row=3,column=1,columnspan=3,pady=20)
    laberror.grid_remove()

    subbut = Button(delwin, text = "Submit", command = deleteformcheck )
    subbut.grid(row=4,column=1, columnspan = 3,pady=20)

def displayres():
    bool = TRUE
    while bool:
        bool,mydb,mycursor = checkinternet(TRUE)

    diswin = Toplevel(root)
    diswin.grab_set()

    labtop = Label(diswin, text = "The records are: ")
    labtop.grid(row=1,column=1,columnspan=4,sticky=W)

    labid = Label(diswin, text = "ID")
    labid.grid(row=2,column=1,padx=10)

    labname = Label(diswin, text = "Name")
    labname.grid(row=2,column=2,padx=10)

    labprice = Label(diswin, text = "Price")
    labprice.grid(row=2,column=3,padx=10)

    labquantity = Label(diswin, text = "Quantity")
    labquantity.grid(row=2,column=4,padx=10)

    mycursor.execute("SELECT * FROM Products")
    myresult = mycursor.fetchall()
    results = Listbox(diswin)
    i = 0
    var = IntVar()
    l = []
    for x in myresult:
        i = i + 1
        if i>2:
            b = Button(diswin, text = "Next Page", command = lambda: var.set(1))
            b.grid(row=3+i,column=1, columnspan=4)
            b.wait_variable(var)
            b.destroy()
            for s in l:
                s.destroy()
            i = 1

        tmp = Label(diswin, text=str(x[0]))
        tmp.grid(row=2+i,column=1)
        l.append(tmp)
        tmp = Label(diswin, text=str(x[1]))
        tmp.grid(row=2+i,column=2)
        l.append(tmp)
        tmp = Label(diswin, text=str(x[2]))
        tmp.grid(row=2+i,column=3)
        l.append(tmp)
        tmp = Label(diswin, text=str(x[3]))
        tmp.grid(row=2+i,column=4)
        l.append(tmp)

def checkadmintable(mydb, mycursor):
    #Check for Table
    mycursor.execute("SHOW TABLES")
    flag = FALSE
    for x in mycursor:
        for i in x:
            if i == 'Admins':
                flag = TRUE
                break

    #Create table if it does not exist
    if flag == FALSE:
        mycursor.execute("CREATE TABLE Admins (username varchar(255) PRIMARY KEY, password VARCHAR(255) NOT NULL)")
        sql = "INSERT INTO Admins (username, password) VALUES (%s, %s)"
        val = ("root","root")
        mycursor.execute(sql, val)
        mydb.commit()
    pass

def employeepage():
    #user Window
    user = Toplevel(root)
    user.grab_set()
    user.title("Employee User")
    user.geometry("300x300")

    ins = Button(user, text = "Insert Record", command = lambda: insertform(buttons))  #used lambda since a function cannot be passed values in command so created a new function
    ins.pack(fill = BOTH, expand = TRUE)

    upd = Button()

    dele = Button()

    disp = Button(user, text = "Display Records", command = displayres)
    disp.pack(fill = BOTH, expand = TRUE)

    buttons = [ins,upd,dele,disp]
    checkdb()

    #connecting
    bool = TRUE
    while bool:
        bool,mydb,mycursor = checkinternet(TRUE)

    checktable(mydb, mycursor)
    checkentries(mydb, mycursor,buttons)
    mycursor.close()
    mydb.close()

def adminpage():
    #Admin Window
    admin = Toplevel(root)
    admin.grab_set()
    admin.title("Admin Page")
    admin.geometry("300x300")

    ins = Button(admin, text = "Insert Record", command = lambda: insertform(buttons))  #used lambda since a function cannot be passed values in command so created a new function
    ins.pack(fill = BOTH, expand = TRUE)

    upd = Button(admin, text = "Update Record", command = updateform)
    upd.pack(fill = BOTH, expand = TRUE)

    dele = Button(admin, text = "Delete Record", command = lambda: deleteform(buttons))
    dele.pack(fill = BOTH, expand = TRUE)

    disp = Button(admin, text = "Display Records", command = displayres)
    disp.pack(fill = BOTH, expand = TRUE)

    buttons = [ins,upd,dele,disp]
    checkdb()

    #connecting
    bool = TRUE
    while bool:
        bool,mydb,mycursor = checkinternet(TRUE)

    checktable(mydb, mycursor)
    checkentries(mydb, mycursor,buttons)
    mycursor.close()
    mydb.close()

def adminlogin():

    def admincheck():
        bool = TRUE
        while bool:
            bool,mydb,mycursor = checkinternet(TRUE)

        if username.get() == "" or password.get() == "":
            laberror.grid()

        else:
            checkadmintable(mydb,mycursor)
            sql = "SELECT * FROM Admins WHERE username = '%s'"
            val = (username.get())
            mycursor.execute(sql % val)
            myresult = mycursor.fetchall()

            if len(myresult) == 0:
                laberror.config(text = "No Account with the Username entered.")
                laberror.grid()

            else:
                sql = "SELECT * FROM Admins WHERE username = '%s' AND password = '%s'"
                val = (username.get(),password.get())
                mycursor.execute(sql % val)
                myresult = mycursor.fetchall()
                if len(myresult) == 0:
                    laberror.config(text = "Incorrect Password.")
                    laberror.grid()

                else:
                    admin.grab_release()
                    admin.destroy()
                    mycursor.close()
                    mydb.cursor()
                    adminpage()

    admin = Toplevel(root)
    admin.grab_set()
    admin.title("Login")

    labtop = Label(admin, text = "Administrator Login")
    labtop.grid(row = 1, column = 1, columnspan = 3)

    usernamelab = Label(admin, text = "Username: ")
    usernamelab.grid(row = 2, column = 1, pady = 20, sticky = W)

    passwordlab = Label(admin, text = "Password: ")
    passwordlab.grid(row = 3, column = 1, pady = 20, sticky = W)

    username = Entry(admin)
    username.grid(row = 2, column = 2)

    password = Entry(admin, show = "*")
    password.grid(row = 3, column = 2)

    laberror = Label(admin, text = "*Please fill all details", fg = 'red')
    laberror.grid(row=4,column=1,columnspan=3)
    laberror.grid_remove()

    subbut = Button(admin, text = "Submit", command = admincheck)
    subbut.grid(row = 5, column = 1, columnspan = 3)

    checkdb()

def checkinternet(db=TRUE):
    if db:
        try:
            mydb = mysql.connector.connect(
            host="sql12.freemysqlhosting.net",
            user="sql12330813",
            password="Y9n5gpupbd",
            database="sql12330813"
            )
            mycursor = mydb.cursor()
            return FALSE,mydb,mycursor

        except:
            bool1 = messagebox.askretrycancel("Disconnected", "Check Internet Connection and Try Agian or Cancel to quit.")
            if not bool1:
                sys.exit()
                return FALSE,FALSE,FALSE
            else:
                return TRUE,FALSE,FALSE

    else:
        try:
            mydb = mysql.connector.connect(
            host="sql12.freemysqlhosting.net",
            user="sql12330813",
            password="Y9n5gpupbd"
            )
            mycursor = mydb.cursor()
            return FALSE,mydb,mycursor

        except:
            bool1 = messagebox.askretrycancel("Disconnected", "Check Internet Connection and Try Agian or Cancel to quit.")
            if not bool1:
                sys.exit()
                return FALSE,FALSE,FALSE
            else:
                return TRUE,FALSE,FALSE

if __name__ == "__main__":

    root = Tk()
    root.title("Open Ended")
    root.geometry("300x300")

    adm = Button(root, text = "Administrator", command = adminlogin)
    adm.pack(fill = BOTH, expand = TRUE)

    employee = Button(root, text = "Employee", command = employeepage)
    employee.pack(fill = BOTH, expand = TRUE)

    bool = TRUE
    while bool:
        bool,_,_ = checkinternet(FALSE)

    root.mainloop()

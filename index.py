from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

root = Tk()
root.title("Contact List")
width = 700
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#C70039")
#============================VARIABLES===================================
FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
CONTACT = StringVar()
#============================METHODS=====================================
def validate(Window):
	if len(FIRSTNAME.get())==0:
		tkMessageBox.showwarning("attention","Enter First Name",parent=Window)
		return False
	if FIRSTNAME.get().isalpha()==False:
		tkMessageBox.showwarning("attention","Invalid name",parent=Window)
		return False
	if len(LASTNAME.get())==0:
		tkMessageBox.showwarning("attention","Enter Last Name",parent=Window)
		return False
	if LASTNAME.get().isalpha()==False:
		tkMessageBox.showwarning("attention","Invalid last name",parent=Window)
		return False
	if GENDER.get()=="0":
		tkMessageBox.showwarning("attention","select gender",parent=Window)
		return False
	if len(AGE.get())==0:
		tkMessageBox.showwarning("attention","Enter Age",parent=Window)
		return False
	if AGE.get().lstrip("-").isdigit()==False:
		tkMessageBox.showwarning("attention","Invalid age",parent=Window)
		return False
	if(int(AGE.get()) < 0):
		tkMessageBox.showwarning("attention","Invalid age must be > 0",parent=Window)
		return False

	if len(ADDRESS.get())==0:
		tkMessageBox.showwarning("attention","Address",parent=Window)
		return False
	if len(CONTACT.get())==0:
		tkMessageBox.showwarning("attention","Enter Contact",parent=Window)
		return False
	if CONTACT.get().isdigit()==False:
		tkMessageBox.showwarning("attention","Contact number must be digits",parent=Window)
		return False
	if len(CONTACT.get())!=10:
		tkMessageBox.showwarning("attention","invalid contact number length",parent=Window)
		return False
	else:
		return True

def setNull():
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set(0)
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")
def Database():
    conn = sqlite3.connect("pythontut.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, gender TEXT, age TEXT, address TEXT, contact TEXT)")
    cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def SubmitData():
    if  validate(NewWindow):
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("pythontut.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `member` (firstname, lastname, gender, age, address, contact) VALUES(?, ?, ?, ?, ?, ?)", (str(FIRSTNAME.get().capitalize()), str(LASTNAME.get().capitalize()), str(GENDER.get()), int(AGE.get()), str(ADDRESS.get().title()), str(CONTACT.get())))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        tkMessageBox.showinfo("Success","Record Inserted",parent=NewWindow)
        setNull()

def UpdateData():
    if validate(UpdateWindow):
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("pythontut.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE `member` SET `firstname` = ?, `lastname` = ?, `gender` =?, `age` = ?,  `address` = ?, `contact` = ? WHERE `mem_id` = ?", (str(FIRSTNAME.get().capitalize()), str(LASTNAME.get().capitalize()), str(GENDER.get()), int(AGE.get()), str(ADDRESS.get().title()), str(CONTACT.get()), int(mem_id)))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        tkMessageBox.showinfo("Success","Record Updated",parent=UpdateWindow)
        UpdateWindow.destroy()
        setNull()
    
def OnSelected(event):
    #if tree.identify("column",event.x,event.y) == "#4":
    #   print("4")
    if not tree.selection():
       tkMessageBox.showwarning('Attention', 'Please Select Something First!')
       return
    else:
       global mem_id, UpdateWindow
       if 'UpdateWindow' in globals():
          UpdateWindow.destroy()
       curItem = tree.focus()
       contents =(tree.item(curItem))
       selecteditem = contents['values']
       mem_id = selecteditem[0]
       setNull()
       FIRSTNAME.set(selecteditem[1])
       LASTNAME.set(selecteditem[2])
       GENDER.set(selecteditem[3])
       AGE.set(selecteditem[4])
       ADDRESS.set(selecteditem[5])
       CONTACT.set(selecteditem[6])
       UpdateWindow = Toplevel(root)
       UpdateWindow.title("Contact List")
       width = 400
       height = 300
       screen_width = root.winfo_screenwidth()
       screen_height = root.winfo_screenheight()
       x = ((screen_width/2) + 450) - (width/2)
       y = ((screen_height/2) + 20) - (height/2)
       UpdateWindow.resizable(0, 0)
       UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
       if 'NewWindow' in globals():
          NewWindow.destroy()
    #===================FRAMES==============================
    FormTitle = Frame(UpdateWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(UpdateWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male",  font=('arial', 14)).pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female",  font=('arial', 14)).pack(side=LEFT)
    #===================LABELS==============================
    lbl_title = Label(FormTitle, text="Updating Contacts", font=('arial', 16), bg="orange",  width = 300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(ContactForm, text="Firstname", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(ContactForm, text="Lastname", font=('arial', 14), bd=5)
    lbl_lastname.grid(row=1, sticky=W)
    lbl_gender = Label(ContactForm, text="Gender", font=('arial', 14), bd=5)
    lbl_gender.grid(row=2, sticky=W)
    lbl_age = Label(ContactForm, text="Age", font=('arial', 14), bd=5)
    lbl_age.grid(row=3, sticky=W)
    lbl_address = Label(ContactForm, text="Address", font=('arial', 14), bd=5)
    lbl_address.grid(row=4, sticky=W)
    lbl_contact = Label(ContactForm, text="Contact", font=('arial', 14), bd=5)
    lbl_contact.grid(row=5, sticky=W)
    #===================ENTRY===============================
    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14))
    lastname.grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    age = Entry(ContactForm, textvariable=AGE,  font=('arial', 14))
    age.grid(row=3, column=1)
    address = Entry(ContactForm, textvariable=ADDRESS,  font=('arial', 14))
    address.grid(row=4, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT,  font=('arial', 14))
    contact.grid(row=5, column=1)
    #==================BUTTONS==============================
    btn_updatecon = Button(ContactForm, text="Update", width=50, command=UpdateData)
    btn_updatecon.grid(row=6, columnspan=2, pady=10)

def DeleteData():
    if not tree.selection():
       tkMessageBox.showwarning('Attention', 'Please Select Something First!')
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("pythontut.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
    
def AddNewWindow():
    global NewWindow
    if 'NewWindow' in globals():
        NewWindow.destroy()
    setNull()
    NewWindow = Toplevel(root)
    NewWindow.title("Contact List")
    width = 400
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = ((screen_width/2) - 455) - (width/2)
    y = ((screen_height/2) + 20) - (height/2)
    NewWindow.resizable(0, 0)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()
    #===================FRAMES==============================
    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Male = Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male",  font=('arial', 14)).pack(side=LEFT)
    Female = Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female",  font=('arial', 14)).pack(side=LEFT)
    #===================LABELS==============================
    lbl_title = Label(FormTitle, text="Adding New Contacts", font=('arial', 16), bg="#66ff66",  width = 300)
    lbl_title.pack(fill=X)
    lbl_firstname = Label(ContactForm, text="Firstname", font=('arial', 14), bd=5)
    lbl_firstname.grid(row=0, sticky=W)
    lbl_lastname = Label(ContactForm, text="Lastname", font=('arial', 14), bd=5)
    lbl_lastname.grid(row=1, sticky=W)
    lbl_gender = Label(ContactForm, text="Gender", font=('arial', 14), bd=5)
    lbl_gender.grid(row=2, sticky=W)
    lbl_age = Label(ContactForm, text="Age", font=('arial', 14), bd=5)
    lbl_age.grid(row=3, sticky=W)
    lbl_address = Label(ContactForm, text="Address", font=('arial', 14), bd=5)
    lbl_address.grid(row=4, sticky=W)
    lbl_contact = Label(ContactForm, text="Contact", font=('arial', 14), bd=5)
    lbl_contact.grid(row=5, sticky=W)
    #===================ENTRY===============================
    firstname = Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14))
    firstname.grid(row=0, column=1)
    lastname = Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14))
    lastname.grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    age = Entry(ContactForm, textvariable=AGE,  font=('arial', 14))
    age.grid(row=3, column=1)
    address = Entry(ContactForm, textvariable=ADDRESS,  font=('arial', 14))
    address.grid(row=4, column=1)
    contact = Entry(ContactForm, textvariable=CONTACT,  font=('arial', 14))
    contact.grid(row=5, column=1)
    #==================BUTTONS==============================
    btn_addcon = Button(ContactForm, text="Save", width=50, command=SubmitData)
    btn_addcon.grid(row=6, columnspan=2, pady=10)


#============================FRAMES======================================
Top = Frame(root, width=500, bd=1,bg="#17202A")
Top.pack(side=TOP)
Mid = Frame(root, width=500,  bg="#C70039")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidLeftPadding = Frame(Mid, width=370, bg="#C70039")
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)
#============================LABELS======================================
lbl_title = Label(Top, text="Contact Management System", font=('arial', 16), width=500,bg="#ffffff")
lbl_title.pack(fill=X)

#============================ENTRY=======================================

#============================BUTTONS=====================================
btn_add = Button(MidLeft, text="+ ADD NEW", bg="#66ff66", command=AddNewWindow)
btn_add.pack()
btn_delete = Button(MidRight, text="DELETE", bg="#FFFF00", command=DeleteData)
btn_delete.pack(side=RIGHT)

#============================TABLES======================================
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("MemberID", "Firstname", "Lastname", "Gender", "Age", "Address", "Contact"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('Firstname', text="Firstname", anchor=W)
tree.heading('Lastname', text="Lastname", anchor=W)
tree.heading('Gender', text="Gender", anchor=W)
tree.heading('Age', text="Age", anchor=W)
tree.heading('Address', text="Address", anchor=W)
tree.heading('Contact', text="Contact", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=90)
tree.column('#5', stretch=NO, minwidth=0, width=80)
tree.column('#6', stretch=NO, minwidth=0, width=120)
tree.column('#7', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)
#============================INITIALIZATION==============================
if __name__ == '__main__':
    Database()
    root.mainloop()
    

from ctypes import alignment
from tkinter import *
import pyrebase as pybase
from tkinter import messagebox, ttk

# API Provided By Firebase Itself
firebaseConfig = {
    "apiKey": "AIzaSyBGs7cq211Kin3iE73vpP3fYp51IjfKjaw",
    "authDomain": "student-management-syste-1836f.firebaseapp.com",
    "projectId": "student-management-syste-1836f",
    "storageBucket": "student-management-syste-1836f.appspot.com",
    "messagingSenderId": "288592150624",
    "appId": "1:288592150624:web:d120a6406d3a54d3504305",
    "databaseURL": "https://student-management-syste-1836f-default-rtdb.firebaseio.com/",
}

# Firebase Connection
firebase = pybase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

# Colors
BKGD = "#13a5b6"
WHITE = "#FFFFFF"
BLACK = "#000000"

# Font Styles
TEXT_INPUT_FONT_STYLE = ("Arial", 13)
SUB_TITLE_FONT_STYLE = ("Arial", 10, "bold")


class Main:
    def __init__(self, root):
        self.root = root
        self.root.resizable(0, 0)
        self.root.geometry("1250x600")
        self.root.title("Student Data Management System")

        # Variables
        self.id = StringVar()
        self.name = StringVar()
        self.email = StringVar()
        self.semester = StringVar()
        self.department = StringVar()

        # Frame 1
        Frame_1 = Frame(self.root, bd=5, relief=GROOVE, bg=BKGD, pady=5)
        Frame_1.place(x=0, y=0, width=1250, height=190)

        # Frame 2
        Frame_2 = Frame(self.root, bd=5, relief=RIDGE, bg=BKGD)
        Frame_2.place(x=0, y=190, width=1250, height=410)

        # ID
        lbl_id = Label(Frame_1, bg=BKGD, fg=WHITE, text="ID", font=SUB_TITLE_FONT_STYLE)
        lbl_id.grid(row=0, column=2, pady=10, padx=15, sticky="w")
        txt_id = Entry(Frame_1,width=23,textvariable=self.id,font=TEXT_INPUT_FONT_STYLE,)
        txt_id.grid(row=1, column=2, pady=10, padx=15, sticky="w")

        # Name
        lbl_name = Label(Frame_1, text="Name", font=SUB_TITLE_FONT_STYLE, bg=BKGD, fg=WHITE)
        lbl_name.grid(row=0, column=3, pady=10, padx=15, sticky="w")
        txt_name = Entry(Frame_1,width=23,textvariable=self.name,font=TEXT_INPUT_FONT_STYLE,)
        txt_name.grid(row=1, column=3, pady=10, padx=15, sticky="w")

        # Email
        lbl_mail = Label(Frame_1, text="E-mail", font=SUB_TITLE_FONT_STYLE, bg=BKGD, fg=WHITE)
        lbl_mail.grid(row=0, column=1, pady=10, padx=15, sticky="w")
        txt_mail = Entry(Frame_1,width=23,textvariable=self.email,font=TEXT_INPUT_FONT_STYLE)
        txt_mail.grid(row=1, column=1, pady=10, padx=15, sticky="w")

        # Semester
        lbl_sem = Label(Frame_1, text="Semester", font=SUB_TITLE_FONT_STYLE, bg=BKGD, fg=WHITE)
        lbl_sem.grid(row=0, column=4, pady=10, padx=15, sticky="w")
        txt_sem = Entry(Frame_1,width=23,textvariable=self.semester,font=TEXT_INPUT_FONT_STYLE)
        txt_sem.grid(row=1, column=4, pady=10, padx=15, sticky="w")

        # Department
        lbl_dept = Label(Frame_1, text="Department", font=SUB_TITLE_FONT_STYLE, bg=BKGD, fg=WHITE)
        lbl_dept.grid(row=0, column=0, pady=10, padx=15, sticky="w")
        txt_dept = Entry(Frame_1,width=23,textvariable=self.department,font=TEXT_INPUT_FONT_STYLE)
        txt_dept.grid(row=1, column=0, pady=10, padx=15, sticky="w")

        # Button Frame
        Frame_Btn = Frame(Frame_1, bg=BKGD, pady=10, padx=10)
        Frame_Btn.grid(row=3, columnspan=5)

        # Add Button
        add_btn = Button(Frame_Btn, command=self.add_students, text="Add", padx=146, pady=6)
        add_btn.grid(row=0, column=1, pady=20, padx=2)

        # Delete Button
        del_btn = Button(Frame_Btn, command=self.delete_data, text="Delete", padx=124, pady=6)
        del_btn.grid(row=0, column=2, pady=20, padx=2)

        # Clear Button
        clr_btn = Button(Frame_Btn, command=self.clear, text="Clear", padx=130, pady=6)
        clr_btn.grid(row=0, column=3, pady=20, padx=2)

        # Exit Button
        exit_btn = Button(Frame_Btn, command=self.root.destroy, text="Quit", padx=130, pady=6)
        exit_btn.grid(row=0, column=4, pady=20, padx=2)

        # Data Table Frame
        Table_Frame = Frame(Frame_2, bg=BKGD, padx=10, pady=10)
        Table_Frame.place(x=0, y=0, width=1240, height=400)

        # Scroll Bar
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)

        # Data Table
        self.Student_Table = ttk.Treeview(
            Table_Frame,
            columns=("department", "email", "id", "name", "semester"),
            yscrollcommand=scroll_y.set,
        )
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.configure(command=self.Student_Table.yview)

        # Column Names
        self.Student_Table.heading("id", text="ID")
        self.Student_Table.heading("name", text="Name")
        self.Student_Table.heading("email", text="E-mail")
        self.Student_Table.heading("semester", text="Semester")
        self.Student_Table.heading("department", text="Department")

        # To Remove Indexing Column from Table
        self.Student_Table["show"] = "headings"

        # Table Location
        self.Student_Table.pack(fill="both", expand=1, alignment=CENTER)

        # Binding the Button
        self.Student_Table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    def add_students(self):
        if (self.id.get() == ""):
            messagebox.showerror("Error", "All feilds are required!")
        else:
            collected_data = {
                "Id": self.id.get(),
                "Name": self.name.get(),
                "Email": self.email.get(),
                "Semester": self.semester.get(),
                "Department": self.department.get(),
            }
            db.push(collected_data)
            messagebox.showinfo("Success", "Data Inserted")

            self.clear()
            self.clear_all()
            self.fetch_data()

    def clear_all(self) :
        for item in self.Student_Table.get_children():
            self.Student_Table.delete(item)

    def clear(self):
        self.id.set("")
        self.name.set("")
        self.email.set("")
        self.semester.set("")
        self.department.set("")

    def fetch_data(self):
        student = db.get()
        if(student.val() == None):
            pass
        else:
            for i in student.each():
                x = i.val()
                one, two, three, four, five = "", "", "", "", ""
                one1, two1, three1, four1, five1 = False, False, False, False, False
                for j in x.values():
                    if (one1 == False):
                        one = j
                        one1 = True
                    elif (two1 == False):
                        two = j
                        two1 = True
                    elif (three1 == False):
                        three = j
                        three1 = True
                    elif (four1 == False):
                        four = j
                        four1 = True
                    elif (five1 == False):
                        five = j
                        five1 = True

                self.Student_Table.insert("", "end", text="1", values=(one, two, three, four, five))

    def get_cursor(self, event):
        cursor_row = self.Student_Table.focus()
        contents = self.Student_Table.item(cursor_row)
        row = contents["values"]
        self.department.set(row[0])
        self.email.set(row[1])
        self.id.set(row[2])
        self.name.set(row[3])
        self.semester.set(row[4])

    def delete_data(self):
        cursor_row = self.Student_Table.focus()
        contents = self.Student_Table.item(cursor_row)
        dict = {'text':'','image':'','values':'','open':0,'tags':''}
        if(contents == dict):
            messagebox.showinfo("Error", "Select the data row to delete")
            return

        data_1 = contents.get("values")
        string__values = [str(i) for i in list(data_1)]
        tag = db.child().get().val()
        for k, v in tag.items():
            res = [str(i) for i in list(v.values())]
            if(string__values == res):
                db.child(k).remove()
                messagebox.showinfo("Success", "Data Deleted")
                break

        self.clear()
        self.clear_all()
        self.fetch_data()

if __name__ == "__main__":
    root = Tk()
    obj = Main(root)
    root.mainloop()

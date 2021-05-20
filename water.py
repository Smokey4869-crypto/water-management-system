from tkinter import *
from db import Database
from PIL import ImageTk, Image
from customers import CustomerWin
from employee import EmployeeWindow
from admin import AdminWindow

database = Database("water.db")


class Login:
    def __init__(self, root):
        self.login = root
        self.login.title('Login')
        self.login.geometry("975x650")
        self.login.resizable(False, False)

        def btn_login():
            result = database.login(en_username.get(), en_password.get())
            if result is not None:
                self.login.destroy()
                if result[0] == "emp1":
                    AdminWindow(result[0])
                elif result[0][0] == "e":
                    EmployeeWindow(result[0])
                else:
                    CustomerWin(int(result[0]))

        image = ImageTk.PhotoImage(Image.open("images//Login.png").resize((975, 650), Image.ANTIALIAS))
        canvas = Canvas(self.login)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=image, anchor="nw")

        en_username = Entry(self.login, relief="flat", width=21, font=("Calibri", 13), bg="#E6E4EF")
        en_username.place(x=632, y=251)

        en_password = Entry(self.login, relief="flat", width=21, font=("Calibri", 13), bg="#E6E4EF", show="*")
        en_password.place(x=632, y=301)

        submit_btn = ImageTk.PhotoImage(Image.open("images//Submit_button.png").resize((300, 40), Image.ANTIALIAS))
        btn_login = Button(self.login, image=submit_btn, relief="flat", bg="white", activebackground="white",
                           command=btn_login)
        btn_login.place(x=543, y=350)

        self.login.mainloop()


if __name__ == '__main__':
    win = Tk()
    Login = Login(win)

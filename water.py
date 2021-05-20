from tkinter import *
from db import Database
from PIL import ImageTk, Image
from customers import CustomerWin
from employee import EmployeeWindow
from admin import AdminWindow
from tkinter import messagebox

database = Database("water_database.db")


def center_window(root, width, height):
    positionRight = int(root.winfo_screenwidth() / 2 - width / 2)
    positionDown = int(root.winfo_screenheight() / 2 - height / 2 - 60)

    root.geometry("%dx%d+%d+%d" % (width, height, positionRight, positionDown))


class Login:
    def __init__(self, root):
        self.login = root
        self.login.title('Login')
        center_window(self.login, 975, 650)
        # self.login.geometry("975x650")
        self.login.resizable(False, False)

        self.lb_username = Label()
        self.en_username = Entry()
        self.lb_password = Label()
        self.en_password = Entry()

        self.btn_login = Button()

        self.draw()

    def draw(self):
        image = ImageTk.PhotoImage(Image.open("images//Login.png").resize((975, 650), Image.ANTIALIAS))
        canvas = Canvas(self.login)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=image, anchor="nw")

        self.en_username = Entry(self.login, relief="flat", width=21, font=("Calibri", 13), bg="#E6E4EF")
        self.en_username.place(x=632, y=251)

        self.en_password = Entry(self.login, relief="flat", width=21, font=("Calibri", 13), bg="#E6E4EF", show="*")
        self.en_password.place(x=632, y=301)

        submit_btn = ImageTk.PhotoImage(Image.open("images//Submit_button.png").resize((300, 40), Image.ANTIALIAS))
        self.btn_login = Button(self.login, image=submit_btn, relief="flat", bg="white",
                                activebackground="white", command=self.fun_login)
        self.btn_login.place(x=543, y=350)

        self.login.mainloop()

    def fun_login(self):
        result = database.login(self.en_username.get(), self.en_password.get())
        if result is not None:
            self.login.destroy()
            if result[0] == "admin":
                AdminWindow(result[0])
            elif result[0][0] == "e":
                EmployeeWindow(result[0])
            else:
                CustomerWin(int(result[0]))
        else:
            messagebox.showwarning(title=None, message='Wrong Username or Password')


if __name__ == '__main__':
    win = Tk()
    Login = Login(win)

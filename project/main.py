import tkinter as tk
from tkinter import messagebox
from AI import SmallAI
ai_robot = SmallAI()
global messages_history
messages_history = []
# pipeline_ins = pipeline(task=Tasks.translation, model="./nlp_csanmt_translation_en2zh_base")
# 主界面
global name

class MainInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("MAIN")
        self.master.geometry("500x300")
        # self.login = tk.Tk()
        # self.withdraw = tk.Tk()

        # Login Button
        self.login_button = tk.Button(self.master, text="Login", command=self.show_login_interface)
        self.login_button.pack()

        # Register Button
        self.register_button = tk.Button(self.master, text="Register", command=self.show_register_interface)
        self.register_button.pack()

    def show_login_interface(self):
        login = tk.Tk()
        # clean main UI
        self.master.withdraw()
        # show login UI
        LoginInterface(login)

    def show_register_interface(self):
        withdraw = tk.Tk()
        # close main UI
        self.master.withdraw()
        # show Register UI
        RegisterInterface(withdraw)

# User Login UI
class LoginInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("User Login")
        self.master.geometry("500x300")

        tk.Label(self.master, text="Username:").pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        tk.Label(self.master, text="Password:").pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.master, text="Login", command=self.login)
        self.login_button.pack()

        self.back_button = tk.Button(self.master, text="Back", command=self.back_to_main)
        self.back_button.pack()

    def login(self):
        global name
        # LOGIN
        username = self.username_entry.get()
        password = self.password_entry.get()
        name = username
        with open("user_data.txt","r") as f:
            user_data = f.readlines()
        if (username + "," + password + "\n") in user_data:
            messagebox.showinfo("Success", "Welcome back!")
            self.show_user_operation_interface()
        else:
            messagebox.showerror("Fail", "Username or password error!")

    def back_to_main(self):
        main_interface = tk.Tk()
        # close login UI
        self.master.withdraw()
        # show main UI
        MainInterface(main_interface)

    def show_user_operation_interface(self):
        user_operation_interface = tk.Tk()
        # close mainUI
        self.master.withdraw()
        # show operate UI
        UserOperationInterface(user_operation_interface)

# user login ui
class RegisterInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("REGISTER")
        self.master.geometry("500x300")

        tk.Label(self.master, text="Username:").pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        tk.Label(self.master, text="Password:").pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.master, text="Register", command=self.login)
        self.login_button.pack()

        self.back_button = tk.Button(self.master, text="Back", command=self.back_to_main)
        self.back_button.pack()


    def back_to_main(self):
        main_interface = tk.Tk()
        # close login ui
        self.master.withdraw()
        # show main ui
        MainInterface(main_interface)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        with open("user_data.txt", "a") as f:
            f.write(str(username)+","+str(password)+"\n")
        messagebox.showinfo("Register success!", "Welcome!")

class UserOperationInterface:
    def __init__(self, master):
        self.master = master
        self.master.title("Conversation")
        self.master.geometry("500x400")

        self.chat_history = []  # 用于保存对话历史

        tk.Label(self.master, text="Conversation:").pack()
        self.chat_display = tk.Text(self.master, height=10, width=50)
        self.chat_display.pack()

        self.input_entry = tk.Entry(self.master, width=50)
        self.input_entry.pack()

        self.confirm_button = tk.Button(self.master, text="Send", command=self.confirm)
        self.confirm_button.pack()

        self.back_button = tk.Button(self.master, text="Back", command=self.back_to_main)
        self.back_button.pack()

    def confirm(self):
        global messages_history
        user_input = self.input_entry.get()
        if user_input:  # ensure user input a useful message
            self.add_to_chat_history("User: " + user_input + "\n_________________________________________")
            self.input_entry.delete(0, tk.END)  # clean entry
            answer_result, messages_history = ai_robot.answer(user_input, name, messages_history)
            self.respond_to_user(answer_result)  # AI answer

    def respond_to_user(self, user_input):
        ai_response = "AI: " + user_input + "\n_________________________________________"  # 这里可以替换为AI的实际回复
        self.add_to_chat_history(ai_response)

    def add_to_chat_history(self, message):
        self.chat_history.append(message)
        self.chat_display.insert(tk.END, message + "\n")  # add message to box

    def back_to_main(self):
        main_interface = tk.Tk()
        # close conversation UI
        self.master.withdraw()
        # show main ui
        MainInterface(main_interface)

# user operate ui
class UserOperationInterfaceTrans:
    def __init__(self, master):
        self.master = master
        self.master.title("Conversation")
        self.master.geometry("500x300")

        tk.Label(self.master, text="User:").pack()
        self.input_entry = tk.Entry(self.master)
        self.input_entry.pack()

        tk.Label(self.master, text="AI:").pack()
        self.output_label = tk.Label(self.master, text="")
        self.output_label.pack()

        self.confirm_button = tk.Button(self.master, text="Enter", command=self.confirm)
        self.confirm_button.pack()

        self.back_button = tk.Button(self.master, text="Back", command=self.back_to_main)
        self.back_button.pack()

    def confirm(self):
        input_text = self.input_entry.get()
        # outputs = pipeline_ins(input=input_text)
        # self.output_label.config(text=outputs['translation'])

    def back_to_main(self):
        main_interface = tk.Tk()
        # close register UI
        self.master.withdraw()
        # show main ui
        MainInterface(main_interface)
if __name__ == "__main__":
    # main UI
    root = tk.Tk()
    # an entity
    main_interface = MainInterface(root)
    # loop
    root.mainloop()
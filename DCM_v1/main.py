import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tm

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 8)
VERSION = 0.01

# not too many comments, but will be changing this
# TODO: move from using pack to grid for better page layout

def popupmsg(msg):
    def exit_popup():
        popup.destroy()

    popup = tk.Tk()
    #popup.minsize(300,80)
    popup.wm_title("Notice")
    label = ttk.Label(popup, text = msg, font=NORM_FONT)
    label.pack(side="top", expand=True, pady=10)
    B1 = ttk.Button(popup, text="Done", command=exit_popup)
    B1.pack()
    popup.mainloop()


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Heart DCM")
        tk.Tk.resizable(self, width=True, height=True)
        self.debug_status = False

        container = tk.Frame(self)
        container.grid(row=0, column =0, sticky='NSEW')
        container.grid_columnconfigure(0,weight=1)
        container.grid_rowconfigure(0,weight=1)

        self.create_menu(container)

        self.frames = {}

        for F in {LoginPage, PageExampleOne, PageExampleTwo}:
        
            frame = F(parent = container, controller = self)
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky="NSEW")

        self.show_frame(LoginPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def create_menu(self, container):
        menubar = tk.Menu(container)

        help_menu = tk.Menu(menubar, tearoff = 0)
        help_menu.add_command(label="Documentation", command = lambda: popupmsg('Not Supported Yet!'))

        user_menu = tk.Menu(menubar, tearoff = 0)
        user_menu.add_command(label="Add User", command = lambda: popupmsg('Not Supported Yet!'))
        user_menu.add_command(label="Edit User", command = lambda: popupmsg('Not Supported Yet!'))
        user_menu.add_command(label="Delete User", command = lambda: popupmsg('Not Supported Yet!'))

        version_menu = tk.Menu(menubar, tearoff=0)
        version_menu.add_command(label="Version: {}".format(VERSION))
        version_menu.entryconfigure(0, state = tk.DISABLED)

        debug_menu = tk.Menu(menubar, tearoff= 0)
        debug_menu.add_command(label="Debug: {}".format(self.debug_status), command = lambda: self.toggle_debug(debug_menu))

        menubar.add_cascade(label="Help", menu=help_menu)
        menubar.add_cascade(label="Users", menu=user_menu)
        menubar.add_cascade(label="Debugging", menu=debug_menu)
        menubar.add_cascade(label="Version", menu=version_menu)
        tk.Tk.config(self, menu=menubar)


    def toggle_debug(self, menu):
        #commands for debugging
        self.debug_status = not self.debug_status
        menu.entryconfigure(0, label="Debug: {}".format(self.debug_status))

    def quit_program(self):
        self.destroy()



class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, master = parent)
        self.grid_columnconfigure((0,3),weight=2)
        self.grid_columnconfigure((1,2),weight=1)
        

        page_title = tk.Label(self, text="Login Page", font=LARGE_FONT, bg="green")
        page_title.grid(row=0, column=1, ipadx=100, ipady=50, columnspan=2) #(side="top", pady=10, padx=10)

        login_label = tk.Label(self, text="Username: ", font=NORM_FONT, bg="green")
        login_label.grid(row=1, column=1)# pack()

        username_entry = ttk.Entry(self)
        username_entry.grid(row=1, column=2 ) #pack()

        password_label = tk.Label(self, text="Password: ", font=NORM_FONT, bg="green")
        password_label.grid(row=2, column=1)#pack()

        password_entry = ttk.Entry(self, show="*")
        password_entry.grid(row=2, column=2)#pack()

        login_button = ttk.Button(self, text="Login", command= lambda: 
        controller.show_frame(PageExampleOne) if 
        self.authenticate(username_entry.get(), password_entry.get()) else False) 
                                                    
        login_button.grid(row=3, column=0)#pack() 
        print(self.grid_size())
    
    def authenticate(self, username, password):
        # do some stuff
        if username and password:
            return True #connect with backend
        else: 
            tm.showerror(message="Invalid Username or Password")

class PageExampleOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #self.grid(row =0, column = 0, sticky="nsew")
        self.columnconfigure((1,4), weight=1)
        self.rowconfigure((0,1),weight=1)

        garbage = {"A":1, "B": 2, "C": "Banana"}
        
        label = tk.Label(self, text = 'Page Example One', font=LARGE_FONT)
        label.grid(row=0, column=0)#pack(side="top", padx=10,pady=10)

        x = 1
        for key in garbage:
            dcm_data_label = tk.Label(self, text = '{} :'.format(key), font=NORM_FONT)
            dcm_value_label = tk.Label(self, text = '{}'.format(garbage[key]), font=NORM_FONT)
            dcm_data_label.grid(row=x, column=0, sticky="nsew")
            dcm_value_label.grid(row=x, column=1,sticky="nsew")
            x += 1

        button1 = ttk.Button(self, text="Back to Login", command= lambda: controller.show_frame(LoginPage))
        button1.grid(row=x+1, column = 2)#pack()

class PageExampleTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = 'Page Example Two', font=LARGE_FONT)
        label.grid(row=0)#pack(padx=10,pady=10)
        button1 = ttk.Button(self, text="Back to Login", command= lambda: controller.show_frame(LoginPage))
        button1.grid(row=0)#pack()



def main():
    app = Application()

    window_width = 1280
    window_height  = 720

    location_x = int((app.winfo_screenwidth()/2) - (window_width/2))
    location_y = int((app.winfo_screenheight()/2) - (window_height/2))
    app.geometry("{}x{}+{}+{}".format(
        window_width,
        window_height,
        location_x,
        location_y
    ))
    app.mainloop()





if __name__ == "__main__":
    main()
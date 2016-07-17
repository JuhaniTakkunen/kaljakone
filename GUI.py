# -*- coding: utf-8 -*-
try:
    import tkinter as tk
    import tkinter
except ImportError:
    import Tkinter as tk
    import Tkinter as tkinter
import google_api
import platform
import os
import logging
logging.basicConfig()

ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()

class PageIdentify(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        frame = tkinter.Frame(self, borderwidth=5, padx=10, pady=20, bg='blue')
        frame.pack(fill=tkinter.BOTH, expand=1)

        # Load icons
        Page.img_user1 = tkinter.PhotoImage(file=os.path.join(ROOT_DIRECTORY, "images/avatars/junnu.gif"))
        Page.img_user2 = tkinter.PhotoImage(file=os.path.join(ROOT_DIRECTORY, "images/avatars/opa.gif"))
        Page.img_user3 = tkinter.PhotoImage(file=os.path.join(ROOT_DIRECTORY, "images/avatars/random_girl.gif"))

        # Create buttons
        button1 = tkinter.Button(frame, height=90, width=90, padx=5, pady=5, image=Page.img_user1, command=lambda: self.identify("Junnu"))
        button2 = tkinter.Button(frame, height=90, width=90, padx=5, pady=5, image=Page.img_user2, command=lambda: self.identify("Opa"))
        button3 = tkinter.Button(frame, height=90, width=90, padx=5, pady=5, image=Page.img_user3, command=lambda: self.identify("Random Girl"))

        # Add buttons to frame
        button1.pack(side=tkinter.LEFT)
        button2.pack(side=tkinter.LEFT)
        button3.pack(side=tkinter.LEFT)
        self.update()

    def identify(self, userID):
        self.master.Order.userID = userID
        self.master.p1.show()   # TODO: is master ok to use?
        self.update()

class PageProduct(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        frame = tkinter.Frame(self, borderwidth=5, padx=10, pady=20, bg='red')
        frame.pack(fill=tkinter.BOTH, expand=1)

        # Load icons
        Page.beer = beer = tkinter.PhotoImage(file=os.path.join(ROOT_DIRECTORY, "images/beer.gif"))
        Page.cider = cider = tkinter.PhotoImage(file=os.path.join(ROOT_DIRECTORY, "images/cider.gif"))
        Page.settings = settings = tkinter.PhotoImage(file=os.path.join(ROOT_DIRECTORY, "images/settings.gif"))

        # Create buttons
        button1 = tkinter.Button(frame, height=90, width=90, padx=5, pady=5, image=beer, command=lambda: self.order("kalja"))
        button2 = tkinter.Button(frame, height=90, width=90, padx=5, pady=5, image=cider, command=lambda: self.order("siideri"))
        button3 = tkinter.Button(frame, height=90, width=90, padx=5, pady=5, image=settings, command=lambda: exit(1))

        # Add buttons to frame
        button1.pack(side=tkinter.LEFT)
        button2.pack(side=tkinter.LEFT)
        button3.pack(side=tkinter.LEFT)
        self.update()

    def order(self, product):
        self.master.Order.product = product
        self.master.p2.show()   # TODO: is master ok to use?
        self.update()


class PageQuantity(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        frame = tkinter.Frame(self, borderwidth=5, padx=10, pady=20, bg = 'cyan')
        self.quantity = 1
        frame.grid()  # This page works better with grind vs frame

        def increase_quantity():
            self.quantity += 1
            button2["text"] = str(self.quantity) + "\n (valitse)"
            if self.quantity > 1:
                button1.grid()
                button1_empty.grid_remove()
            if self.quantity > 9:
                button3.grid_remove()
                button1_empty.grid(row=0, column=3)

        def decrease_quantity():
            self.quantity -= 1
            button2["text"] = str(self.quantity) + "\n (valitse)"
            if self.quantity < 2:
                button1.grid_remove()
                button1_empty.grid(row=0, column=1)
            if self.quantity < 10:
                button3.grid()
                button3_empty.grid_remove()

        # luodaan painike
        button1 = tkinter.Button(frame, width=7, height=6, text="-", font=("Helvetica", 16), command=decrease_quantity)
        button1_empty = tkinter.Label(frame, width=7, height=6, text="", font=("Helvetica", 16))
        button2 = tkinter.Button(frame, width=7, height=6, text=str(self.quantity) + "\n (valitse)", font=("Helvetica", 16), command=self.order)
        button3 = tkinter.Button(frame, width=7, height=6, text="+", font=("Helvetica", 16), command=increase_quantity)
        button3_empty = tkinter.Label(frame, width=7, height=6, text="", font=("Helvetica", 16))

        # lisätään painike ikkunaan
        button1.grid(row=0, column=1)
        button2.grid(row=0, column=2)
        button3.grid(row=0, column=3)
        self.update()

    def order(self):
        if type(self.quantity) == int:
            print("add: ", self.quantity)
            self.master.Order.quantity = self.quantity
        else:
            exit(1)
        self.master.p3.show()
        self.update()

class PageSendOrder(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        frame = tkinter.Frame(self, borderwidth=5, padx=10, pady=20, bg = 'black')
        frame.pack(fill=tkinter.BOTH, expand=1)

        # luodaan painike
        button1 = tkinter.Button(frame, width=14, height=6, text="Lähetä tilaus", font=("Helvetica", 16), command=lambda: self.send_order())

        # lisätään painike ikkunaan
        button1.pack(side=tkinter.LEFT)
        self.update()

    def send_order(self):
        result = self.master.Order.send()
        if result:
            self.master.p4.show()
            self.update()
        else:
            print("result failed: ", result)
            self.master.p5.show()
            self.update()

class PageRegisterOk(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="REGISTER OK")
        label.pack(side="top", fill="both", expand=True)
        frame = tkinter.Frame(self, borderwidth=5,padx=10, pady=20, bg = 'green')

        frame.pack(fill=tkinter.BOTH, expand=1)

        # luodaan painike
        button1 = tkinter.Button(frame, width=7, height=6, text="continue", font=("Helvetica", 16), command=self.master.p0.show)

        # lisätään painike ikkunaan
        button1.pack(side=tkinter.LEFT)
        self.update()


class PageRegisterFailed(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="REGISTER FAILED")
        label.pack(side="top", fill="both", expand=True)
        frame = tkinter.Frame(self, borderwidth=5,padx=10, pady=20, bg = 'red')
        frame.pack(fill=tkinter.BOTH, expand=1)

        # luodaan painike
        button1 = tkinter.Button(frame, width=7, height=6, text="continue", font=("Helvetica", 16), command=self.master.p0.show)

        # lisätään painike ikkunaan
        button1.pack(side=tkinter.LEFT)
        self.update()

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        self.Order = google_api.Order()

        tk.Frame.__init__(self, *args, **kwargs)

        # Create pages
        p0 = self.p0 = PageIdentify(self)
        p1 = self.p1 = PageProduct(self)
        p2 = self.p2 = PageQuantity(self)
        p3 = self.p3 = PageSendOrder(self)
        p4 = self.p4 = PageRegisterOk(self)
        p5 = self.p5 = PageRegisterFailed(self)

        # Create Frames
        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        # Add pages
        p0.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # Create top menu bar (for testing - removed in end product (?))
        b0 = tk.Button(buttonframe, text="Identify", command=lambda: p0.lift())
        b1 = tk.Button(buttonframe, text="Product", command=lambda: p1.lift())
        b2 = tk.Button(buttonframe, text="Quantity", command=lambda: p2.lift())
        b3 = tk.Button(buttonframe, text="Confirm", command=lambda: p3.lift())

        # Show buttons
        b0.pack(side="left")
        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        # Show page
        p0.show()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        main = MainView(root)
        main.pack(side="top", fill="both", expand=True)
        root.wm_geometry("320x240")  # Junnus Raspberry pi resolution
        if platform.node() in ["vadelma", "raspberrypi"]:
            root.attributes('-fullscreen', True)  # Fullscreen for RPi
        root.mainloop()
    except Exception:
        logging.exception("Unkown exception in main loop")
        logging.critical("Exit program after error")
        exit(1)

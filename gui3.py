# -*- coding: utf-8 -*-

import Tkinter as tk
import Tkinter as tkinter
import google_api
import platform
import threading
import urllib.request
import time



# https://docs.google.com/spreadsheets/d/1sTuTq5U_kp0zuS32VVKr8_N70lUChA3c2Jewm3HWcEo/edit?usp=sharing
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()

    def hide(self):
        self.lower()


class PageProduct(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        frame = tkinter.Frame(self, borderwidth=5,padx=10, pady=20, bg = 'red')
        frame.pack(fill=tkinter.BOTH, expand=1)

        # Load icons
        Page.beer = beer = tkinter.PhotoImage(file="beer.gif")
        Page.cider = cider = tkinter.PhotoImage(file="cider.gif")
        Page.settings = settings = tkinter.PhotoImage(file="settings.gif")

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
        frame = tkinter.Frame(self, borderwidth=5,padx=10, pady=20, bg = 'cyan')
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
        frame = tkinter.Frame(self, borderwidth=5,padx=10, pady=20, bg = 'black')
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
        button1 = tkinter.Button(frame, width=7, height=6, text="continue", font=("Helvetica", 16), command=self.master.p1.show)

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
        button1 = tkinter.Button(frame, width=7, height=6, text="continue", font=("Helvetica", 16), command=self.master.p1.show)

        # lisätään painike ikkunaan
        button1.pack(side=tkinter.LEFT)
        self.update()


class PageNoInternet(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="We are out of internets!")
        label.pack(side="top", fill="both", expand=True)
        frame = tkinter.Frame(self, borderwidth=5,padx=10, pady=20, bg = 'red')
        frame.pack(fill=tkinter.BOTH, expand=1)

        # luodaan painike
        button1 = tkinter.Button(frame, width=7, height=6, text="go to start", font=("Helvetica", 16), command=self.master.p1.show)

        # lisätään painike ikkunaan
        button1.pack(side=tkinter.LEFT)
        self.update()


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        self.Order = google_api.Order()

        tk.Frame.__init__(self, *args, **kwargs)

        # Create pages
        p1 = self.p1 = PageProduct(self)
        p2 = self.p2 = PageQuantity(self)
        p3 = self.p3 = PageSendOrder(self)
        p4 = self.p4 = PageRegisterOk(self)
        p5 = self.p5 = PageRegisterFailed(self)
        p6 = self.p6 = PageNoInternet(self)

        # Create Frames
        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        # Add pages
        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p6.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # Create top menu bar (for testing - removed in end product (?))
        b1 = tk.Button(buttonframe, text="Product", command=lambda: p1.lift())
        b2 = tk.Button(buttonframe, text="Quantity", command=lambda: p2.lift())
        b3 = tk.Button(buttonframe, text="Confirm", command=lambda: p3.lift())

        # Show buttons
        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        # Show page
        p1.show()

        def check_thread():
            if self.mt.isAlive():
                # print("alive")
                internet_ok = self.after(600, check_thread)
                if internet_ok:
                    pass
                else:
                    print("not ok")
            else:
                print("dead")
                self.mt.start()


        # Run web-test
        self.mt = MyThread(error_page=p6)
        self.mt.daemon = True
        self.mt.start()
        check_thread()
        p6.show()


class MyThread(threading.Thread):

    def __init__(self, error_page):
        threading.Thread.__init__(self)
        self.connection = threading.Event()
        self.counter = 0
        self.error_page = error_page

    def run(self):
        while True:
            self.counter += 1
            self.connection.clear()
            try:

                url = 'http://www.google.fi'

                response = urllib.request.urlopen(url, timeout=20)
                self.connection.set()
            except urllib.request.URLError as err:
                self.connection.clear()
                pass
            finally:
                if self.connection.is_set():
                    self.error_page.hide()
                else:
                    self.error_page.show()
                time.sleep(1)

        print("fail3")

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("320x240")  # Junnus Raspberry pi resolution
    if platform.node() == "vadelma":
        root.attributes('-fullscreen', True)
    root.mainloop()


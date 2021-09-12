import tkinter as tk
import hashlib
import sys
import requests
# import requests, sys, os, csv, webbrowser
# from tkinter.filedialog import askopenfilename
# from tkinter import messagebox
from tkinter import font

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(pady=10)
        self.create_widgets()

    def create_widgets(self):
        myfont = font.Font(family="Helvetica", size=11,
                            weight='bold', slant='italic')

        self.entvar = tk.StringVar()
        self.entvar.trace("w", self.text_changed) # trigger changed event
        entry = tk.Entry(self, textvariable=self.entvar, bg='white')
        entry.grid(row=1, column=1, sticky=tk.W+tk.E)

        btn = tk.Button(self, command=self.btn_clicked, text="Check Password", font=myfont)
        btn.grid(row=2, column=1, sticky=tk.W+tk.E, pady=5)

        self.lblvar = tk.StringVar()
        lbl = tk.Label(self, width=22, textvariable=self.lblvar,
                      font=myfont, bg="white")
        lbl.grid(row=3, column=1)
        self.lblvar.set("haveibeenpwned.com")
        entry.focus()


    def text_changed(self, *args):
        self.lblvar.set('')

    def btn_clicked(self):
        pw = self.entvar.get()
        pw = pw.strip()
        sha1pwd, count = self.lookup_pwned_api(pw)
        if count:
          self.lblvar.set('found ' + str(count) + ' times')
        else:
          self.lblvar.set('found 0 times!')

    def lookup_pwned_api(self, pwd):
        """Returns hash and number of times password was seen in pwned database.
        Args:
            pwd: password to check
        """
        sha1pwd = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
        head, tail = sha1pwd[:5], sha1pwd[5:]
        url = 'https://api.pwnedpasswords.com/range/' + head
        res = requests.get(url)
        if res.status_code != 200:
          return "error", 0
        hashes = (line.split(':') for line in res.text.splitlines())
        count = next((int(count) for t, count in hashes if t == tail), 0)
        return sha1pwd, count

#
root = tk.Tk()
W = 250
H = 115
root.geometry('%dx%d' % (W, H))
root.title("Pwned ?")
# root.overrideredirect(True) # removed window decorations
root.resizable(0,0) # no resize & removes maximize button
app = Application(master=root)
app.mainloop()

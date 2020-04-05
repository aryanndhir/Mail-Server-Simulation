"""
reader/writer- If sent is empty, the person cannot read it. Email can be modified.
sender/receiver- message passing
priority-
binary semaphore - only one person can login
"""
from tkinter import *
from tkinter import ttk
import os
from os import path
import re
import json

if not path.exists('sentbox'):
    os.makedirs('sentbox')
if not path.exists('receivedbox'):
    os.makedirs('receivedbox')
if not path.exists('sentbox\\spam'):
    os.makedirs('sentbox\\spam')
if not path.exists('receivedbox\\queue'):
    os.makedirs('receivedbox\\queue')

if not path.isfile("accounts.txt"):
    with open(path.join(os.getcwd(), "accounts.txt"), 'w') as _:
        _.write("{}")


spamwords = ["dhir", "spam", "money", "$$$", "lottery"]
if not path.isfile("spamwords.txt"):
    with open(path.join(os.getcwd(), "spamwords.txt"), 'a') as f:
        f.write("\n".join(spamwords))

with open(path.join(os.getcwd(), "spamwords.txt"), 'r') as f:
    spamwords = f.readlines()

spamwords = [re.sub('\n', '', word) for word in spamwords]

window = Tk()
window.geometry("250x400")
window.title("Email Service")
window.resizable(width=False, height=False)
ff = Frame(window)
semLogin = 0


class mail:
    def __init__(self):
        global ff
        self.prior = IntVar()
        self.toget = StringVar()
        self.content = StringVar()
        self.sub = StringVar()
        self.user = StringVar()
        self.pwd = StringVar()
        self.choose = StringVar()
        self.backbutton = ttk.Button(window)

    def backButton(self, cmd):
        self.backbutton.destroy()
        self.backbutton = ttk.Button(window, text="Back", command=cmd)
        self.backbutton.grid(sticky=W)

    def logoutButton(self):
        global semLogin
        semLogin = 0
        self.backbutton.destroy()
        self.backbutton = ttk.Button(window, text="Logout", command=self.login)
        self.backbutton.grid(sticky=W)

    def die(self):
        ff.destroy()
        self.backbutton.destroy()

    def create(self):
        self.die()
        global ff
        ff = Frame(window)
        self.incorrectemail = ttk.Label(
            ff, text="Incorrect email!", font=("Calibri", 10))
        self.enteremail = ttk.Label(
            ff, text="Enter an email!", font=("Calibri", 10))
        self.emptybody = ttk.Label(
            ff, text="Cannot be empty!", font=("Calibri", 10))
        self.invalidreg = ttk.Label(
            ff, text="Invalid Email ID", font=("Calibri", 10))
        self.invalid = Label(ff, text="Invalid Email/Password",
                             fg="red", font=("Calibri", 10))
        self.alreadyexists = Label(
            ff, text="Username already exists!", font=("Calibri", 10))
        self.registered = Label(
            ff, text="Registered! Try logging in!", font=("Calibri", 10))
        self.lb1 = Listbox(ff, width=25)
        self.emptysubject = Label(
            ff, text="Subject cannot be empty!", font=("Calibri", 10))
        self.illegalseq = Label(
            ff, text="Illegal sequence entered!", font=("Calibri", 10))

    def clear(self):
        self.prior.set("")
        self.toget.set("")
        self.content.set("")
        self.user.set("")
        self.pwd.set("")

    def forgeterrors(self):
        enames = ['incorrectemail', 'enteremail', 'emptybody']
        self.incorrectemail.grid_forget()
        self.enteremail.grid_forget()
        self.emptybody.grid_forget()
        self.illegalseq.grid_forget()
        
    def sendfunc(self):
        self.forgeterrors()
        dir = path.dirname(__file__)
        to = self.toget.get()
        x = self.user.get()
        illegals = ["<priority>", "<subject>", "<body>"]
        if to:
            tmp = re.search("(\w+\.?)+@\w+.\w+", to)
            if tmp:
                ndir = path.join(dir, f"sentbox\\{x}--{to}.txt")
                content = contentbody.get('1.0', 'end')
                priority = self.prior.get()
                if content != "\n":
                    if self.sub.get() != "":
                        isIllegal = False
                        for il in illegals:
                            if il in content:
                                isIllegal = True
                                break
                        if not isIllegal:
                            for word in spamwords:
                                if word in content:
                                    ndir = path.join(
                                        dir, f"sentbox\\spam\\{x}--{to}.txt")
                                    break
                            try:
                                f = open(ndir, 'r+')
                            except:
                                f = open(ndir, 'w+')
                            msg = ""
                            msg += "<priority>" + \
                                   str(priority) + "<subject>" + \
                                self.sub.get() + "<body>" + content
                            f.write(msg)
                            f.close()
                            contentbody.delete('1.0', 'end')
                            self.sub.set("")
                            self.prior.set(1)
                            self.toget.set("")
                        else:
                            self.illegalseq.grid()
                    else:
                        self.emptysubject.grid()
                else:
                    self.emptybody.grid()
            else:
                self.incorrectemail.grid()
        else:
            self.enteremail.grid()

    def send(self):
        self.die()
        self.create()
        self.backButton(self.home)

        ttk.Label(ff, text="To:", font=("Calibri", 12)).grid()
        ttk.Entry(ff, textvariable=self.toget).grid()

        ttk.Label(ff, text="Subject:", font=("Calibri", 12)).grid()
        ttk.Entry(ff, textvariable=self.sub).grid()

        ttk.Label(ff, text="Content:", font=("Calibri", 12)).grid()
        global contentbody
        contentbody = Text(ff, height=10, width=29)
        contentbody.grid(padx=6)

        self.prior.set(1)
        ttk.Label(ff, text="Priority", font=("Calibri", 12)).grid()
        priorbox = ttk.Spinbox(
            ff, from_=0.0, to=4.0, textvariable=self.prior, wrap=True, width=5, state='readonly')
        priorbox.grid()
        ttk.Button(ff, text="Send", command=self.sendfunc).grid(pady=2)

        ff.grid()

    def onselect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        self.click = w.get(index)
        self.editbutton.configure(state = "normal")

    def edit1func(self):
        global s3, fp
        fp = self.user.get() + "--" + self.choose.get() + ".txt"
        s3 = p1 + "\\sentbox\\"

        self.lb1.delete(0, END)
        self.editbutton.configure(state = "disabled")
        l1.clear()


        for r, d, f in os.walk(p1 + '\\sentbox'):
            for file in f:
                if fp == file:
                    with open(r+"\\"+fp) as fc:
                        for line in fc.readlines():
                            if "<priority>" in line:
                                s1 = line.split("\n")
                                s2 = "".join(s1[0])
                                s2 = s2.split("<body>")
                                s2 = "".join(s2[0])
                                s2 = s2.split("<subject>")
                                l1.append(s2[1])
        for f in l1:
            self.lb1.insert(END, f)

        self.lb1.bind('<<ListboxSelect>>', self.onselect)

    def edit1(self):
        self.die()
        self.create()
        self.backButton(self.home)

        global p1, ctr
        p1 = os.getcwd()

        global l1
        files, l1 = set(), []

        for r, d, f in os.walk(p1 + '\\sentbox'):
            for file in f:
                if '.txt' in file:
                    s1 = self.user.get() + "--"
                    if s1 in file:
                        s2 = file.split("--")
                        s3 = s2[1].split(".txt")
                        files.add(s3[0])

        ttk.Label(ff, text="Select Email ID", font=(
            "Calibri", 12)).grid(row=0, column=0)
        self.lb1.grid(row=3, column=0)

        ttk.Label(ff, text="Select Mail", font=(
            "Calibri", 12)).grid(row=2, column=0)

        ttk.OptionMenu(ff, self.choose, "Select one", *files,
                       command=lambda _: self.edit1func()).grid(row=1, column=0)

        self.editbutton = ttk.Button(ff, text="Edit", command=self.edit2)
        self.editbutton.configure(state="disabled")
        self.editbutton.grid(pady=5)

        ff.grid(padx=36, pady=30)

    def noshift(self, path, sub, content):
        l2, ctr = [], 0
        with open(path) as fc:
            for line in fc.readlines():
                if sub in line:
                    l2.append("<priority>" + str(self.prior.get()) + "<subject>" + self.click + "<body>" + content)
                    ctr += 1
                elif ctr == 1 and "<priority>" not in line:
                    continue
                else:
                    ctr = 0
                    l2.append(line)

        fc = open(s3 + fp, "w")
        for i in l2:
            fc.write(i)
        fc.close()

    def shift(self, p1, p2, sub, content):
        l2, l3, ctr = [], [], 0
        with open(p1) as fc:
            for line in fc.readlines():
                if sub in line:
                    l2.append(line)
                    ctr = 1
                elif ctr == 1 and "<priority>" not in line:
                    l2.append(line)
                elif ctr == 1 and "<priority>" in line:
                    break

        with open(p1) as fc:
            for line in fc.readlines():
                if line not in l2:
                    l3.append(line)

        l2 = ["<priority>" + str(self.prior.get()) + "<subject>" + self.click + "<body>" + content]

        if not l3:
            os.remove(p1)
        else:
            fc = open(p1, "w")
            for i in l3:
                fc.write(i)
            fc.close()

        if path.isfile(p2):
            with open(p2) as fc:
                for line in fc.readlines():
                    l2.append(line)

        fc = open(p2, "w")
        for i in l2:
            fc.write(i)
        fc.close()

    def edit2func(self):
        global sp
        ctr1, ctr2 = 0, 0
        # ctr1 indicates if its still spam or not
        # ctr2 indicates if its in spam folder or not
        s3 = p1 + "\\sentbox\\"
        fp = self.user.get() + "--" + self.choose.get() + ".txt"
        sub = ">" + self.click + "<"
        content = cb.get('1.0', 'end')

        for word in spamwords:
            if word in content:
                ctr1 = 1
                break

        for r, d, f in os.walk(p1 + '\\sentbox'):
            for file in f:
                if fp == file:
                    with open(r + "\\" + fp) as fc:
                        for line in fc.readlines():
                            if sub in line:
                                if "spam" in r:
                                    ctr2 = 1

        if ctr1 == 0 and ctr2 == 0:
            self.noshift(s3+fp, sub, content)

        elif ctr1 == 1 and ctr2 == 1:
            self.noshift(s3+"spam\\"+fp, sub, content)

        elif ctr1 == 1 and ctr2 == 0:
            self.shift(s3+fp, s3+"spam\\"+fp, sub, content)

        elif ctr1 == 0 and ctr2 == 1:
            self.shift(s3+"spam\\"+fp, s3+fp, sub, content)
            
    def edit2(self):
        self.die()
        self.create()
        self.backButton(self.edit1)
        ttk.Label(ff, text="Edit Message", font=(
            "Calibri", 12)).grid(row=0, column=0)
        ttk.Label(ff, text=f"To:  {self.choose.get()}", font=(
            "Calibri", 12)).grid(row=1, column=0)
        global cb
        cb = Text(ff, height=10, width=29)
        ctr = 0
        self.selectsomething = Label(ff, text="Please ensure selection!")
        self.editsavebutton = ttk.Button(ff, text="Save", command=self.edit2func)
        try:
            self.selectsomething.grid_forget()
            self.editsavebutton.configure(state="normal")
            sub = ">" + self.click + "<"
            s3 = p1 +"\\sentbox\\" + fp

            for r, d, f in os.walk(p1 + '\\sentbox'):
                for file in f:
                    if fp == file:
                        with open(r + "\\" + fp) as fc:
                            for line in fc.readlines():
                                if sub in line:
                                    if "spam" in r:
                                        s3 = p1 + "\\sentbox\\spam\\"+fp
                                        break
            try:
                with open(s3) as fc:
                    for line in fc.readlines():
                        if sub in line:
                            l2 = line.split("<body>")
                            s1 = l2[1]
                            ctr += 1
                        elif ctr > 0 and "<priority>" not in line:
                            s1 += line
                        elif ctr > 0 and "<priority>" in line:
                            break
                self.editbody = s1

                cb.insert(END, self.editbody)
                cb.grid(padx=6)
            except FileNotFoundError:
                self.selectsomething.grid()
                self.editsavebutton.configure(state="disabled")
        except AttributeError:
            self.selectsomething.grid()
            self.editsavebutton.configure(state="disabled")

        self.prior.set(1)
        ttk.Label(ff, text="Priority", font=("Calibri", 12)).grid()
        priorbox = ttk.Spinbox(
            ff, from_=0.0, to=4.0, textvariable=self.prior, wrap=True, width=5, state='readonly')
        priorbox.grid()

        self.editsavebutton.grid(pady=5)
##        except:
##            self.selectsomething.grid()
        ff.grid(pady=2)

    def read1func(self):
        self.selectsomething = Label(ff, text="Please ensure selection!")
        self.selectsomething.grid_forget()
        global s3, s4
        s3 = p1 + "\\sentbox\\" + self.choose.get() + "--" + self.user.get() + ".txt"
        s4 = p1 + "\\receivedbox\\" + self.user.get() + "--" + self.choose.get() + ".txt"
        self.lb1.delete(0, END)
        l1.clear()
        try:
            with open(s3) as fc:
                for line in fc.readlines():
                    if "<priority>" in line:
                        s1 = line.split("\n")
                        s2 = "".join(s1[0])
                        s2 = s2.split("<body>")
                        s2 = "".join(s2[0])
                        s2 = s2.split("<subject>")
                        l1.append(s2[1])

            for f in l1:
                self.lb1.insert(END, f)
        except:
            self.selectsomething.grid()

        self.lb1.bind('<<ListboxSelect>>', self.onselect)

    def read1(self):
        self.die()
        self.create()
        self.backButton(self.home)

        global p1
        p1 = os.getcwd()

        global l1
        files, l1 = set(), []

        for r, d, f in os.walk(p1 + '\\sentbox'):
            for file in f:
                if '.txt' in file:
                    s1 = "--" + self.user.get()
                    if s1 in file:
                        s2 = file.split("--")
                        s3 = s2[0]
                        files.add(s3)

        ttk.Label(ff, text="Select Email ID", font=(
            "Calibri", 12)).grid(row=0, column=0)
        self.lb1.grid(row=3, column=0)

        ttk.Label(ff, text="Select Mail", font=(
            "Calibri", 12)).grid(row=2, column=0)
        ttk.OptionMenu(ff, self.choose, "Select one", *files,
                       command=lambda _: self.read1func()).grid(row=1, column=0)

        ttk.Button(ff, text="Read", command=self.read2).grid(pady=5)

        def purgeinbox():
            dir_name = os.getcwd() + "\\receivedbox"
            test = os.listdir(dir_name)

            for item in test:
                if item.endswith(".txt"):
                    os.remove(os.path.join(dir_name, item))
            dir_name = os.getcwd() + "\\receivedbox\\queue"
            test = os.listdir(dir_name)

            for item in test:
                os.replace(os.getcwd() + "\\receivedbox\\queue" + item,
                           os.getcwd() + "\\receivedbox\\" + item)
        Button(ff, text="Purge Inbox",
               command=purgeinbox).grid(pady=3)
        
        ff.grid(padx=36, pady=30)

    def read2func(self):

        sub = ">" + self.click + "<"
        l2, ctr, l3 = [], 0, []
        with open(s3) as fc:
            for line in fc.readlines():
                if sub in line:
                    l2.append(line)
                    ctr += 1
                elif ctr > 0 and "<priority>" not in line:
                        l2.append(line)
                elif ctr > 0 and "<priority>" in line:
                    break

        with open(s3) as fc:
            for line in fc.readlines():
                if line not in l2:
                    l3.append(line)

        if not l3:
            os.remove(s3)
        else:
            fc = open(s3, "w")
            for i in l3:
                fc.write(i)
            fc.close()

        s4 = p1 + "\\receivedbox\\" + self.choose.get() + "--" + self.user.get() + ".txt"
        fc = open(s4, "w")
        for i in l2:
            fc.write(i)
        fc.close()
        self.read1()

    def read2(self):
        try:
            self.die()
            self.create()
            self.backButton(self.read1)
            ttk.Label(ff, text="Read Message", font=(
                "Calibri", 12)).grid(row=0, column=0)
            ttk.Label(ff, text=f"From:  {self.choose.get()}", font=(
                "Calibri", 12)).grid(row=1, column=0)
            self.selectsomething = Label(ff, text="Please ensure selection!")
            self.selectsomething.grid_forget()
            global cb
            cb = Text(ff, height=10, width=29)
            ctr = 0
            sub = ">" + self.click + "<"

            with open(s3) as fc:
                for line in fc.readlines():
                    if sub in line:
                        l2 = line.split("<body>")
                        s1 = l2[1]
                        ctr += 1
                    elif ctr > 0 and "<priority>" not in line:
                        s1 += line
                    elif ctr > 0 and "<priority>" in line:
                        break

            self.readbody = s1

            cb.insert(END, self.readbody)
            cb.grid(padx=6)
            cb.configure(state="disabled")
            self.prior.set(1)
            ttk.Label(ff, text="Priority", font=("Calibri", 12)).grid()
            priorbox = ttk.Spinbox(
                ff, from_=0.0, to=4.0, textvariable=self.prior, wrap=True, width=5, state='disabled')
            priorbox.grid()

            ttk.Button(ff, text="Close", command=self.read2func).grid(pady=5)

        except:
            self.backButton(self.read1)
            self.selectsomething.grid()
        ff.grid(pady=2)

    def home(self):
        self.die()
        self.create()
        self.logoutButton()

        Button(ff, text="Send", command=self.send,
               height=2, width=8).grid(pady=5)
        Button(ff, text="Edit", command=self.edit1,
               height=2, width=8).grid(pady=5)
        Button(ff, text="Read", command=self.read,
               height=2, width=8).grid(pady=5)
        ff.grid(padx=90, pady=75)

    def validatelogin(self):
        global semLogin
        u1 = self.user.get()
        pwd = self.pwd.get()
        ctr = 0

        d2 = json.load(open("accounts.txt"))
        try:
            if d2[u1] == pwd:
                ctr = 1

            if ctr == 0:
                self.invalid.grid()
            else:
                semLogin = 1
                self.home()
        except:
            self.invalid.grid()

    def validatesignup(self):
        self.forgeterrors()
        u = self.user.get()
        p = self.pwd.get()
        d2 = json.load(open("accounts.txt"))

        if u == "" or p == "":
            self.emptybody.grid()
        elif u in d2:
            self.alreadyexists.grid()
        elif not re.search("(\w+\.?)+@\w+.\w+", u):
            self.invalidreg.grid()
        else:
            d2[u] = p
            json.dump(d2, open("accounts.txt", 'w'))

            self.login()

    def register(self):
        self.die()
        self.create()
        self.backButton(self.login)

        Label(ff, text="Enter New Email ID", font=("Calibri", 12)).grid()
        ttk.Entry(ff, textvariable=self.user).grid()
        Label(ff, text="Enter New Password", font=("Calibri", 12)).grid()

        ttk.Entry(ff, textvariable=self.pwd).grid()
        Button(ff, text="Register", command=self.validatesignup,
               height=2, width=8).grid(pady=5)

        ff.grid(padx=50, pady=60)

    def login(self):
        global semLogin

        self.die()
        self.create()
        self.clear()

        l1 = Label(ff, text="Email ID", font=("Calibri", 12))
        l1.grid(pady=5)

        e1 = ttk.Entry(ff, textvariable=self.user)
        e1.grid()

        l2 = Label(ff, text="Password", font=("Calibri", 12))
        l2.grid(pady=5)

        e2 = ttk.Entry(ff, textvariable=self.pwd, show="*")
        e2.grid()

        bframe = Frame(ff)
        b1 = Button(bframe, text="Login", command=self.validatelogin,
                    height=2, width=8)
        b1.grid()
        b2 = Button(bframe, text="Register", command=self.register,
                    height=2, width=8)
        b2.grid(pady=6)
        bframe.grid(pady=6)

        if semLogin != 0:
            Label(ff, text="System busy!", fg='red').grid()
            l1.configure(state='disabled')
            l2.configure(state='disabled')
            e1.configure(state='disabled')
            e2.configure(state='disabled')
            b1.configure(state='disabled')
            b2.configure(state='disabled')

        ff.grid(padx=52, pady=40)

    def read(self):
        self.die()
        self.create()
        self.backButton(self.home)

        Label(ff, text="INBOX", font=("Calibri", 12)).grid()
        msg = Label(ff, text="Select username:", font=("Calibri", 12))
        msg.grid()
        inbox = ttk.Combobox(ff)
        p1 = os.getcwd()
        senders_emails = []
        file_names = []
        path, dirs, files = next(os.walk("receivedbox"))
        file_count = len(files)

        exclude=set("spam")
        
        for r, d, f in os.walk(p1 + '\\sentbox'):
            for file in f:
                if '.txt' in file:
                    s1 = "--" + self.user.get()
                    if 'spam' not in r:
                        if s1 in file:
                            s2 = file.split("--")
                            senders_emails.append(s2[0])
                            file_names.append(file)

        def readmessage():
            def revSort(tup):   
                lst = len(tup)  
                for i in range(0, lst):  
                    for j in range(0, lst-i-1):  
                        if (tup[j][1] > tup[j + 1][1]):  
                            temp = tup[j]  
                            tup[j]= tup[j + 1]  
                            tup[j + 1]= temp
                return tup[::-1]
            msg.config(text="")
            sender = inbox.get()
            file_to_display = file_names[senders_emails.index(sender)]
            lines = []
            try:
                priorlist=[]
                with open('sentbox\\' + file_to_display) as fc:
                    reads = fc.read()
                    x = reads.split("<priority>")
                    del x[0]
                    for mail in x:
                        y = mail.split("<body>")
                        forprior = (y[1], int(y[0][0]))
                        priorlist.append(forprior)
                
                for vals in revSort(priorlist):
                    lines.append(vals[0])
                    lines.append("\n------\n")
                msg.config(text="".join(lines))
                if(file_count < 6):
                    os.replace(os.getcwd() + "\\sentbox\\" + file_to_display,
                               os.getcwd() + "\\receivedbox\\" + file_to_display)
                else:
                    os.replace(os.getcwd() + "\\sentbox\\" + file_to_display,
                               os.getcwd() + "\\receivedbox\\queue\\" + file_to_display)
            except FileNotFoundError:
                pass

        def purgeinbox():
            dir_name = os.getcwd() + "\\receivedbox"
            test = os.listdir(dir_name)

            for item in test:
                if item.endswith(".txt"):
                    os.remove(os.path.join(dir_name, item))
            dir_name = os.getcwd() + "\\receivedbox\\queue"
            test = os.listdir(dir_name)

            for item in test:
                os.replace(os.getcwd() + "\\receivedbox\\queue" + item,
                           os.getcwd() + "\\receivedbox\\" + item)

        inbox['values'] = senders_emails
        inbox.grid()
        Button(ff, text="Read Message",
               command=readmessage).grid(pady=3)
        Button(ff, text="Purge Inbox",
               command=purgeinbox).grid(pady=3)

        ff.grid(padx=40)


obj = mail()
obj.create()
obj.login()
window.mainloop()

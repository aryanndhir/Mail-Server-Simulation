import os

"""This was made as a part of a project. However, with proper tinkering, can work with any file.

This function looks for words in the entire 'sentbox' directory and filters spam emails and moves them to spam.
It also looks at spam emails to make sure that no non-spam messages are in the spam folder."""

"""
The 'emails' are in this format in the .txt files.
<priority>3<subject>hidc<body>dc1234
"""

spamwords = ["dhir", "spam", "money", "$$$", "lottery"]

def spamSweeper():
    cwd=os.getcwd()
    normal = cwd + "\\sentbox\\"
    spambox = normal + "\\spam\\"

    def makeFile(filename):
            try:
                t=open(filename, 'r')
                t.close()
            except:
                t=open(filename, 'w')
                t.close()

    def moveSpam(isSpam, filename, mail):
        if isSpam:
            spamf=os.path.join(spambox, filename+"_")
            makeFile(spamf)
            if mail:
                with open(spamf, "a") as f:
                    f.write("<priority>"+mail)
        else:
            normalf=os.path.join(normal, filename+"_")
            makeFile(normalf)
            if mail:
                with open(normalf, "a") as f:
                    f.write("<priority>"+mail)
            
    for root, dirs, files in os.walk(normal):
         for file in files:
            if file.endswith(".txt"):
                tmp= os.path.join(root, file)
                #print(tmp)
                with open(tmp, "r") as f:
                    mails= f.read()
                    mails=mails.split("<priority>")
                    for mail in mails:
                        isSpam=False
                        for word in spamwords:
                            if word in mail:
                                print("spam found!!!")
                                print(file)
                                print(mail)
                                isSpam=True
                                break
                        moveSpam(isSpam, file, mail)

    for root, dirs, files in os.walk(normal):
        for file in files:
            if file.endswith(".txt"):
                os.remove(os.path.join(root, file))
    for root, dirs, files in os.walk(normal):
        for file in files:
            if file.endswith(".txt_"):
                name=os.path.join(root, file)
                with open(name, "r") as f:
                    readit = f.read()
                if not readit or readit.isspace():
                    os.remove(name)
                else:
                    os.rename(name, name[:-1])
                        
    

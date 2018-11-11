import os

def cmd():
    while True:
        # read cmd
        file = open("./static/ajax/linuxcmd.txt", "r")
        text = file.read()
        file.close()

        if (text != ""):
            # clear cmd
            file = open("./static/ajax/linuxcmd.txt", "w")
            file.write("")
            file.close()
            # print(text)
            os.system(text)

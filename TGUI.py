# -*- coding: utf-8 -*-
from Tkinter import *
import project_new


def main():
    def get_list():
        machines.delete(0.0, END)
        machines.insert(END, project_new.get_list())

#    def get_info():
#        project_new.get_info(ip.get())

    def click():
        project_new.known_ip(ip.get())

    def ran():
        project_new.ran_ip()

    def cw():
        root.destroy()
        exit()

    root = Tk()  # creates interface

    root.iconbitmap('ssh.ico')  # creates logo

    root.title("Cyber Project")  # creates title

    machines = Text(root, width=100, height=3, wrap=WORD, background="white")  # stores scan output
    machines.grid(row=2, column=0, columnspan=2, sticky=W)

    root.configure(background='black')  # creates background

    Label(root, text="WELCOME TO OUR CYBER PROJECT!", bg="black", fg="white", font="none 12 bold")\
        .grid(row=0,
              column=0,
              sticky=W)  # creates page title

    Label(root, text="SCAN NETWORK FOR HOSTS ------------------------------------> ", bg="black", fg="white", font="none 12 bold")\
        .grid(row=1,
              column=0,
              sticky=W)  # creates scan lable

    Button(root, text="SCAN", width=4, command=get_list).grid(row=1, column=0, sticky=E)  # creates scan button

    Label(root, text="Enter ip: ", bg="black", fg="white", font="none 12 bold").grid(row=3, column=0, sticky=W)  # creates label

    ip = Entry(root, width=20, bg="white")
    ip.grid(row=4, column=0, sticky=W)  # stores ip input

    #Button(root, text="GET INFO ABOUT A MACHINE", width=24, command=get_info()).grid(row=5, column=0, sticky=W)

    Button(root, text="SSH TUNNEL!", width=11, command=click).grid(row=6, column=0, sticky=W)  # button for tunneling

    Button(root, text="PRESS ME FOR RANDOM MACHINE TUNNELING SSH!", width=42, command=ran).grid(row=8, column=0, sticky=W)  # button for random tunneling

    Button(root, text="Exit", width=14, command=cw).grid(row=9, column=0, sticky=W)  # creates exit button

    root.mainloop()


if __name__ == '__main__':
    main()

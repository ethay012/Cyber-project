# -*- coding: utf-8 -*-
from Tkinter import *
import project_2.0


def main():
    def click():
        project.known_ip(ip.get())

    def ran():
        project.ran_ip()

    def cw():
        root.destroy()
        exit()

    root = Tk()
    root.title("Cyber Project")
    root.configure(background="black")
    Label(root, text="WELCOME TO OUR CYBER PROJECT!", bg="black", fg="white", font="none 12 bold").grid(row=0, column=0, sticky=W)
    Label(root, text="Enter ip: ", bg="black", fg="white", font="none 12 bold").grid(row=1, column=0, sticky=W)
    ip = Entry(root, width=20, bg="white")
    ip.grid(row=2, column=0, sticky=W)
    Button(root, text="LET'S SSH AND STUFF!", width=20, command=click).grid(row=4, column=0, sticky=W)
    Label(root, text="Press for random ip.", bg="black", fg="white", font="none 12 bold").grid(row=5, column=0, sticky=W)
    Button(root, text="LET'S PROBABLY GET ARRESTED AND STUFF!", width=38, command=ran).grid(row=6, column=0, sticky=W)
    Button(root, text="Exit", width=14, command=cw).grid(row=7, column=0, sticky=W)

    root.mainloop()


if __name__ == '__main__':
    main()
import requests
from bs4 import BeautifulSoup
import os
import tkinter as tk
from tkinter import messagebox as msg
from PIL import Image,ImageTk

def download():
    manga_name = manga_entry.get().strip().lower().replace(' ','-')
    #credits : Manga kakalot site used in this project.
    #Prefer Mangakakalot to read Manga Online for free
    if len(manga_entry.get()) == 0:
        msg.showerror("Invalid","Enter Valid Manga name")
    if len(chapter_entry.get()) == 0:
        msg.showerror("Invalid","Enter Valid Chapter Number")
    if len(manga_entry.get()) !=0 and len(chapter_entry.get()) !=0:
        URL = requests.get("https://mangakakalot.fun/chapter/{}".format(manga_name))
        soup = BeautifulSoup(URL.content,'html.parser')
        tag = soup.find("title")
        save_image(manga_name,chapter_entry.get())

def save_image(name,chapter):
    os.mkdir("{}_chapter{}_manga".format(name.capitalize(),chapter))
    os.chdir("{}_chapter{}_manga".format(name.capitalize(),chapter))
    for index in range(1,150):
        URL = requests.get("https://img.mghubcdn.com/file/imghub/{}/{}/{}.jpg".format(name,chapter,index))
        if URL.status_code == 200:
            with open(f"{index}.jpg", "wb+") as f:
                f.write(URL.content)
        else:
            break
    if len(os.listdir()) != 0:
        msg.showinfo("Successfully Downloaded","Check the folder and Enjoy reading")
    else:
        msg.showerror("Invalid","Invalid Entry")

    manga_entry.delete(0,"end")
    chapter_entry.delete(0,"end")

def main():
    root = tk.Tk()
    root.geometry("455x425+425+150")
    root.resizable(False,False)
    root.title("Manga scrapping")

    # adjust the opacity for background image
    img = Image.open('manga.png')
    img = img.convert("RGBA")
    data=img.getdata() #list of tuples
    newData=[]
    for i in data:
        i=i[:3]
        i=i+(180,)
        newData.append(i)
    img.putdata(newData)
    img = img.resize((453,430), Image.ANTIALIAS)
    bg= ImageTk.PhotoImage(img)

    canvas= tk.Canvas(root)
    canvas.pack(expand=True, fill= "both")
    canvas.create_image(0,0,image=bg, anchor="nw")

    global manga_entry,chapter_entry
    manga = tk.StringVar()
    chapter = tk.StringVar()

    manga_head = tk.Label(text="Download Manga Chapters",font=("arial",18,"bold"),fg="black").place(x=60,y=15,width=340,height=40)

    manga_name = tk.Label(text="Enter Manga",font=("times new roman",15,"bold"),fg="black",bg="grey").place(x=45,y=205)
    chap_num = tk.Label(text="Enter Chapter",font=("times new roman",15,"bold"),fg="black",bg="grey").place(x=30,y=275)

    manga_entry = tk.Entry(textvariable=manga,font=("arial",15,"bold"),bd=5)
    manga_entry.place(x=180,y=190,width=200,height=50)
    manga_entry.focus_set()
    chapter_entry = tk.Entry(textvariable=chapter,font=("arial",15,"bold"),bd=5)
    chapter_entry.place(x=180,y=260,width=200,height=50)

    btn = tk.Button(text="Download",font=("times new roman",15,"bold"),command=download,bd=5,fg="white",bg="blue").place(x=165,y=340,width=100,height=40)
    root.mainloop()

if __name__ == '__main__':
    main()
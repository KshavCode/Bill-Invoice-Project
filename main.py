from tkinter import *
import datetime
import os
from tkinter import messagebox
import json

datenow = datetime.datetime.now()
datenow = datenow.strftime("%d-%b-%Y")
root = Tk()
root.geometry("920x600")
root.resizable(False, False)
root.title("Bill Invoice")
root.iconbitmap("C:\\Users\\PC\\Downloads\\bill-512.ico")

def invoplus():
    calculate_fun()
    if int(float(totalamount.get())) == 0:
        messagebox.showerror(
            "Error!", "How are you going to save an empty invoice? Check if you have entered all the details correctly.")
    elif cname.get() == "":
        messagebox.showerror(
            "Invalid Bill", "Looks like you forgot to add the customer name!.")
    else:
        msg_box = messagebox.askquestion(
            "Confirmation", "Do you really want to save the bill?")
        if msg_box == "yes":
            global inum
            cusname = cname.get()
            ii1 = i1.get()
            ii2 = i2.get()
            ii3 = i3.get()
            ii4 = i4.get()
            ii5 = i5.get()
            ii6 = i6.get()
            tamount = totalamount.get()
            quanti1 = quantity1.get()
            quanti2 = quantity2.get()
            quanti3 = quantity3.get()
            quanti4 = quantity4.get()
            quanti5 = quantity5.get()
            quanti6 = quantity6.get()
            pri1 = price1.get()
            pri2 = price2.get()
            pri3 = price3.get()
            pri4 = price4.get()
            pri5 = price5.get()
            pri6 = price6.get()
            amoun1 = amount1.get()
            amoun2 = amount2.get()
            amoun3 = amount3.get()
            amoun4 = amount4.get()
            amoun5 = amount5.get()
            amoun6 = amount6.get()
            if ii1 == "Select an item or select None otherwise" or ii1 == "None":
                ii1 = ""
            if ii2 == "Select an item or select None otherwise" or ii2 == "None":
                ii2 = ""
            if ii3 == "Select an item or select None otherwise" or ii3 == "None":
                ii3 = ""
            if ii4 == "Select an item or select None otherwise" or ii4 == "None":
                ii4 = ""
            if ii5 == "Select an item or select None otherwise" or ii5 == "None":
                ii5 = ""
            if ii6 == "Select an item or select None otherwise" or ii6 == "None":
                ii6 = ""

            with open(f"Invoice{datenow}\\invoice", "r") as t:
                inum = int(t.read())

            with open(f"Invoice{datenow}\\invoice", "w") as p:
                p.write(str(inum+1))

            with open(f"Invoice{datenow}\\{inum}.txt", "w", encoding="utf-8") as q:
                q.write(f"Invoice No. - {inum}, Customer name - {cusname}\n\nItems ~\n{ii1} (₹{pri1}x{quanti1}={amoun1})\n{ii2} (₹{pri2}x{quanti2}={amoun2})\n{ii3} (₹{pri3}x{quanti3}={amoun3})\n{ii4} (₹{pri4}x{quanti4}={amoun4})\n{ii5} (₹{pri5}x{quanti5}={amoun5})\n{ii6} (₹{pri6}x{quanti6}={amoun6})\n\nTotal Amount = ₹{tamount}")

            invar.set("{:04d}".format(inum+1))
            cname.set("")
            i1.set("Select an item or select None otherwise")
            i2.set("Select an item or select None otherwise")
            i3.set("Select an item or select None otherwise")
            i4.set("Select an item or select None otherwise")
            i5.set("Select an item or select None otherwise")
            i6.set("Select an item or select None otherwise")
            price1.set("")
            price2.set("")
            price3.set("")
            price4.set("")
            price5.set("")
            price6.set("")
            quantity1.set("")
            quantity2.set("")
            quantity3.set("")
            quantity4.set("")
            quantity5.set("")
            quantity6.set("")
            amount1.set("")
            amount2.set("")
            amount3.set("")
            amount4.set("")
            amount5.set("")
            amount6.set("")
        else:
            pass


def reset_fun():
    cname.set("")
    i1.set("Select an item or select None otherwise")
    i2.set("Select an item or select None otherwise")
    i3.set("Select an item or select None otherwise")
    i4.set("Select an item or select None otherwise")
    i5.set("Select an item or select None otherwise")
    i6.set("Select an item or select None otherwise")
    price1.set("")
    price2.set("")
    price3.set("")
    price4.set("")
    price5.set("")
    price6.set("")
    quantity1.set("")
    quantity2.set("")
    quantity3.set("")
    quantity4.set("")
    quantity5.set("")
    quantity6.set("")
    amount1.set("")
    amount2.set("")
    amount3.set("")
    amount4.set("")
    amount5.set("")
    amount6.set("")
    totalamount.set("")


def calculate_fun():
    a = "Select an item or select None otherwise"

    if i1.get() == "None" or i1.get() == "Select an item or select None otherwise":
        messagebox.showerror(
            "Items?", "How are you going to calculate when you didn't enter any item name.")
    else:
        it1 = i1.get()
        it2 = i2.get()
        it3 = i3.get()
        it4 = i4.get()
        it5 = i5.get()
        it6 = i6.get()
        if it1:
            with open("Docs\\prices.json") as g:
                jqr = json.load(g)["price"][it1]
            price1.set(jqr)
        if it2:
            with open("Docs\\prices.json") as g:
                jr = json.load(g)["price"][it2]
            price2.set(jr)
        if it3:
            with open("Docs\\prices.json") as g:
                jer = json.load(g)["price"][it3]
            price3.set(jer)
        if it4:
            with open("Docs\\prices.json") as g:
                jre = json.load(g)["price"][it4]
            price4.set(jre)
        if it5:
            with open("Docs\\prices.json") as g:
                jrrr = json.load(g)["price"][it5]
            price5.set(jrrr)
        if it6:
            with open("Docs\\prices.json") as g:
                jrr = json.load(g)["price"][it6]
            price6.set(jrr)

        pricee1 = price1.get()
        pricee2 = price2.get()
        pricee3 = price3.get()
        pricee4 = price4.get()
        pricee5 = price5.get()
        pricee6 = price6.get()
        quantityy1 = quantity1.get()
        quantityy2 = quantity2.get()
        quantityy3 = quantity3.get()
        quantityy4 = quantity4.get()
        quantityy5 = quantity5.get()
        quantityy6 = quantity6.get()

        if it1 == a or it1 == "None":
            pricee1 = 0
        if it2 == a or it2 == "None":
            pricee2 = 0
        if it3 == a or it3 == "None":
            pricee3 = 0
        if it4 == a or it4 == "None":
            pricee4 = 0
        if it5 == a or it5 == "None":
            pricee5 = 0
        if it6 == a or it6 == "None":
            pricee6 = 0

        if not quantityy1:
            quantityy1 = 0
        if not quantityy2:
            quantityy2 = 0
        if not quantityy3:
            quantityy3 = 0
        if not quantityy4:
            quantityy4 = 0
        if not quantityy5:
            quantityy5 = 0
        if not quantityy6:
            quantityy6 = 0

        try:
            calc1 = float(pricee1)*float(quantityy1)
            calc2 = float(pricee2)*float(quantityy2)
            calc3 = float(pricee3)*float(quantityy3)
            calc4 = float(pricee4)*float(quantityy4)
            calc5 = float(pricee5)*float(quantityy5)
            calc6 = float(pricee6)*float(quantityy6)
            amount1.set(calc1)
            amount2.set(calc2)
            amount3.set(calc3)
            amount4.set(calc4)
            amount5.set(calc5)
            amount6.set(calc6)
            totalamount.set(calc1+calc2+calc3+calc4+calc5+calc6)
        except:
            messagebox.showwarning(
                "Error", "Do you think you entered numerical values only?")


item_lis = []
with open("Docs\\items.txt") as ab:
    item = ab.readlines()
    for i in item:
        j = i.strip()
        item_lis.append(j)
try:
    with open(f"Invoice{datenow}\\invoice") as re:
        filee = re.read()
        filee = int(filee)
        inum = "{:04d}".format(filee)
except:
    os.mkdir(
        f"C:\\Users\\PC\\Desktop\\Coding Tutorial\\Project\\Bill Invoice\\Invoice{datenow}")
    with open(f"Invoice{datenow}\\invoice", "w") as wr:
        wr.write("1")
    with open(f"Invoice{datenow}\\invoice") as re:
        filee = int(re.read())
        inum = "{:04d}".format(filee)

invar = StringVar()
cname = StringVar()
i1 = StringVar()
i2 = StringVar()
i3 = StringVar()
i4 = StringVar()
i5 = StringVar()
i6 = StringVar()
price1 = StringVar()
price2 = StringVar()
price3 = StringVar()
price4 = StringVar()
price5 = StringVar()
price6 = StringVar()
quantity1 = StringVar()
quantity2 = StringVar()
quantity3 = StringVar()
quantity4 = StringVar()
quantity5 = StringVar()
quantity6 = StringVar()
amount1 = StringVar()
amount2 = StringVar()
amount3 = StringVar()
amount4 = StringVar()
amount5 = StringVar()
amount6 = StringVar()
totalamount = StringVar()

invar.set(inum)
i1.set("Select an item or select None otherwise")
i2.set("Select an item or select None otherwise")
i3.set("Select an item or select None otherwise")
i4.set("Select an item or select None otherwise")
i5.set("Select an item or select None otherwise")
i6.set("Select an item or select None otherwise")

can = Canvas(width=320.5, height=1000)
can.create_line(320.5, 0, 320.5, 350, width=5)

inv = Label(root, text="Invoice No. : ", font="garamond 18")
custname = Label(root, text="Customer Name :", font="garamond 16")
ite1 = Label(root, text="Item 1 : ", font="garamond 16")
ite2 = Label(root, text="Item 2 : ", font="garamond 16")
ite3 = Label(root, text="Item 3 : ", font="garamond 16")
ite4 = Label(root, text="Item 4 : ", font="garamond 16")
ite5 = Label(root, text="Item 5 : ", font="garamond 16")
ite6 = Label(root, text="Item 6 : ", font="garamond 16")
pri = Label(root, text="Price (₹)", font="corbel 16")
quan = Label(root, text="Quantity ", font="corbel 16")
amou = Label(root, text="Amount (₹)", font="corbel 16")
tot = Label(root, text="Total (₹) :", font="corbel 13")


inven = Entry(root, textvariable=invar, state=DISABLED,
              font="georgia 15", width=4)
cent = Entry(root, textvariable=cname,  font="georgia 13")
pric1 = Entry(root, textvariable=price1,  font="georgia 13",
              width=6, justify=CENTER, background="#D9FEFF")
pric2 = Entry(root, textvariable=price2,  font="georgia 13",
              width=6, justify=CENTER, background="#D9FEFF")
pric3 = Entry(root, textvariable=price3,  font="georgia 13",
              width=6, justify=CENTER, background="#D9FEFF")
pric4 = Entry(root, textvariable=price4,  font="georgia 13",
              width=6, justify=CENTER, background="#D9FEFF")
pric5 = Entry(root, textvariable=price5,  font="georgia 13",
              width=6, justify=CENTER, background="#D9FEFF")
pric6 = Entry(root, textvariable=price6,  font="georgia 13",
              width=6, justify=CENTER, background="#D9FEFF")
quant1 = Entry(root, textvariable=quantity1,  font="georgia 13",
               width=6, justify=CENTER, background="#D9FFF2")
quant2 = Entry(root, textvariable=quantity2,  font="georgia 13",
               width=6, justify=CENTER, background="#D9FFF2")
quant3 = Entry(root, textvariable=quantity3,  font="georgia 13",
               width=6, justify=CENTER, background="#D9FFF2")
quant4 = Entry(root, textvariable=quantity4,  font="georgia 13",
               width=6, justify=CENTER, background="#D9FFF2")
quant5 = Entry(root, textvariable=quantity5,  font="georgia 13",
               width=6, justify=CENTER, background="#D9FFF2")
quant6 = Entry(root, textvariable=quantity6,  font="georgia 13",
               width=6, justify=CENTER, background="#D9FFF2")
am1 = Entry(root, textvariable=amount1,  font="arial 13",
            width=7, justify=CENTER, state=DISABLED)
am2 = Entry(root, textvariable=amount2,  font="arial 13",
            width=7, justify=CENTER, state=DISABLED)
am3 = Entry(root, textvariable=amount3,  font="arial 13",
            width=7, justify=CENTER, state=DISABLED)
am4 = Entry(root, textvariable=amount4,  font="arial 13",
            width=7, justify=CENTER, state=DISABLED)
am5 = Entry(root, textvariable=amount5,  font="arial 13",
            width=7, justify=CENTER, state=DISABLED)
am6 = Entry(root, textvariable=amount6,  font="arial 13",
            width=7, justify=CENTER, state=DISABLED)
tamou = Entry(root, textvariable=totalamount, font="arial 13",
              width=8, justify=CENTER, state=DISABLED)

item1 = OptionMenu(root, i1, *item_lis)
item2 = OptionMenu(root, i2, *item_lis)
item3 = OptionMenu(root, i3, *item_lis)
item4 = OptionMenu(root, i4, *item_lis)
item5 = OptionMenu(root, i5, *item_lis)
item6 = OptionMenu(root, i6, *item_lis)
item1.config(font="helv 12 bold")
item2.config(font="helv 12 bold")
item3.config(font="helv 12 bold")
item4.config(font="helv 12 bold")
item5.config(font="helv 12 bold")
item6.config(font="helv 12 bold")

calculate = Button(root, text="Calculate", command=calculate_fun, background="#BEEDA7",
                   activebackground="#A9EDA7", width=15, height=1, font="corbel 14 bold", relief=RIDGE)
delete = Button(root, text="Reset", command=reset_fun, activebackground="#FFB0B0",
                background="#FFCDC7", width=15, height=1, font="corbel 14 bold", relief=RIDGE)
newinvo = Button(root, text="Save and Next Invoice", command=invoplus, activebackground="#FAFFC7",
                 background="#FEFFF3", width=20, font="corbel 14 bold", relief=RIDGE)

inv.place(x=10, y=1.5)
inven.place(x=150, y=5.5)
custname.place(x=10, y=100)
cent.place(x=165, y=104)
ite1.place(x=10, y=150)
ite2.place(x=10, y=200)
ite3.place(x=10, y=250)
ite4.place(x=10, y=300)
ite5.place(x=10, y=350)
ite6.place(x=10, y=400)
item1.place(x=83, y=148)
item2.place(x=83, y=198)
item3.place(x=83, y=248)
item4.place(x=83, y=298)
item5.place(x=83, y=348)
item6.place(x=83, y=398)
pri.place(x=500, y=100)
quan.place(x=650, y=100)
amou.place(x=800, y=100)
can.place(x=150, y=100)
quant1.place(x=660, y=150)
quant2.place(x=660, y=200)
quant3.place(x=660, y=250)
quant4.place(x=660, y=300)
quant5.place(x=660, y=350)
quant6.place(x=660, y=400)
pric1.place(x=505, y=150)
pric2.place(x=505, y=200)
pric3.place(x=505, y=250)
pric4.place(x=505, y=300)
pric5.place(x=505, y=350)
pric6.place(x=505, y=400)
am1.place(x=813, y=150)
am2.place(x=813, y=200)
am3.place(x=813, y=250)
am4.place(x=813, y=300)
am5.place(x=813, y=350)
am6.place(x=813, y=400)
calculate.place(x=275, y=500)
delete.place(x=490, y=500)
tot.place(x=735, y=450)
tamou.place(x=813, y=453)
newinvo.place(x=352.5, y=550)

root.mainloop()

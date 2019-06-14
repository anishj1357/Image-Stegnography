from tkinter import *
from tkinter import filedialog

from PIL import Image

def encode():
    image = Image.open(var, 'r')

    data = s_encode
    if (len(data) == 0):
        raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = o_name
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):

        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1


def genData(data):
    # list of binary codes
    # of given data
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd


def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0') and (pix[j] % 2 != 0):

                if (pix[j] % 2 != 0):
                    pix[j] -= 1

            elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                pix[j] -= 1

        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means the
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                pix[-1] -= 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def decode():
    image = Image.open(var1, 'r')

    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]
        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data


window = Tk()
window.geometry("600x600")


def closewindow():
    top = Toplevel()
    top.title("ENCODE")
    top.geometry("600x600")



    lblb = Label(top, text="Image")
    lblb.grid(row=0,column=0,padx=70,pady=30)

    elblb = Entry(top)
    elblb.grid(row=0,column=1,padx=70,pady=30)

    def mfileopen():
        file1 = filedialog.askopenfile(initialdir="/F")
        global var
        var = file1.name
        print(var)
        elblb.insert(0, file1.name)


    btnb = Button(top, text="BROWSE", fg="black",bg="grey", bd=10,command=mfileopen)
    btnb.grid(row=0, column=2, padx=20, pady=30)



    lbld = Label(top, text="Secret Message")
    lbld.grid(row=2,column=0,padx=70,pady=30)

    def returnEntry_secretmessage(elbld):
        global s_encode
        s_encode = elbld.widget.get()
        print(s_encode)

    elbld = Entry(top)
    elbld.bind("<Return>", returnEntry_secretmessage)
    elbld.grid(row=2,column=1,padx=70,pady=30)

    output_name = Label(top, text='Enter Image name with Extension:')
    output_name.grid(row=3,column=0)

    def returnEntry_outputImage(output_Entry):
        global o_name
        o_name = output_Entry.widget.get()
        print(o_name)

    output_Entry = Entry(top)
    output_Entry.bind("<Return>", returnEntry_outputImage)
    output_Entry.grid(row=3,column=1,pady=30)

    btna = Button(top, text="ENCRYPT",bg="grey", fg="black", bd=10, command=lambda: encode())
    btna.grid(row=4,column=0,pady=30)
    btna.place(relx=0.5, rely=0.5, anchor=CENTER)

    btn5 = Button(top, text="CLOSE", bg="grey", fg="black", bd=10, command=top.destroy)
    btn5.grid(row=5,column=0,padx=20,pady=30)
    btn5.place(relx=0.5, rely=0.6, anchor=CENTER)


def decwindow():
    bot = Toplevel()
    bot.title("DECODE")
    bot.geometry("600x600")

    lblf = Label(bot, text="Image")
    lblf.grid(row=0,column=0,padx=70,pady=30)
    elblf = Entry(bot)
    elblf.grid(row=0,column=1,padx=70,pady=30)

    def mfileopen():
        file2 = filedialog.askopenfile(initialdir="/F")
        global var1
        var1 = file2.name
        elblf.insert(0, file2.name)
        print(var1)

    btndec = Button(bot, text="BROWSE", fg="black",bg="grey", bd=10,command=mfileopen)
    btndec.grid(row=0,column=2,padx=10,pady=30)


    def calling_function():
        global mn
        mn = decode()
        print(mn)

    btnh = Button(bot, text="decrypt", fg="black", bd=10, bg="grey",font="bold",command=calling_function)
    btnh.grid(row=3,column=0,padx=70,pady=30)
    btnh.place(relx=0.5, rely=0.2, anchor=CENTER)

    outlbl = Label(bot, text="The decrypted secret message is:")
    outlbl.grid(row=4,column=0,pady=80)
    outlbl.place(relx=0.2, rely=0.3, anchor=CENTER)
    def funcen():
        outentlb.insert(0,mn)
    but = Button(bot,text="get text",fg="black",bg="grey", bd=10,command=funcen)
    but.grid(row=5,column=2,padx=70,pady=30)
    but.place(relx=0.7, rely=0.3, anchor=CENTER)

    outentlb = Entry(bot)
    outentlb.grid(row=5,column=1,pady=80)
    outentlb.place(relx=0.5, rely=0.3, anchor=CENTER)

    btn6 = Button(bot, text="close", bg="grey", fg="black", bd=10,command=bot.destroy)
    btn6.grid(row=6,column=0,padx=70,pady=90)
    btn6.place(relx=0.5, rely=0.4, anchor=CENTER)


def lastwindow():
    exit()


lbl1 = Label(window, text="IMAGE STEGANOGRAPHY", fg="black", bd=15, font="Times 30 bold underline")
lbl1.pack()
lbl2 = Label(window, text="Choose an option:", fg="black", bd=10, font=20)
lbl2.pack()

btn1 = Button(window, bd=10, bg="grey", text="ENCODE", fg="black", command=closewindow)
btn1.pack()
btn2 = Button(window, bd=10, bg="grey", text="DECODE", fg="black", command=decwindow)
btn2.pack()
btn3 = Button(window, bd=10, bg="grey", text="EXIT", fg="black", command=lastwindow)
btn3.pack()
window.mainloop()

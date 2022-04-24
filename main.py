# A Desktop program where you can upload images and add a watermark.

from PIL import Image, ImageTk
import tkinter as tk


# Global #
working_image = Image.new("RGBA", (100, 100))
image_open = False


# # ------------------------ WATERMARK ALPHA ------------------------------#
# Adds alpha to the watermark so that white pixels are transparent and black
# pixels are transparent.
# This was used to create the current default watermark, could be modified to
# allow custom watermark images.
def create_watermark(file_name):
    watermark = Image.open(file_name)
    rgba = watermark.convert('RGBA')
    data = rgba.getdata()
    new_data = []
    for datum in data:
        if datum[0:3] == (0, 0, 0):
            new_data.append(datum[0:3] + (50,))
        elif datum[0:3] == (255, 255, 255):
            new_data.append(datum[0:3]+(0,))
        else:
            new_data.append(datum[0:3] + (0,))
    image = Image.new("RGBA", watermark.size)
    image.putdata(new_data)
    image.save("default_watermark.png")


# # ------------------------ PLACE WATERMARK ------------------------------#
# open the watermark, set it to below half opacity
def place_watermark(watermark="default_watermark.png"):
    global working_image, p_working_image, image_open
    if image_open:
        image_to_modify = working_image
        watermark_img = Image.open(watermark)
        width, height = image_to_modify.size
        watermark_img = watermark_img.crop((0, 0, width, height))
        image_to_modify.paste(watermark_img, (0, 0), watermark_img)
        p_working_image = ImageTk.PhotoImage(image_to_modify)
        canvas.itemconfig(image, image=p_working_image)
        canvas.itemconfig(text, text="Watermark added.")
    else:
        canvas.itemconfig(text, text="Load an image to add a watermark.")


def save_image():
    global working_image, image_open, p_working_image
    if image_open:
        save_name = save_as.get()
        working_image.save(f'{save_name}.{working_image.format}', working_image.format)
        canvas.itemconfig(text, text="Image Saved")
        working_image = Image.new("RGBA", (100, 100))
        p_working_image = ImageTk.PhotoImage(working_image)
        canvas.itemconfig(image, image=p_working_image)
        file_name.delete(0, 'end')
        save_file_name.delete(0, 'end')


def open_image():
    global working_image, p_working_image, image_open
    file_name = open_this_file.get()
    try:
        working_image = Image.open(file_name)
    except (FileNotFoundError, AttributeError):
        canvas.itemconfig(text, text="No file found with that name.")
    else:
        p_working_image = ImageTk.PhotoImage(working_image)
        canvas.itemconfig(image, image=p_working_image)
        image_open = True


window = tk.Tk()
window.title("Watermarker")
window.minsize(width=220, height=220)
window.config(padx=50, pady=50)

p_working_image = ImageTk.PhotoImage(working_image)

title_label = tk.Label(text="Add Watermark")
title_label.grid(column=1, row=0)

canvas = tk.Canvas(width=600, height=400, highlightthickness=1)
myimg = ImageTk.PhotoImage(working_image)
image = canvas.create_image(0, 5, image=myimg, anchor="nw")
text = canvas.create_text(0, 5, text= "Enter an path to an image", anchor="nw")
canvas.grid(column=0, columnspan=3, row=1)

label_file_name = tk.Label(text="Enter File Name")
label_file_name.grid(column=0, row=2)

open_this_file = tk.StringVar()
file_name = tk.Entry(width=40, textvariable=open_this_file)
file_name.grid(column=1, row=2)

open_file = tk.Button(text="Open File", command=open_image)
open_file.grid(column=2, row=2, sticky="EW")

add_watermark = tk.Button(text="Add Watermark", command=place_watermark)
add_watermark.grid(column=0, columnspan=3, row=3, sticky="EW")

label_file_save = tk.Label(text="Save As")
label_file_save.grid(column=0, row=4)

save_as = tk.StringVar()
save_file_name = tk.Entry(width=40, textvariable=save_as)
save_file_name.grid(column=1, row=4)

save_button = tk.Button(text="Save", command=save_image)
save_button.grid(column=2, row=4, sticky="EW")


window.mainloop()


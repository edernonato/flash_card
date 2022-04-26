from tkinter import *
import pandas
from random import randint, choice
BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")


words_dict = data.to_dict(orient="records")
current_card = {}


def generate_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(words_dict)
    french_word = current_card["French"]
    canvas.itemconfig(cards_img, image=card_front)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_text, text=french_word, fill="black")
    flip_timer = window.after(3000, flip_card)


def wrong_button_pushed():
    generate_word()


def right_button_pushed():
    global words_dict, current_card
    words_dict.remove(current_card)
    df = pandas.DataFrame(words_dict)
    df.to_csv("data/words_to_learn.csv", index=False)
    generate_word()


def flip_card():
    global current_card
    english_word = current_card["English"]
    canvas.itemconfig(cards_img, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_text, text=english_word, fill="white")


window = Tk()
window.title("Flash Cards APP")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, border=0, bg=BACKGROUND_COLOR)
cards_img = canvas.create_image(400, 263, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)
card_title = canvas.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
card_text = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))

wrong_img = PhotoImage(file="images/wrong.png")
right_img = PhotoImage(file="images/right.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=wrong_button_pushed)
wrong_button.grid(row=1, column=0)

right_button = Button(image=right_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=right_button_pushed)
right_button.grid(row=1, column=1)

generate_word()

window.mainloop()

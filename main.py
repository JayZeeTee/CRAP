# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 11:34:47 2025
@author: Joshua Z. Tynes
"""

"""
Lasted Updated on Sun Feb 23 21:00:00 2025
@author: Joshua Z. Tynes
"""
"""
/****************************************************
Crowell Road Agricultural Products - Inventory System
Purpose: Back End System and Graphical User Interface
Intended Systems:Windows PC and RPI with touch screen
Student: Joshua Z. Tynes
Student #: B00385580
Instructor: Dr. Issam Hammad
Date: February 03, 2025
Dalhouie Unversity - Department of Engineering
Mathematics & Internetworking
/****************************************************
"""
# import csv
import cv2
# import serial
# from decimal import Decimal
# import RPi.GPIO as GPIO
# import datetime
# import time
# import threading
import numpy as np
from numpy import unique
import pandas as pd
# from time import sleep
# from guizero import App, Box, Picture, PushButton, Slider, TextBox, Window

"""
/**************************************************
Global Item Object
/**************************************************
"""


class Item:
    def __init__(self, Name, Price, Quantity):
        self.Name = Name
        self.Price = Price
        self.Quantity = Quantity


class Prod(Item):
    Type = "Veg"  # Class Attribute

    def __init__(self, Name, Price, Quantity, Type):
        super().__init__(Name, Price, Quantity)
        self.Type = Type

    def set_ID(self, ID):
        self.ID = ID


class Sold(Prod):
    Status = "Sold"  # Class Attribute

    def __init__(self, Name, Price, Quantity, Type, Status, SaleDate):
        super().__init__(Name, Price, Quantity, Type)
        self.Status = Status
        self.SaleDate = SaleDate

    def get_SaleDate(self):
        # Print message
        # Get Sale Date
        return self.SaleDate

#df = pd.read_excel("Q:\School Files\DAL\ENGM4620-Python\CRAPveg.xlsx")
#print(df)

#out = df.to_numpy().tolist()
#print(out)

file_path = r'Q:\School Files\DAL\ENGM4620-Python\CRAPveg.xlsx'
xlsx = pd.read_excel(file_path)
names = unique(xlsx.Name)
print(names)

# List of vegetable types
vegetables = names #["Beets", "Bean", "Brussel Sprouts", "Carrots", "Tomato", "Potato", "Squash"]
selected_vegetable = None
varieties = []
order = []

# Button settings
button_width = 150
button_height = 50
padding = 50

# Colours
default_colour = (200, 200, 200)
hover_colour = (200, 000, 000)


def variety_choice(selected_variety):
    print("You've chosen", selected_variety)
    order.append(selected_variety)
    print(order)

# Create buttons dynamically
def create_button(options, window_name):
    buttons = [('<- Back', (20, 20, 170, 70))]
    buttons_per_row = 4
    created = 0
    cols = 0
    for i, option in enumerate(options):
        x1, y1 = 20 + created * (button_width + padding), 100 + cols * (button_height + padding)
        x2, y2 = x1 + button_width, y1 + button_height
        buttons.append((option, (x1, y1, x2, y2)))
        if created < buttons_per_row:
            created += 1
        else:
            created = 0
            cols += 1
    return buttons


# Draw buttons on window
def draw_buttons(frame, buttons, mouse_pos):
    #print(buttons)
    for text, (x1, y1, x2, y2) in buttons:
        colour = hover_colour if (x1 < mouse_pos[0] < x2 and y1 < mouse_pos[1] < y2) else default_colour #Hover colour not working properly
        cv2.rectangle(frame, (x1, y1), (x2, y2), colour, -1)
        cv2.putText(frame, text, (x1 + 10, y1 + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (0, 0, 0), 2)
    return frame


# Check if button is clicked
def check_click(buttons, mouse_pos):
    for text, (x1, y1, x2, y2) in buttons:
        if x1 < mouse_pos[0] < x2 and y1 < mouse_pos[1] < y2:
            return text
    return None

def get_varieties():
    varieties = []
    print(xlsx)
    out = xlsx.to_numpy().tolist()
#    print(out)
#    print(len(out))
#    print(mylist)

    for i in range(len(out)):
        extracted_veg = out[i]
        if extracted_veg[1] == selected_vegetable:
            # print(extracted_veg[2])
            varieties.append(extracted_veg[2])
#    print(varieties) # For testing to ensure correct list was generated
    return varieties

def variety_selection():
    #cv2.destroyWindow("Select Vegetable")
    cv2.namedWindow(selected_vegetable)
    varieties = get_varieties()
    buttons = create_button(varieties, selected_vegetable)

    while True:
        frame = np.ones((600, 800, 3),
                        dtype=np.uint8) * 255  # creates a 400 by 300 windows with hex rgb values for each pixel
        mouse_pos = cv2.getWindowImageRect(selected_vegetable)[:2]
        #frame = draw_buttons(frame, [('<- Back', (20, 20, 170, 70))], mouse_pos)
        frame = draw_buttons(frame, buttons, mouse_pos)
        cv2.imshow(selected_vegetable, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

        if cv2.getWindowProperty(selected_vegetable, cv2.WND_PROP_VISIBLE) < 1:
            break

        def mouse_callback(event, x, y, flags, param):
            global selected_variety
            if event == cv2.EVENT_LBUTTONDOWN:
                selected = check_click(buttons, (x, y))
                if selected:
                    selected_variety = selected
                    variety_choice(selected_variety)   #add to chosen vegetables to buy
                    #cv2.destroyWindow(selected_variety)
                    # enter_varities()

        cv2.setMouseCallback(selected_vegetable, mouse_callback)
    #cv2.destroyAllWindows()

def vegetable_selection():
    global selected_vegetable
    cv2.namedWindow("Select Vegetable")
    buttons = create_button(vegetables, "Select Vegetable")

    while True:
        frame = np.ones((600, 800, 3),
                        dtype=np.uint8) * 255  # creates a 400 by 300 windows with hex rgb values for each pixel
        mouse_pos = cv2.getWindowImageRect("Select Vegetable")[:2]
        frame = draw_buttons(frame, buttons, mouse_pos)
        cv2.imshow("Select Vegetable", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

        if cv2.getWindowProperty("Select Vegetable", cv2.WND_PROP_VISIBLE) < 1:
            break

        def mouse_callback(event, x, y, flags, param):
            global selected_vegetable
            if event == cv2.EVENT_LBUTTONDOWN:
                selected = check_click(buttons, (x, y))
                if selected:
                    selected_vegetable = selected
                    variety_selection()# Create veg window
                    #cv2.createButton('ButtonBeans', )  # add callback function after name
                    #cv2.createButton('ButtonCarrots', )
                    #cv2.destroyWindow("Select Vegetable")
                    # enter_varities()

        cv2.setMouseCallback("Select Vegetable", mouse_callback)
    #cv2.destroyAllWindows()

"""
def enter_varieties():
    global varieties
    cv2.namedWindow("Enter Varieties")
    text_input = ""

    while True:
        frame = np.ones((600, 800, 3), dtype=np.uint8) * 255
        cv2.putText(frame, f"Varieties of {selected_vegetable}:", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.putText(frame, text_input, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.putText(frame, "Press Enter to Save", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.imshow("Enter Varieties", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        elif key == 13:
            varieties.append(text_input)
            text_input = ""
        elif key == 8:
            text_input = text_input[:-1]
        elif 32 <= key <= 126:
            text_input += chr(key)

    #cv2.destroyAllWindows()
"""

if __name__ == "__main__":
    vegetable_selection()

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


file_path = r'./CRAPveg.xlsx'
xlsx = pd.read_excel(file_path)
names = unique(xlsx.Name)
#print(names)

# List of vegetable types
vegetables = names
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
    #print("You've chosen", selected_variety)
    order.append(selected_variety)
    #print(order)

# Create buttons dynamically
def create_button(options, window_name):
    buttons = []#[('<- Back', (20, 20, 170, 70)),('$ Checkout', (620, 20, 770, 70))]
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
#    print(xlsx)
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
    variety_buttons = [('<- Back', (20, 20, 170, 70)),('$ Checkout', (620, 20, 770, 70))]
    buttons = create_button(varieties, selected_vegetable)

    while True:
        frame = np.ones((600, 800, 3),
                        dtype=np.uint8) * 255  # creates a 400 by 300 windows with hex rgb values for each pixel
        mouse_pos = cv2.getWindowImageRect(selected_vegetable)[:2]
        frame = draw_buttons(frame, buttons+variety_buttons, mouse_pos)
        cv2.imshow(selected_vegetable, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

        if cv2.getWindowProperty(selected_vegetable, cv2.WND_PROP_VISIBLE) < 1:
            break

        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                selected = check_click(buttons, (x, y))
                back = check_click([('<- Back', (20, 20, 170, 70))], (x, y))
                checkout = check_click([('$ Checkout', (620, 20, 770, 70))], (x, y))
                if selected:
                    selected_variety = selected
                    variety_choice(selected_variety)   #add to chosen vegetables to buy
                    #cv2.destroyWindow(selected_variety)
                    # enter_varities()
                elif back:
                    cv2.destroyWindow(selected_vegetable)
                elif checkout:
                    print("Checkout")
                    print("You have chosen to purchase the following vegetables: ", order)

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
        frame = draw_buttons(frame, buttons+[('$ Checkout', (620, 20, 770, 70))], mouse_pos)
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
                checkout = check_click([('$ Checkout', (620, 20, 770, 70))], (x, y))
                if selected:
                    selected_vegetable = selected
                    variety_selection()# Create veg window
                elif checkout:
                    print("Checkout")
                    print("You have chosen to purchase the following vegetables: ", order)
                    #cv2.destroyWindow("Select Vegetable")

        cv2.setMouseCallback("Select Vegetable", mouse_callback)
    #cv2.destroyAllWindows()

def sales_terminal():
    print("The C.R.A.P. Sales Terminal will now be launched")
    print("Users may now select the vegetables they would like to purchase")
    vegetable_selection()

def admin_mode():
    print("The C.R.A.P. Administration Menu will now be launched")
    admin_menu()

def display_inventory():
    print("The following items are currently in stock:")
    print(xlsx)


def update_inventory():
    global xlsx
    print("The following items are currently in stock:")
    print(xlsx)
    #selected_vegetable = input("Enter the number of the vegetable you would like to update: ")

    try:
        selected_index = int(input("Enter the row number of the vegetable you would like to update: "))
        if selected_index < 0 or selected_index >= len(xlsx):
            print("Invalid row number. Please try again.")
            return

        selected_row = xlsx.iloc[selected_index]
        print(
            f"\nYou selected: {selected_row['Name']} - {selected_row['Variety']} (Current Quantity: {selected_row['Quantity']})")

        new_quantity = int(input("Enter the new quantity of the selected item: "))
        if new_quantity < 0:
            new_quantity = 0

        xlsx.at[selected_index, 'Quantity'] = new_quantity
        xlsx.to_excel(file_path, index=False)
        print(f"Quantity updated successfully. New quantity: {new_quantity}")
        print(xlsx)

    except ValueError:
        print("Invalid input. Please try again.")


def add_new_item():
    global xlsx
    print("Please enter the details of the new item you would like to add:")
    name = input("What type of vegetable is the new item: ")
    variety = input("Enter the variety of the new item: ")

    try:
        price_input = input("Enter the price of the item: ")
        quantity_input = input("Enter the quantity of the item: ")

        price = float(price_input)
        quantity = int(quantity_input)

        if quantity < 0:
            quantity = 0

        new_data = pd.DataFrame([["Veg", name, variety, "", quantity, price]], columns=xlsx.columns)
        xlsx = pd.concat([xlsx, new_data], ignore_index=True)
        xlsx.to_excel(file_path, index=False)
        print("Item added successfully!")
        print(xlsx)
    except ValueError as e:
        print(f"Invalid input: {e}. Please enter numerical values for price and quantity.")

def admin_menu():
    print("1. See Inventory")
    print("2. Update Inventory")
    print("3. Add New Item")
    print("4. Return to Main Menu")
    choice = input("Enter your choice: ")
    if choice == "1":
        display_inventory()
    elif choice == "2":
        update_inventory()
    elif choice == "3":
        add_new_item()
    elif choice == "4":
        main_menu()
    else:
        print("Invalid choice. Please try again.")
        admin_menu()

def welcome():
    print("Welcome to C.R.A.P. program")
    print("Please select from the following options: ")
    main_menu()

def main_menu():
    while True:
        print("Please select from the following options: ")
        print("1. Enter Administration Menu")
        print("2. Launch Sales")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            admin_mode()
        elif choice == "2":
            sales_terminal()
        elif choice == "3":
            exit()
        else:
            print("Invalid choice. Please try again.")
            main_menu()

def crap():
    welcome()

if __name__ == "__main__":
    crap()

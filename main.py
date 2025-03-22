import customtkinter as ctk
import pyperclip
import requests
import matplotlib.pyplot as plt
from tkinter import StringVar, ttk

# Initialize window
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Advanced Unit & Currency Converter")
app.geometry("750x600")

# Fonts
FONT_LARGE = ("Poppins", 16, "bold")
FONT_MEDIUM = ("Roboto", 14)

# Unit categories & conversion formulas
unit_categories = {
    "Length": ["Meter", "Kilometer", "Mile", "Yard", "Foot"],
    "Weight": ["Gram", "Kilogram", "Pound", "Ounce"],
    "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "Currency": ["USD", "INR", "EUR", "GBP", "JPY", "CAD", "AUD", "CNY"]
}

conversion_factors = {
    "Meter": {"Kilometer": 0.001, "Mile": 0.000621371, "Yard": 1.09361, "Foot": 3.28084},
    "Kilometer": {"Meter": 1000, "Mile": 0.621371, "Yard": 1093.61, "Foot": 3280.84},
    "Celsius": {"Fahrenheit": lambda c: (c * 9/5) + 32, "Kelvin": lambda c: c + 273.15}
}

# Function to fetch live exchange rates
def get_currency_rate(from_currency, to_currency):
    API_KEY = "YOUR_API_KEY_HERE"
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and "conversion_rates" in data:
            return data["conversion_rates"].get(to_currency, None)
        else:
            return None
    except:
        return None

# Function to update dropdowns when category changes
def update_units(event=None):
    selected_category = category_var.get()
    from_unit_dropdown["values"] = unit_categories[selected_category]
    to_unit_dropdown["values"] = unit_categories[selected_category]
    from_unit_var.set(unit_categories[selected_category][0])
    to_unit_var.set(unit_categories[selected_category][1])

# Function to convert values
def convert():
    try:
        value = float(entry_value.get())
        from_unit = from_unit_var.get()
        to_unit = to_unit_var.get()

        if from_unit == to_unit:
            result_var.set(f"{value} {from_unit} = {value} {to_unit}")
            return

        if from_unit in unit_categories["Currency"] and to_unit in unit_categories["Currency"]:
            rate = get_currency_rate(from_unit, to_unit)
            if rate:
                result = value * rate
                result_var.set(f"{value} {from_unit} = {round(result, 2)} {to_unit}")
            else:
                result_var.set("Exchange rate unavailable!")
            return

        if from_unit in conversion_factors and to_unit in conversion_factors[from_unit]:
            if callable(conversion_factors[from_unit][to_unit]):
                result = conversion_factors[from_unit][to_unit](value)
            else:
                result = value * conversion_factors[from_unit][to_unit]
            result_var.set(f"{value} {from_unit} = {round(result, 4)} {to_unit}")
        else:
            result_var.set("Conversion not available!")

    except ValueError:
        result_var.set("Invalid input!")

# UI Layout
frame = ctk.CTkFrame(app)
frame.pack(pady=20, padx=10, fill="both", expand=True)

category_var = StringVar(value="Length")
category_dropdown = ttk.Combobox(frame, textvariable=category_var, values=list(unit_categories.keys()), font=FONT_MEDIUM)
category_dropdown.grid(row=0, column=0, padx=10, pady=10)
category_dropdown.bind("<<ComboboxSelected>>", update_units)

entry_value = StringVar()
entry = ctk.CTkEntry(frame, textvariable=entry_value, width=140, font=FONT_MEDIUM)
entry.grid(row=0, column=1, padx=10, pady=10)

from_unit_var = StringVar()
to_unit_var = StringVar()

from_unit_dropdown = ttk.Combobox(frame, textvariable=from_unit_var, font=FONT_MEDIUM)
from_unit_dropdown.grid(row=0, column=2, padx=10, pady=10)

to_unit_dropdown = ttk.Combobox(frame, textvariable=to_unit_var, font=FONT_MEDIUM)
to_unit_dropdown.grid(row=0, column=3, padx=10, pady=10)

convert_button = ctk.CTkButton(frame, text="Convert", command=convert)
convert_button.grid(row=0, column=4, padx=10, pady=10)

result_var = StringVar()
result_label = ctk.CTkLabel(frame, textvariable=result_var, font=FONT_LARGE)
result_label.grid(row=1, column=0, columnspan=5, pady=10)

update_units()
app.mainloop()

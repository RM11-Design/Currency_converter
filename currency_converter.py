from tkinter import *
from tkinter import messagebox
import requests
from PIL import Image, ImageTk # for importing images/logo

class App(Tk):
    def __init__(self):
        super().__init__()

        font1 = 'aspira-regular'
        colour1 = "#25283D" # dark blue
        colour2 = "#383D5D" # little lighter dark blue
        colour3 = "#19535F"

        self.title("Currency converter")
        self.geometry("650x490")

        self.resizable(False, False)

        self.configure(bg=colour1)

        
        # Main title

        main_title = Label(text="Currency Converter",
                           font=(font1, 20),
                           bg=colour1,
                           fg="white")
        main_title.place(relx=0.34,rely=0.045)


        self.canvas = Canvas(self,
                             width=500,
                             height=350,
                             highlightthickness=0,
                             bg=colour2)
        self.canvas.place(relx=0.11, rely=0.15)

        # Logo

        logo_image = Image.open("exchange white.png")
        resize_image = logo_image.resize((35,35))  # Resizing the image
        img = ImageTk.PhotoImage(resize_image)

        logo = Label(image=img,
                    bg=colour1)
        logo.image = img
        logo.place(relx=0.27,rely=0.04)


        # Amount entry
        self.canvas.create_text(45, 75, # x and y co-ordinates
                                text="Amount",
                                font=(font1, 12),
                                fill="white")
        
        self.canvas.create_text(250, 40, # x and y co-ordinates
                                text="Enter an amount",
                                font=(font1, 17),
                                fill="white")

        self.amount = Entry(self,
                             font=(font1, 15),
                             width=20,
                             bg=colour1,
                             fg="white")
        self.canvas.create_window(130,100,
                                  window=self.amount)

        # Currency selection OptionMenus
        currency = ["USD", "EUR", "GBP", "JPY"]
        self.selected_currency1 = StringVar(value=currency[0])
        self.selected_currency2 = StringVar(value=currency[0])

        self.currency1 = OptionMenu(self.canvas,
                                    self.selected_currency1,
                                    *currency)
        self.currency1.config(font=(font1, 14),
                              bg=colour1,
                              fg="white",
                              highlightthickness=0)
        self.currency1_window = self.canvas.create_window(310, 100,
                                                          window=self.currency1)

        self.currency2 = OptionMenu(self.canvas,
                                    self.selected_currency2,
                                    *currency)
        self.currency2.config(font=(font1, 14), 
                              bg=colour1,
                              fg="white",
                              highlightthickness=0)
        self.currency2_window = self.canvas.create_window(430, 100,
                                                          window=self.currency2)

        # Calculate button
        self.calculate_button = Button(self.canvas,
                                       text="Calculate",
                                       font=(font1, 15),
                                       bg=colour3,
                                       fg="white",
                                       border=0,
                                       height=1,
                                       width=10,  # Button text color
                                       command=self.calculate)  # Command to execute when clicked
        self.calculate_button_window = self.canvas.create_window(255, 170,
                                                                 window=self.calculate_button)

        # Result label
        self.result_label = Label(self.canvas, 
                                  text="", 
                                  font=(font1, 19), 
                                  bg=colour2, 
                                  fg="white")
        self.result_label_window = self.canvas.create_window(255, 230, window=self.result_label)

    def calculate(self):
        amount = self.amount.get()

        # Checks if the entered amount is not a number. If it's not a number, it shows an error message and exits the method.
        if not amount.isdigit():
            messagebox.showerror("Error", "Please enter a valid amount.")
            return
        # Converts number into decimal-point number.
        amount = float(amount)
        from_currency = self.selected_currency1.get()
        to_currency = self.selected_currency2.get()

        # Sends a request to the Frankfurter API to get the latest currency conversion rate for the specified amount from from_currency to to_currency. The response from the API is stored in the variable response.
        response = requests.get(f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}")

        # Converts the API response from JSON format into python dictionary, stores it in a variable called "data". It looks inside the rates section of the dictionary to find the value for to_currency and stores it in converted_amount.
        data = response.json()

        # Retrieves converted amount from the "data" dictonary that we made. 
        converted_amount = data["rates"][to_currency]

        # updates the text of the result_label to display the original amount and currency, and the converted amount and currency, in a readable format.
        self.result_label.config(text=f"{amount} {from_currency} = {converted_amount} {to_currency}")

if __name__ == "__main__":
    app = App()
    app.mainloop()

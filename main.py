import smtplib
import datetime as dt
import pandas as pd
import os
import random

LETTERS_PATH = "./letter_templates"

MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("MY_PASSWORD")

def get_list_of_files():
    return os.listdir(LETTERS_PATH)

def get_random_letter():
    list_of_letters = get_list_of_files()
    letter_name = random.choice(list_of_letters)
    with open(f"{LETTERS_PATH}/{letter_name}", mode="r") as file:
        file_content = file.read()
    return file_content

def prepare_message(name):
    letter = get_random_letter()
    letter = letter.replace("[NAME]", name)
    return letter

# Get the birthdays data
birthdays_df = pd.read_csv("birthdays.csv")
birthdays_dict = {(row.month, row.day) : row for index, row in birthdays_df.iterrows()}

# Check if today matches a birthday in the birthdays.csv
now = dt.datetime.now()
today = (now.month, now.day)
if today in birthdays_dict:

    # Get the jubilarian data and prepare the message
    jubilarian_address = birthdays_dict[today].email
    jubilarian_name = birthdays_dict[today]["name"]
    message = prepare_message(jubilarian_name)

    # Send the email
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=jubilarian_address, msg=f"Subject:Happy Birthday!\n\n{message}")





from datetime import datetime
import pandas as pd
import random
import smtplib
import os

MY_EMAIL = "YOUR EMAIL"
PASSWORD = "YOUR PASSWORD"

today = datetime.now()
today_tuple = (today.month, today.day)

try:
    data = pd.read_csv("birthdays.csv")
except FileNotFoundError:
    print("The birthdays.csv file was not found.")
    data = pd.DataFrame(columns=["name", "email", "year", "month", "day"])

birthday_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}

if today_tuple in birthday_dict:
    birthday_person = birthday_dict[today_tuple]
    file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"

    try:
        with open(file_path) as letter_file:
            contents = letter_file.read()
            new_content = contents.replace("NAME", birthday_person['name'])
    except FileNotFoundError:
        print(f"The letter template {file_path} was not found.")
        new_content = "Happy Birthday!"

    try:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=birthday_person["email"],
                msg=f"Subject:Happy Birthday!\n\n{new_content}"
            )
            print(f"Birthday email sent to {birthday_person['name']} at {birthday_person['email']}.")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")
else:
    print("No birthdays today.")

import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 32.650879 # Your latitude
MY_LONG = -85.377968 # Your longitude
my_email = "rehabviking@gmail.com"
password = "fspswohpgrxymdix"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

# Your position is within +5 or -5 degrees of the ISS position.


def can_be_seen():

    if abs(iss_latitude - MY_LAT) < 5 and abs(iss_longitude - MY_LONG) < 5:
        return True


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()


def is_dark():

    if time_now.hour > sunset or time_now.hour < sunrise:
        return True


while True:
    time.sleep(60)
    if can_be_seen() and is_dark():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs="vpoole21@icloud.com", msg=f"Subject:ISS\n\nLook up!")
            connection.close()






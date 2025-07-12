import requests
import geocoder
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
API_KEY = "a5ccec85eb6bd16f843b476fcb77e34d"
API_URL = "https://api.openweathermap.org/data/2.5/weather"
def convert_temp(kelvin, unit):
    if unit == "C":
        return round(kelvin - 273.15, 2)
    elif unit == "F":
        return round((kelvin - 273.15) * 9 / 5 + 32, 2)

def get_weather_by_location(location):
    params = {"appid": API_KEY}
    params["zip" if location.isdigit() else "q"] = location
    return requests.get(API_URL, params=params).json()

def get_weather_by_coordinates(lat, lon):
    return requests.get(API_URL, params={"lat": lat, "lon": lon, "appid": API_KEY}).json()

def fetch_weather(auto_detect=False):
    if auto_detect:
        g = geocoder.ip("me")
        if not g.ok:
            messagebox.showerror("Error", "Location detection failed.")
            return
        data = get_weather_by_coordinates(*g.latlng)
    else:
        location = city_entry.get().strip()
        if not location:
            messagebox.showwarning("Input Error", "Enter city name or ZIP code.")
            return
        data = get_weather_by_location(location)

    if data.get("cod") != 200:
        messagebox.showerror("API Error", data.get("message", "Unknown error"))
        return

    weather = data["weather"][0]
    main = data["main"]
    wind = data["wind"]
    icon_code = weather["icon"]
    temp = convert_temp(main["temp"], unit_var.get())

    result_label.config(
        text=(
            f"Location: {data['name']}, {data['sys']['country']}\n"
            f"Temperature: {temp} °{unit_var.get()}\n"
            f"Condition: {weather['description'].capitalize()}\n"
            f"Humidity: {main['humidity']}%\n"
            f"Wind Speed: {wind['speed']} m/s"
        )
    )

    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    img_data = requests.get(icon_url).content
    icon_tk = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
    icon_label.config(image=icon_tk)
    icon_label.image = icon_tk
app = tk.Tk()
app.title("🌦 Combined Weather App")
app.geometry("440x540")
app.configure(bg="#e3f2fd")

tk.Label(app, text="Weather Info", font=("Arial", 18, "bold"), bg="#e3f2fd").pack(pady=10)

tk.Label(app, text="Enter City or ZIP Code:", font=("Arial", 12), bg="#e3f2fd").pack()
city_entry = tk.Entry(app, font=("Arial", 14), width=30)
city_entry.pack(pady=5)

unit_var = tk.StringVar(value="C")
tk.Radiobutton(app, text="Celsius (°C)",  variable=unit_var, value="C", bg="#e3f2fd").pack()
tk.Radiobutton(app, text="Fahrenheit (°F)", variable=unit_var, value="F", bg="#e3f2fd").pack()

tk.Button(app, text="Get Weather", font=("Arial", 12), bg="#1e88e5", fg="white",
          command=lambda: fetch_weather(auto_detect=False)).pack(pady=8)

tk.Button(app, text="Auto Detect Location 🌐", font=("Arial", 12), bg="#43a047", fg="white",
          command=lambda: fetch_weather(auto_detect=True)).pack()

icon_label = tk.Label(app, bg="#e3f2fd")
icon_label.pack()

result_label = tk.Label(app, text="", font=("Arial", 12), bg="#e3f2fd", justify="left")
result_label.pack(pady=10)

app.mainloop()

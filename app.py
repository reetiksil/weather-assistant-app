import customtkinter as ctk
from weather_api import get_weather
import threading
import asyncio
import edge_tts
import os
import pygame

app=ctk.CTk()
app.title("Voice Weather Assistant")
app.geometry("600x500")
app.resizable(False,False)
current_sound= None

pygame.mixer.init()

async def voice_generator(text):
    com=edge_tts.Communicate(text, voice="en-US-AriaNeural")
    await com.save("weather.mp3")

def search():
    city = city_entry.get()
    location_label.configure(text=city)
    temp_label.configure(text="Fetching Temperature")
    condition_label.configure(text="Fetching Condition")
    details_label.configure(text="Fetching Humidity & Cloud cover")

    search_button.configure(state="disabled")
    thread=threading.Thread(target=fetch_weather, args=(city,))
    thread.start()

def fetch_weather(city):
    global current_sound
    result= get_weather(city)
    if result["success"]:

        tempc = result["temp_c"]
        tempf= result["temp_f"]
        humidity = result["humidity"]
        cloud = result["cloud"]
        condition = result["description"]
        condition_lower = condition.lower()

        if condition_lower == "clear":
            spoken_condition = "clear skies"
        elif condition_lower=="sunny":
            spoken_condition="a sunny day"
        
        elif condition_lower == "partly cloudy":
            spoken_condition = "partly cloudy skies"
        else:
            spoken_condition = condition_lower

        speech_text = (
        f"Here is the latest weather update for {city}. "
        f"It is currently {tempc} degrees Celsius or {tempf} degrees fahrenheit with {spoken_condition}. "
        f"The humidity is around {humidity} percent, "
        f"and cloud cover is about {cloud} percent."
        )

        asyncio.run(voice_generator(speech_text))


        if current_sound and pygame.mixer.get_busy():
            pygame.mixer.stop()

        current_sound = pygame.mixer.Sound("weather.mp3")
        current_sound.play()
        app.after(0,update_result,city, tempc, tempf, condition, humidity, cloud)
    else:
        display_text = result["message"]
        speech_text = (
        "I'm sorry, I couldn't retrieve the weather information. "
        "Please check your internet connection or try again."
    )
        asyncio.run(voice_generator(speech_text))


        if current_sound and pygame.mixer.get_busy():
            pygame.mixer.stop()

        current_sound = pygame.mixer.Sound("weather.mp3")
        current_sound.play()
        

        app.after(0,
            update_result_error,
            result["message"])

def update_result(city, tempc,tempf, conditon, humidity,cloud):
    location_label.configure(text=city)
    temp_label.configure(text=f"{tempc}°C/{tempf}°F")
    condition_label.configure(text=conditon)
    details_label.configure(text=f"Humidity: {humidity}% Cloud cover: {cloud}%")
    search_button.configure(state="normal")

def update_result_error(message):
    location_label.configure(text="Error")
    temp_label.configure(text="---")
    condition_label.configure(text=message)
    details_label.configure(text="")
    search_button.configure(state="normal")
   
   

title_label=ctk.CTkLabel(app, 
                         text="Weather Assistant", 
                         font=ctk.CTkFont(size=24, weight="bold"))
title_label.pack(pady=20)

input_frame=ctk.CTkFrame(app)
input_frame.pack(pady=20)

city_entry=ctk.CTkEntry(input_frame, placeholder_text="Enter the location(city,country): " )
city_entry.pack(side="left", padx=10)

search_button=ctk.CTkButton(input_frame, text="Search",command=search )
search_button.pack(side="left", padx=10)

result_frame=ctk.CTkFrame(app)
result_frame.pack(pady=20, fill="both", expand=True)

location_label=ctk.CTkLabel(result_frame, text="City" ,font=ctk.CTkFont(size=24, weight="bold"))
location_label.pack(pady=10)

temp_label=ctk.CTkLabel(result_frame, text="Temp" ,font=ctk.CTkFont(size=55, weight="bold"))
temp_label.pack(pady=10)

condition_label=ctk.CTkLabel(result_frame, text="Condition" ,font=ctk.CTkFont(size=24))
condition_label.pack(pady=3)

details_label=ctk.CTkLabel(result_frame, text="Description" ,font=ctk.CTkFont(size=22))
details_label.pack(pady=3)


app.mainloop()

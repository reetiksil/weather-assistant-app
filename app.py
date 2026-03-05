import customtkinter as ctk
from weather_api import get_weather
import threading
import asyncio
import edge_tts
import os
import pygame
from PIL import Image
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("550x750")
app.title("Weather Assistant")
app.resizable(False,False)

current_sound= None
voice_enabled=True
selected_voice="te-IN-ShrutiNeural"
preview_text="Hello! This is how I will sound in your weather updates."
voice_packs = {
    "Neerja(IN-Female)": "en-IN-NeerjaNeural",
    "Prabhat(IN-Male)": "en-IN-PrabhatNeural",
    "Aria(US-Female)": "en-US-AriaNeural",
    "Libby(UK-Female)": "en-GB-LibbyNeural"
    }
tts_rate="+0%"
speed_rates = {
    "Slow": "-10%",
    "Normal": "+0%",
    "Fast": "+25%",
    "Faster": "+30%"
}
settings_panel=None
loading_animation_running = False
loading_dots = 0
# loading icons
logo_icon=ctk.CTkImage(
    light_image=Image.open("assets/icons/weather.png"),
    dark_image=Image.open("assets/icons/weather2.png"),
    size=(170,170)
)
loading_icon=ctk.CTkImage(
    light_image=Image.open("assets/icons/loading.png"),
    dark_image=Image.open("assets/icons/loading.png"),
    size=(70,70)
)
clear_icon=ctk.CTkImage(
    light_image=Image.open("assets/icons/clear.png"),
    dark_image=Image.open("assets/icons/clear.png"),
    size=(100,100)
)
rain_icon=ctk.CTkImage(
    light_image=Image.open("assets/icons/rain.png"),
    dark_image=Image.open("assets/icons/rain.png"),
    size=(100,100)
)
lightrain_icon=ctk.CTkImage(
    light_image=Image.open("assets/icons/lightrain.png"),
    dark_image=Image.open("assets/icons/lightrain.png"),
    size=(100,100)
)
thunder_icon=ctk.CTkImage(
    light_image=Image.open("assets/icons/thunder.png"),
    dark_image=Image.open("assets/icons/thunder.png"),
    size=(100,100)
)
mist_icon=ctk.CTkImage(
    light_image=Image.open("assets/icons/mist.png"),
    dark_image=Image.open("assets/icons/mist.png"),
    size=(100,100)
    )
cloudy_icon=ctk.CTkImage(
    light_image=Image.open("assets/icons/cloudy.png"),
    dark_image=Image.open("assets/icons/cloudy.png"),
    size=(100,100)
    )
snow_icon=ctk.CTkImage(
    light_image=Image.open("assets/icons/snow.png"),
    dark_image=Image.open("assets/icons/snow.png"),
    size=(100,100)
)
search_icon=ctk.CTkImage(
    light_image=Image.open("assets/icons/search.png"),
    dark_image=Image.open("assets/icons/search.png"),
    size=(25,25)
)
mic_icon=ctk.CTkImage(
    light_image=Image.open("assets/icons/mic2.png"),
    dark_image=Image.open("assets/icons/mic2.png"),
    size=(30,30)
)
settings_icon=ctk.CTkImage(
    light_image=Image.open("assets/icons/settings.png"),
    dark_image=Image.open("assets/icons/settings2.png"),
    size=(30,30)
)
pygame.mixer.init()

async def voice_generator(text, voice, filename="weather.mp3"):
    com = edge_tts.Communicate(text, voice=voice, rate=tts_rate)
    await com.save(filename)

def preview_voice(voice):
    try:
        asyncio.run(voice_generator(preview_text, voice, "preview.mp3"))

        if os.path.exists("preview.mp3"):
            pygame.mixer.stop()
            preview_sound = pygame.mixer.Sound("preview.mp3")
            preview_sound.play()

    except Exception as e:
        print("Voice preview failed:", e)

def open_settings():

    global settings_panel

    # toggle behavior
    if settings_panel and settings_panel.winfo_exists():
        settings_panel.destroy()
        settings_panel = None
        return

    settings_panel = ctk.CTkFrame(
        app,
        width=180,
        height=170,
        corner_radius=20,
        fg_color="#1f1f1f",
        border_width=1,
        border_color="#2f2f2f"
    )
    
    # position near the gear icon
    settings_panel.place(x=20, y=70)
    settings_panel.pack_propagate(False)
    settings_panel.grab_set() 
    # close button
    close_button = ctk.CTkButton(
        settings_panel,
        text="✕",
        width=26,
        height=26,
        corner_radius=13,
        fg_color="transparent",
        hover_color="#333333",
        command=settings_panel.destroy
    )
    close_button.place(relx=1.0, x=-8, y=8, anchor="ne")

    # title
    title = ctk.CTkLabel(
        settings_panel,
        text="Settings",
        font=ctk.CTkFont(size=14, weight="bold")
    )
    title.pack(pady=(5, 5))

    # toggle
    def voice_toggle():
        global voice_enabled
        voice_enabled = voice_switch.get()

    voice_switch = ctk.CTkSwitch(
        settings_panel,
        text="Enable Voice",
        command=voice_toggle
    )
    voice_switch.pack(pady=5)

    if voice_enabled:
        voice_switch.select()
    else:
        voice_switch.deselect()


    def change_voice(choice):
        global selected_voice

        selected_voice = voice_packs[choice]

        threading.Thread(
            target=preview_voice,
            args=(selected_voice,),
            daemon=True
        ).start()

    voice_menu = ctk.CTkOptionMenu(
    settings_panel,
    values=list(voice_packs.keys()),
    command=change_voice
    )

    voice_menu.pack(pady=(0,10))
    voice_menu.set("Select Voice Pack")

        
    def change_speed(choice):
        global tts_rate
        tts_rate = speed_rates[choice]
        
    speech_speed = ctk.CTkOptionMenu(
    settings_panel,
    values=list(speed_rates.keys()),
    command=change_speed
    )

    speech_speed.pack()
    speech_speed.set("Normal")
   

def search():
    if current_sound and pygame.mixer.get_busy():
        pygame.mixer.stop()
    city = city_entry.get()
    app_title.configure(text=f"Weather report for {city.title()} is: ".replace(",", ", "),font=ctk.CTkFont(size=15, weight="normal"),text_color="#9D9A9A" )
    temp_label.configure(text="", image=loading_icon)
    Wlcm2_label.configure(text="")
    Wlcm_label.configure(text="")
    Wlcm2_label.pack(pady=(0,70))
    logo_label.configure(image=loading_icon)
    logo_label.pack(pady=(0,30))
    icon_label.configure(image="")
    global loading_animation_running, loading_dots

    loading_animation_running = True
    loading_dots = 0
    animate_loading_text()
    details_label.configure(text="")
    search_button.configure(state="disabled")
    
    thread=threading.Thread(target=fetch_weather, args=(city,))

    thread.start()

def animate_loading_text():
    global loading_dots

    if not loading_animation_running:
        return

    dots = "." * (loading_dots % 4) 
    condition_label.configure(text=f" Fetching Details{dots}", font=ctk.CTkFont(size=33, weight="bold"))
    Wlcm2_label.configure(text=f" Fetching Details{dots}", font=ctk.CTkFont(size=33, weight="bold"))

    loading_dots += 1

    app.after(400, animate_loading_text) 

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

        #selecting icons
        
        condition = result["description"].lower()

        if "thunder" in condition:
            selected_icon = thunder_icon

        elif "light rain" in condition:
            selected_icon = lightrain_icon

        elif "rain" in condition:
            selected_icon = rain_icon

        elif "cloud" in condition:
            selected_icon = cloudy_icon

        elif "clear" in condition or "sunny" in condition:
            selected_icon = clear_icon

        elif "mist" in condition:
            selected_icon = mist_icon

        elif "snow" in condition:
            selected_icon = snow_icon

        else:
            selected_icon = cloudy_icon

        #selecting proper announcement words

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

       
        if voice_enabled:
            try:
                asyncio.run(voice_generator(speech_text))
            except Exception as e:
                print("TTS generation failed:", e)
                return

            # Only play if file exists
            if os.path.exists("weather.mp3"):
                try:
                    if current_sound and pygame.mixer.get_busy():
                        pygame.mixer.stop()

                    current_sound = pygame.mixer.Sound("weather.mp3")
                    current_sound.play()
                except Exception as e:
                    print("Audio playback failed:", e)
            else:
                print("weather.mp3 was not created.")



        app.after(0,update_result,city, tempc, tempf, condition, humidity, cloud, selected_icon)
    else:
        message = result["message"]

        if "Network error" not in message:
            speech_text = (
                "I'm sorry, I couldn't retrieve the weather information. "
                "Please try again."
            )
            asyncio.run(voice_generator(speech_text))

            if current_sound and pygame.mixer.get_busy():
                pygame.mixer.stop()

            current_sound = pygame.mixer.Sound("weather.mp3")
            current_sound.play()

        app.after(0, update_result_error, message)
def update_result(city, tempc, tempf, condition, humidity, cloud, icon):
    global loading_animation_running
    loading_animation_running = False
    temp_label.configure(image="") 
    
    landing_frame.pack_forget()
    weather_frame.pack()
    app_title.configure(text=f"Weather report for {city.title()} is: ".replace(",", ", "),font=ctk.CTkFont(size=15, weight="normal"),text_color="#9D9A9A" )

    icon_label.configure(image=icon)
    temp_label.configure(text=f" {round(tempc)}°")
    condition_label.configure(text=condition.title(),font=ctk.CTkFont(size=18))
    details_label.configure(
        text=f"Humidity {humidity}%   •   Cloud {cloud}%"
    )

    search_button.configure(state="normal")
def update_result_error(message):
    temp_label.configure(text="---")
    condition_label.configure(text=message, font=ctk.CTkFont(size=15))
    details_label.configure(text="")
    search_button.configure(state="normal")


   
top_frame = ctk.CTkFrame(app,height=50, fg_color="transparent")
top_frame.pack(fill="x", pady=(0, 0), padx=15)
left_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
left_frame.pack(side="left", anchor="ne")

settings_btn=ctk.CTkButton(left_frame,text="", image=settings_icon,corner_radius=25, width=20, height=20, fg_color="transparent", hover_color="#2a2a2a", command=open_settings)
settings_btn.pack(pady=20,padx=(0,0))

center_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
center_frame.pack(expand=True,fill="x", padx=(0,50))

date_label = ctk.CTkLabel(
    center_frame,
    text=datetime.now().strftime("%A, %d %B"),
    font=ctk.CTkFont(size=13),
    text_color="#777777"
)
date_label.pack(pady=(2, 0))

time_label = ctk.CTkLabel(
    center_frame,
    text=datetime.now().strftime("%I:%M %p"),
    font=ctk.CTkFont(size=40, weight="bold"),  # 40–50 size
    text_color="#e5e5e5"
)
time_label.pack(pady=(5, 0))


app_title = ctk.CTkLabel(
    center_frame,
    text="Welcome!",
    font=ctk.CTkFont(size=22, weight="bold")
)
app_title.pack()



weather_card = ctk.CTkFrame(app, corner_radius=24, fg_color="#2a2a2a")
weather_card.pack(padx=25, pady=(10, 15), fill="both", expand=True)
weather_card.pack_propagate(False)


content_frame = ctk.CTkFrame(weather_card, fg_color="transparent")
content_frame.place(relx=0.5, rely=0.5, anchor="center")


landing_frame = ctk.CTkFrame(content_frame, fg_color="transparent")

Wlcm_label = ctk.CTkLabel(
    landing_frame,
    text="Search for a city to view weather...",
    font=ctk.CTkFont(size=15),
    text_color="#888888"
)
Wlcm_label.pack(pady=(0, 50))

logo_label = ctk.CTkLabel(
    landing_frame,
    image=logo_icon,
    text=""
)
logo_label.pack(pady=(0, 60))

Wlcm2_label = ctk.CTkLabel(
    landing_frame,
    text="Real-time temperature • Humidity • Wind",
    font=ctk.CTkFont(size=13),
    text_color="#777272"
)
Wlcm2_label.pack(pady=(0,0))

landing_frame.pack()


#after weather is loaded
weather_frame = ctk.CTkFrame(content_frame, fg_color="transparent")

icon_label = ctk.CTkLabel(
    weather_frame,
    text=""
)
icon_label.pack(pady=(0, 10))

temp_label = ctk.CTkLabel(
    weather_frame,
    text="",
    font=ctk.CTkFont(size=100, weight="bold")
)
temp_label.pack(pady=(0, 30))

condition_label = ctk.CTkLabel(
    weather_frame,
    text="",
    font=ctk.CTkFont(size=16),
    text_color="#666666"
)
condition_label.pack(pady=(5, 5))

details_label = ctk.CTkLabel(
    weather_frame,
    text="",
    font=ctk.CTkFont(size=13),
    text_color="#777272"
)
details_label.pack()


quick_frame = ctk.CTkFrame(app, fg_color="transparent")
quick_frame.pack(pady=(5, 10))

quick_label = ctk.CTkLabel(
    quick_frame,
    text="Popular Cities",
    font=ctk.CTkFont(size=14),
    text_color="#888888"
)
quick_label.pack()

cities_frame = ctk.CTkFrame(quick_frame, fg_color="transparent")
cities_frame.pack(pady=5)

def search_city(city):
    city_entry.delete(0, "end")

    city_entry.insert(0, city)
    search()

for city in ["Delhi", "Mumbai", "London", "Tokyo"]:
    btn = ctk.CTkButton(
        cities_frame,
        text=city,
        height=30,
        corner_radius=15,
        text_color="#888888",
        fg_color="#1f1f1f",
        hover_color="#2a2a2a",
        command=lambda c=city: search_city(c)
    )
    btn.pack(side="left", padx=6)

bottom_frame = ctk.CTkFrame(app, fg_color="transparent")
bottom_frame.pack(fill="x", pady=20)

search_container = ctk.CTkFrame(
    bottom_frame,
    height=55,
    corner_radius=30,
    fg_color="#181818"
)
search_container.pack(padx=25, fill="x")
search_container.pack_propagate(False)

mic_button = ctk.CTkButton(
    search_container,
    text="",
    image=mic_icon,
    width=40,
    height=40,
    corner_radius=20,
    fg_color="transparent",
    hover_color="#2a2a2a"
)
mic_button.pack(side="left", padx=(10, 8), pady=7)


city_entry = ctk.CTkEntry(
    search_container,
    placeholder_text="Search city...",
    fg_color="transparent",
    border_width=0,
    text_color="#888888"
)
city_entry.pack(side="left", expand=True, fill="both")


search_button = ctk.CTkButton(
    search_container,
    text="",
    image=search_icon,
    width=40,
    height=40,
    corner_radius=20,
    fg_color="transparent",
    hover_color="#2a2a2a",
    command=search
)
search_button.pack(side="right", padx=(8, 10), pady=7)

def on_close():
    try:
        if current_sound and pygame.mixer.get_busy():
            pygame.mixer.stop()
        if os.path.exists("weather.mp3"):
            os.remove("weather.mp3")
    except:
        pass
    app.destroy()
app.protocol("WM_DELETE_WINDOW", on_close)

app.mainloop()

# Weather Assistant Desktop Application

A modern Python-based Weather Assistant built using CustomTkinter*.
This desktop application provides real-time weather updates with natural voice output using Microsoft Edge TTS, along with secure API key management through environment variables.

Designed as a structured, modular desktop application following clean development practices.

---

## Features

* 🌍 Real-time weather data using Weather API
* 🎨 Modern GUI built with CustomTkinter
* 🔊 Natural Text-to-Speech output using Edge TTS
* 🎵 Audio playback handled with Pygame
* 🔐 Secure API key storage using `.env`
* ⚠️ Error handling for invalid city inputs
* 🧱 Modular and maintainable code structure

---

## 🛠 Tech Stack

* Python 3.x
* CustomTkinter
* Requests
* Edge-TTS
* Pygame
* python-dotenv

---

## 📂 Project Structure

```
weather-assistant-app/
│
├── app.py                # Entry point of the application
├── requirements.txt      # Project dependencies
├── README.md
├── .gitignore
├── .env                  # Not included in repository (contains API key)
├── weather_api.py        # Module to fetch weather data
└── venv/                 # Local virtual environment (not uploaded)


---
# Installation & Setup

## 1️ Clone the Repository

git clone https://github.com/reetiksil/weather-assistant-app.git

cd weather-assistant-app

### 2️ Create a Virtual Environment (Recommended)

python -m venv venv

### 3️ Activate the Virtual Environment

 #### For Windows: 

venv\Scripts\activate

 #### For Mac/Linux:

source venv/bin/activate


### 4️ Install Dependencies

pip install -r requirements.txt


### 5️ Create a `.env` File

Inside the project root directory, create a file named:

.env

Add your Weather API key inside it:

WEATHER_API_KEY=your_api_key_here


### 6️ Run the Application

python app.py

The GUI will launch and you can search for any city to get:

* Temperature
* Weather conditions
* Voice-based weather announcement


## 🔮 Future Improvements

* 🎤 Voice-based city search
* 📦 Convert application to standalone executable (.exe)
* 🌗 Light/Dark theme toggle
* 🌎 Multi-language support
* 📊 Extended weather details (wind speed, pressure, forecast)


##  License

This project is created for educational and learning purposes.


## 👩 Author

Developed as part of MCA Minor Project and personal development practice.
Focused on building structured, modular desktop applications using Python.

# 🌦️ Weather Assistant Desktop Application

A modern **Python-based desktop Weather Assistant** built with **CustomTkinter**. The application fetches real-time weather information using a weather API and provides natural voice-based weather announcements using **Microsoft Edge TTS**.

The project follows a **modular and structured architecture**, with secure API key management through environment variables and dedicated modules for handling weather data and application logic.

---

## ✨ Features

* 🌍 **Real-time Weather Data** — Get current weather information for any city.
* 🎨 **Modern GUI** — Clean and responsive desktop interface built with CustomTkinter.
* 🔊 **Text-to-Speech** — Converts weather information into natural-sounding speech using Microsoft Edge TTS.
* 🎵 **Audio Playback** — Plays generated speech using Pygame.
* 🔐 **Secure API Key Management** — API credentials are stored in a `.env` file and excluded from version control.
* ⚠️ **Error Handling** — Handles invalid city names and API-related errors.
* 🧱 **Modular Architecture** — Separates application interface and weather API functionality for easier maintenance.

---

## 🛠️ Tech Stack

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| **Python 3.x**    | Core programming language       |
| **CustomTkinter** | Modern desktop GUI              |
| **Requests**      | Weather API requests            |
| **Edge-TTS**      | Text-to-speech generation       |
| **Pygame**        | Audio playback                  |
| **python-dotenv** | Environment variable management |

---

## 📂 Project Structure

```text
weather-assistant-app/
│
├── app.py                # Main application and GUI
├── weather_api.py        # Weather API functionality
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignored files
├── .env                  # API key (not included in repository)
└── venv/                 # Virtual environment (not included)
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/reetiksil/weather-assistant-app.git
```

Navigate to the project directory:

```bash
cd weather-assistant-app
```

---

### 2. Create a Virtual Environment

Creating a virtual environment is recommended to keep project dependencies isolated.

```bash
python -m venv venv
```

---

### 3. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

---

### 4. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

---

### 5. Configure the API Key

Create a file named `.env` in the project's root directory:

```text
.env
```

Add your weather API key:

```env
WEATHER_API_KEY=your_api_key_here
```

> **Important:** Never commit your `.env` file to GitHub. Make sure `.env` is included in your `.gitignore` file to prevent accidentally exposing your API key.

---

### 6. Run the Application

Start the application with:

```bash
python app.py
```

The Weather Assistant GUI will launch, allowing you to search for a city and retrieve information such as:

* 🌡️ Temperature
* 🌤️ Current weather conditions
* 🔊 Voice-based weather announcement

---

## 🔄 How It Works

The application follows a simple workflow:

```text
User enters city
       ↓
Application sends request
       ↓
Weather API
       ↓
Weather data received
       ↓
Information displayed in GUI
       ↓
Weather summary converted to speech
       ↓
Audio played using Pygame
```

---

## 🔐 Security

The project uses environment variables to keep the API key separate from the source code.

The API key is stored in:

```text
.env
```

and accessed through `python-dotenv`.

The `.env` file should **never be uploaded to GitHub**.

Example `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

## 🔮 Future Improvements

Potential improvements include:

* 🎤 Voice-based city search
* 📦 Packaging the application as a standalone `.exe`
* 🌗 Light/Dark theme toggle
* 🌎 Multi-language voice output
* 📊 Extended weather information

  * Wind speed
  * Atmospheric pressure
  * Humidity
  * Visibility
  * Forecast data
* 📅 Multi-day weather forecasts
* 📍 Automatic location-based weather detection

---

## 📜 License

This project was created for **educational and learning purposes**

---

## 👨‍💻 Author

**Reetik Sil**

Developed as part of personal development practice, with a focus on building structured and modular Python desktop applications.

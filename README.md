# 🎥 TL;DW — AI YouTube Video Summarizer

**TL;DW (Too Long; Didn't Watch)** is a modern, single-file web application built with Python and FastAPI. It downloads public YouTube videos and processes them through Gemini 2.5 Flash to generate easy-to-read summaries.

---

## Features

* True video analysys: instead of giving the llm just the transcryptipon, the program downloads the video in a low quality and then sends it to gemini
---

## Tech Stack & Architecture

* **Backend Framework:** FastAPI (Asynchronous Python Web Server)
* **Data Validation:** Pydantic (Type Enforcement Schemas)
* **Media Downloader:** yt-dlp
* **AI Core Engine:** Google GenAI SDK (`gemini-2.5-flash`)

---

## Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/teabiotic/TL_DW.git
   cd TL_DW
   ```

2. **Activate your virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Expose your Gemini API Key:**
   Get a free API key from Google AI Studio and export it to your current shell:
   ```bash
   set -x GEMINI_API_KEY "your_api_key"
   ```

5. **Fire up the web server:**
   ```bash
   python main.py
   ```
   Open your browser and navigate to `http://127.0.0.1:8000` to start summarizing!



* and if u use winslop, i ain't helping you

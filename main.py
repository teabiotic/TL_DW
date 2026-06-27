import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>YouTube Summarizer</title></head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h1>TL;DW, an AI YouTube Video Summarizer</h1>
            <p>version 1.0 (a.k.a. "nothing")</p>
            <div style="margin-top: 30px;">
                <input type="text" id="videoUrl" placeholder="Paste your YT link here..." 
                       style="width: 350px; padding: 10px; border: 1px solid #ccc; border-radius: 1px; font-size: 16px;">
                
                <button style="padding: 10px 20px; background-color: #ff0000; color: white; border: none; border-radius: 1px; font-size: 16px; cursor: pointer; font-weight: bold; margin-left: 10px;">
                    SUMMARIZE
                </button>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


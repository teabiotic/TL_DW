import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from google import genai
import yt_dlp
import time


app = FastAPI()

def down_vid(url: str) -> str:
    filename = "video_for_summary.mp4"
    
    if os.path.exists(filename):
        os.remove(filename)
        
    opcje = {
        'format': 'worst[ext=mp4]/mp4', 
        'outtmpl': filename,
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(opcje) as ydl:
        ydl.download([url])
        
    return filename

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head><title>YouTube Summarizer</title></head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
            <h1>TL;DW, an AI YouTube Video Summarizer</h1>
            <p>version 1.2 (a.k.a. "I think it's working")</p>
            
            <div style="margin-top: 30px;">
                <input type="text" id="videoUrl" placeholder="Paste your YT link here..." 
                       style="width: 350px; padding: 10px; border: 1px solid #ccc; border-radius: 1px; font-size: 16px;">
                
                <button onclick="getSummary()" id="submitBtn" style="padding: 10px 20px; background-color: #ff0000; color: white; border: none; border-radius: 1px; font-size: 16px; cursor: pointer; font-weight: bold; margin-left: 10px;">
                    SUMMARIZE
                </button>
            </div>

            <div id="result" style="margin-top: 40px; max-width: 600px; margin-left: auto; margin-right: auto; text-align: left; padding: 20px; background: black; border-radius: 8px; color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                the summary will appear here...
            </div>

            <script>
                async function getSummary() {
                    const urlInput = document.getElementById('videoUrl').value;
                    const resultDiv = document.getElementById('result');
                    const submitBtn = document.getElementById('submitBtn');

                    if (!urlInput) {
                        alert("Please paste a link first!");
                        return;
                    }

                    resultDiv.innerText = "Downloading video and analyzing content... This can take up to a minute.";
                    submitBtn.disabled = true;

                    try {
                        const response = await fetch('/summarize', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ url: urlInput }) // This feeds the URL to your Pydantic model
                        });

                        const data = await response.json();

                        if (data.success) {
                            resultDiv.innerText = data.summary;
                        } else {
                            resultDiv.innerText = "Error: " + data.error;
                        }

                    } catch (err) {
                        resultDiv.innerText = "An unexpected network error occurred: " + err.message;
                    } finally {
                        submitBtn.disabled = false;
                    }
                }
            </script>

        </body>
    </html>
    """

class SummaryRequest(BaseModel):
    url: str

@app.post("/summarize")
async def process_summary(data: SummaryRequest):
    try:
        video_path = down_vid(data.url)
        
        client = genai.Client()
        
        uploaded_file = client.files.upload(file=video_path)
        
        while uploaded_file.state.name == "PROCESSING":
            time.sleep(2)
            uploaded_file = client.files.get(name=uploaded_file.name)
            
        if uploaded_file.state.name == "FAILED":
            raise Exception("Google infrastructure failed to process the video asset.")
            
        prompt = (
            "Analyze this video and provide a comprehensive summary using highly organized "
            "bullet points. use up to 10 bullet points and m,ake the answer as"
            " short as possible while still containing all the necessary info. "
            "Highlight the main topic, core arguments, and critical takeaways."
        )
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[uploaded_file, prompt]
        )
        
        if os.path.exists(video_path):
            os.remove(video_path)
        client.files.delete(name=uploaded_file.name)
        
        return {"success": True, "summary": response.text}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


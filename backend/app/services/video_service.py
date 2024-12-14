from phi.agent import Agent
from phi.model.google import Gemini
from google.generativeai import upload_file, get_file
import tempfile
import os
import aiofiles
import asyncio
from pathlib import Path

class VideoService:
    def __init__(self):
        self.agent = Agent(
            name="Video Analysis Assistant",
            model=Gemini(id="gemini-2.0-flash-exp"),
            markdown=True,
        )
    
    async def save_video(self, file):
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        
        file_path = temp_dir / f"{file.filename}"
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
            
        return str(file_path)
    
    async def analyze_video(self, video_path, prompt):
        try:
            video_file = upload_file(video_path)
            
            while video_file.state.name == "PROCESSING":
                await asyncio.sleep(2)
                video_file = get_file(video_file.name)

            prompt_text = f"""
            Analyze this video and answer the following question: {prompt}
            Focus on providing clear, specific observations from the video content.
            """

            result = self.agent.run(prompt_text, videos=[video_file])
            return result.content
            
        finally:
            Path(video_path).unlink(missing_ok=True) 
# 🎬 Demo Video Script

## Pre-Recording Setup
1. **Start the Docker container:**
   ```bash
   export HUGGINGFACE_HUB_TOKEN="your_token_here"
   ./build_docker.sh
   ```

2. **Verify it's running:**
   - Open http://localhost:5000
   - Check health: http://localhost:5000/health

## Demo Script (2-3 minutes)

### **Introduction (30 seconds)**
- "Hi, I'm Ayush Chaudhary"
- "This is my Slang Translator project"
- "It uses AI to convert formal English into casual slang"
- "It's containerized with Docker for easy deployment"

### **Show the Interface (30 seconds)**
- Show the webpage: http://localhost:5000
- Point out "Created by Ayush Chaudhary" in the header
- Show the clean, modern interface
- Highlight the input text area

### **Demonstrate Translation (60 seconds)**
- Try example: "I would like to request your assistance"
- Click "Translate to Slang"
- Show the loading animation
- Display the slang translation result
- Try another example: "Please wait a moment"
- Show the translation

### **Show Technical Details (30 seconds)**
- Open terminal
- Show `docker ps` to display running container
- Show `docker logs slang-translator-app` briefly
- Mention it uses Mistral-7B model

### **Conclusion (30 seconds)**
- "The app is fully containerized with Docker"
- "It can be easily deployed anywhere"
- "All code is available on GitHub"
- "Thank you for watching!"

## Post-Recording
- Save video as `demo_video.mov` in the project root
- The README is already configured to link to this file
- Commit and push the video file to GitHub
- The video will be directly playable in the README

## Tips for Recording
- Use a clean desktop background
- Zoom in on the browser window
- Speak clearly and at moderate pace
- Show both the interface and terminal
- Keep it under 3 minutes

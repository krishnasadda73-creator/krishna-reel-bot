import os
import random
import subprocess
from pathlib import Path
from datetime import datetime
import textwrap
import pickle

from PIL import Image, ImageDraw, ImageFont
import google.generativeai as genai

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

IMAGE_FOLDER = "images"
BGM_FOLDER = "bgm"
FONT_PATH = "fonts/NotoSansDevanagari-Regular.ttf"

OUTPUT_IMAGE = "frame.png"
OUTPUT_VIDEO = "reel.mp4"

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def generate_text():
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.0-flash")

```
prompt = "एक छोटी, गहरी कृष्ण भक्ति की हिंदी लाइन लिखो, बिना इमोजी।"
try:
    return model.generate_content(prompt).text.strip()
except:
    return "जब कृष्ण साथ हों, तो हर डर समाप्त हो जाता है।"
```

def create_image(text):
imgs = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith((".jpg",".png"))]
img = Image.open(os.path.join(IMAGE_FOLDER, random.choice(imgs))).resize((1080,1920))
draw = ImageDraw.Draw(img)

```
try:
    font = ImageFont.truetype(FONT_PATH, 64)
except:
    font = ImageFont.load_default()

lines = textwrap.wrap(text, 18)
y = 800
for line in lines:
    w = draw.textlength(line, font=font)
    draw.text(((1080-w)//2, y), line, font=font, fill="white", stroke_width=3, stroke_fill="black")
    y += 80

img.save(OUTPUT_IMAGE)
```

def create_video():
bgm = random.choice(list(Path(BGM_FOLDER).glob("*.mp3")))
cmd = [
"ffmpeg","-y","-loop","1","-i",OUTPUT_IMAGE,"-i",str(bgm),
"-t","15","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-shortest",
"-vf","scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
OUTPUT_VIDEO
]
subprocess.run(cmd)

def get_youtube():
creds=None
if os.path.exists("token.pickle"):
creds=pickle.load(open("token.pickle","rb"))
if not creds:
flow=InstalledAppFlow.from_client_secrets_file("client_secret.json",SCOPES)
creds=flow.run_local_server(port=0)
pickle.dump(creds,open("token.pickle","wb"))
return build("youtube","v3",credentials=creds)

def upload():
yt=get_youtube()
body={
"snippet":{
"title":f"Jai Shree Krishna 🙏 {datetime.now().strftime('%d %b')}",
"description":"#krishna #shorts",
"categoryId":"22"
},
"status":{"privacyStatus":"public"}
}
media=MediaFileUpload(OUTPUT_VIDEO)
yt.videos().insert(part="snippet,status",body=body,media_body=media).execute()

def main():
print("START")
text=generate_text()
print(text)
create_image(text)
create_video()
upload()
print("DONE")

if **name**=="**main**":
main()

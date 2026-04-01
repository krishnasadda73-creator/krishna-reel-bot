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

# ================= TEXT =================

def generate_text():
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

```
model = genai.GenerativeModel("models/gemini-2.0-flash")

prompt = "एक छोटी, गहरी कृष्ण भक्ति की हिंदी लाइन लिखो, बिना इमोजी।"

try:
    res = model.generate_content(prompt)
    return res.text.strip()
except:
    return "जब कृष्ण साथ हों, तो हर डर समाप्त हो जाता है।"
```

# ================= IMAGE =================

def create_image(text):
images = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith((".jpg", ".png"))]

```
if not images:
    raise Exception("No images found in images/ folder")

img_path = os.path.join(IMAGE_FOLDER, random.choice(images))

base = Image.open(img_path).convert("RGB").resize((1080, 1920))
draw = ImageDraw.Draw(base)

try:
    font = ImageFont.truetype(FONT_PATH, 64)
except:
    font = ImageFont.load_default()

lines = textwrap.wrap(text, width=18)

y = 800
for line in lines:
    w = draw.textlength(line, font=font)
    x = (1080 - w) // 2
    draw.text((x, y), line, font=font, fill="white", stroke_width=3, stroke_fill="black")
    y += 80

base.save(OUTPUT_IMAGE)
print("✅ Image created")
```

# ================= VIDEO =================

def create_video():
tracks = list(Path(BGM_FOLDER).glob("*.mp3")) + list(Path(BGM_FOLDER).glob("*.wav"))

```
if not tracks:
    raise Exception("No BGM found")

bgm = random.choice(tracks)

cmd = [
    "ffmpeg",
    "-y",
    "-loop", "1",
    "-i", OUTPUT_IMAGE,
    "-i", str(bgm),
    "-t", "15",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-shortest",
    "-vf",
    "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
    OUTPUT_VIDEO
]

subprocess.run(cmd)
print("✅ Video created")
```

# ================= YOUTUBE =================

def get_youtube():
creds = None

```
if os.path.exists("token.pickle"):
    with open("token.pickle", "rb") as f:
        creds = pickle.load(f)

if not creds:
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)

    with open("token.pickle", "wb") as f:
        pickle.dump(creds, f)

return build("youtube", "v3", credentials=creds)
```

def upload():
youtube = get_youtube()

```
body = {
    "snippet": {
        "title": f"Jai Shree Krishna 🙏 {datetime.now().strftime('%d %b')}",
        "description": "#krishna #shorts",
        "categoryId": "22"
    },
    "status": {
        "privacyStatus": "public"
    }
}

media = MediaFileUpload(OUTPUT_VIDEO)

youtube.videos().insert(
    part="snippet,status",
    body=body,
    media_body=media
).execute()

print("✅ Uploaded")
```

# ================= MAIN =================

def main():
print("🚀 START")

```
text = generate_text()
print("📜", text)

create_image(text)
create_video()

# IMPORTANT: GitHub pe upload fail hota hai → skip safely
try:
    upload()
except Exception as e:
    print("⚠️ Upload skipped:", e)

print("🎉 DONE")
```

if **name** == "**main**":
main()

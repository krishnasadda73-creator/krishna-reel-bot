import os
import random
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap
import google.generativeai as genai

IMAGE_FOLDER = "images"
BGM_FOLDER = "bgm"
FONT_PATH = "fonts/NotoSansDevanagari-Regular.ttf"

OUTPUT_IMAGE = "frame.png"
OUTPUT_VIDEO = "reel.mp4"

def generate_text():
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.0-flash")

```
try:
    res = model.generate_content("एक छोटी कृष्ण भक्ति लाइन लिखो")
    return res.text.strip()
except:
    return "जब कृष्ण साथ हों, तो डर खत्म हो जाता है।"
```

def create_image(text):
images = os.listdir(IMAGE_FOLDER)
img_path = os.path.join(IMAGE_FOLDER, random.choice(images))

```
base = Image.open(img_path).resize((1080, 1920))
draw = ImageDraw.Draw(base)

try:
    font = ImageFont.truetype(FONT_PATH, 64)
except:
    font = ImageFont.load_default()

lines = textwrap.wrap(text, 18)

y = 800
for line in lines:
    w = draw.textlength(line, font=font)
    draw.text(((1080 - w)//2, y), line, font=font, fill="white")
    y += 80

base.save(OUTPUT_IMAGE)
```

def create_video():
bgm = random.choice(list(Path(BGM_FOLDER).glob("*.mp3")))

```
cmd = [
    "ffmpeg",
    "-y",
    "-loop", "1",
    "-i", OUTPUT_IMAGE,
    "-i", str(bgm),
    "-t", "10",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    OUTPUT_VIDEO
]

subprocess.run(cmd)
```

def main():
print("🚀 Running full bot")

```
text = generate_text()
print("Text:", text)

create_image(text)
create_video()

print("✅ DONE (video created)")
```

if **name** == "**main**":
main()

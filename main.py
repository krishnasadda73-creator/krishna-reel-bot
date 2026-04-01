import os
import random
import subprocess
from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont
import google.generativeai as genai


IMAGE_FOLDER = "images"
BGM_FOLDER = "bgm"
FONT_PATH = "fonts/NotoSansDevanagari-Regular.ttf"

OUTPUT_IMAGE = "frame.png"
OUTPUT_VIDEO = "reel.mp4"


# ================= TEXT =================
def generate_text():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("models/gemini-2.0-flash")

    prompt = "एक छोटी, गहरी कृष्ण भक्ति की हिंदी लाइन लिखो, बिना इमोजी।"

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Gemini error:", e)
        return "जब कृष्ण साथ हों, तो हर डर समाप्त हो जाता है।"


# ================= IMAGE =================
def create_image(text):
    images = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith((".jpg", ".png"))]

    if not images:
        raise Exception("❌ No images found in images/")

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

        draw.text(
            (x, y),
            line,
            font=font,
            fill="white",
            stroke_width=3,
            stroke_fill="black"
        )

        y += 80

    base.save(OUTPUT_IMAGE)
    print("✅ Image created")


# ================= VIDEO =================
def create_video():
    tracks = list(Path(BGM_FOLDER).glob("*.mp3")) + list(Path(BGM_FOLDER).glob("*.wav"))

    if not tracks:
        raise Exception("❌ No BGM found")

    bgm = random.choice(tracks)

    cmd = [
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", OUTPUT_IMAGE,
        "-i", str(bgm),
        "-t", "10",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        OUTPUT_VIDEO
    ]

    subprocess.run(cmd)
    print("✅ Video created")


# ================= MAIN =================
def main():
    print("🚀 BOT START")

    text = generate_text()
    print("📜 Text:", text)

    create_image(text)
    create_video()

    print("🎉 DONE")


if __name__ == "__main__":
    main()

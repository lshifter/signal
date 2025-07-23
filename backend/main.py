import openai
import base64
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import json
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # укажи домен фронта для продакшена!
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = "sk-...ТВОЙ_КЛЮЧ..."

DISCLAIMER = (
    "⚠️ Дисклеймер: Шанс выигрыша 86%. Мы работаем честно, но помни о рисках. "
    "Все решения принимаешь ты сам. Не нарушай законы своей страны!"
)

def generate_aviator_signal():
    n = random.randint(10, 50)
    coeffs = []
    last = 1.2
    for i in range(n):
        if i % 5 == 0 and i != 0:
            last = round(last + 0.1, 2)
        coeffs.append(f"Забери на x{last}")
    coeffs_text = "<br>".join(f"• {x}" for x in coeffs[:10])
    return (
        f"✈️ <b>Сигнал для AviaMaster</b><br>"
        f"1️⃣ Сделай {n} игр с минимальным депозитом<br>"
        f"2️⃣ В каждой игре забирай на низких коэффициентах:<br>{coeffs_text}<br>"
        f"3️⃣ После выигрыша — стоп<br><br>"
        f"{DISCLAIMER}"
    )

def generate_chicken_signal():
    jumps = random.randint(6, 9)
    attempts = random.randint(10, 30)
    return (
        f"🐔 <b>Сигнал для Checken Road</b><br>"
        f"1️⃣ Сделай {attempts} заходов по минимальной ставке<br>"
        f"2️⃣ В каждом заходе делай ровно {jumps} прыжков (это безопасная стратегия)<br>"
        f"3️⃣ Как только словил выигрыш — остановись!<br><br>"
        f"{DISCLAIMER}"
    )

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...), game: str = Form(...)):
    img_bytes = await file.read()
    img_b64 = base64.b64encode(img_bytes).decode()
    img_mime = file.content_type
    image_url = f"data:{img_mime};base64,{img_b64}"

    prompt = (
        f"Ты эксперт по азартным играм. "
        f"Проверь, является ли изображение скриншотом из игры '{game}'. "
        f"Ответь только JSON: {{'match': true}} если это явно скриншот этой игры, "
        f"или {{'match': false}} если нет. Не пиши ничего кроме JSON."
    )

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Проверь игру по скриншоту:"},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ],
            }
        ],
        max_tokens=100,
        temperature=0.1,
    )
    result = response.choices[0].message.content.strip()
    try:
        match = json.loads(result).get("match", False)
    except Exception:
        match = False

    if not match:
        return {"error": "Скриншот не похож на выбранную игру. Загрузите реальный скрин из игры!"}

    if game == "Checken Road":
        signal = generate_chicken_signal()
    elif game == "AviaMaster":
        signal = generate_aviator_signal()
    else:
        signal = "Ошибка: неизвестная игра."
    return {"signal": signal}

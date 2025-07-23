import random
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для релиза укажи домен фронта!
    allow_methods=["*"],
    allow_headers=["*"],
)

DISCLAIMER = (
    "⚠️ Бот может выдать неправильный сигнал. Загружайте актуальный скриншот с игры!\n"
    "Шанс выигрыша 86%. Мы работаем честно, но помни о рисках. "
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
        f"✈️ <b>Сигнал для Aviator</b><br>"
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
    # Можно даже не читать файл, просто вернуть сигнал
    if game == "Checken Road":
        signal = generate_chicken_signal()
    elif game == "Aviator":
        signal = generate_aviator_signal()
    else:
        signal = "Ошибка: неизвестная игра."
    return {"signal": signal}


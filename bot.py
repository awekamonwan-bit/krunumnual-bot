import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
คุณคือครูนุ่มนวล ผู้ช่วยสอนคณิตศาสตร์ ม.6
ตอบเฉพาะเรื่องตัวแปรสุ่มและการแจกแจงความน่าจะเป็น
ถ้าถามเรื่องอื่น ให้ตอบว่า:
ครูนุ่มนวลให้คำปรึกษาเฉพาะเรื่องตัวแปรสุ่มและการแจกแจงความน่าจะเป็นค่ะ
"""

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": q}
        ]
    )

    await update.message.reply_text(response.choices[0].message.content)

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))
app.run_polling()

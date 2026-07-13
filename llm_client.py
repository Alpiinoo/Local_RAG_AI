from openai import OpenAI
import subprocess
import re

def get_foundry_port():
    result = subprocess.run(
        ["foundry", "service", "status"],
        capture_output=True, text=True
    )
    match = re.search(r"http://127\.0\.0\.1:(\d+)", result.stdout)
    if match:
        return match.group(1)
    return "5273"  # default fallback

port = get_foundry_port()
print(f"Foundry Local port: {port}")

client = OpenAI(
    api_key="foundry-local",
    base_url=f"http://127.0.0.1:{port}/v1"
)

MODEL_ID = "phi-3.5-mini-instruct-trtrtx-gpu:2"
print("Foundry Local'e bağlanıldı!")

def build_prompt(question, chunks):
    context = ""
    for score, source, content in chunks:
        context += f"\n[Kaynak: {source}]\n{content}\n"

    system_message = (
        "Sen yardımcı bir Türkçe asistansın. "
        "Yalnızca sana verilen bağlamı kullanarak soruları Türkçe cevapla. "
        "Eğer cevap bağlamda yoksa sadece 'Bu konuda bilgim yok.' de. "
        "Cevabın sonunda hangi kaynaktan bulduğunu belirt. "
        "Kısa ve öz cevap ver."
    )
    user_message = f"Bağlam:\n{context}\nSoru: {question}"
    return system_message, user_message

def answer_query(question, chunks):
    system_msg, user_msg = build_prompt(question, chunks)
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user",   "content": user_msg}
        ]
    )
    return response.choices[0].message.content
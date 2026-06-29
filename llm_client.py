from openai import OpenAI

# Foundry Local'in default portu
client = OpenAI(
    api_key="foundry-local",
    base_url="http://127.0.0.1:62803/v1"
)

MODEL_ID = "phi-3.5-mini-instruct-trtrtx-gpu:2"

print("Foundry Local'e bağlanıldı!")

def build_prompt(question, chunks):
    context = ""
    for score, source, content in chunks:
        context += f"\n[Kaynak: {source}]\n{content}\n"

    system_message = (
        "Sen yardımcı bir asistansın. "
        "Yalnızca sana verilen bağlamı kullanarak soruları cevapla. "
        "Eğer cevap bağlamda yoksa 'Bu bilgiye sahip değilim.' de. "
        "Cevabında kaynak adını belirt."
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
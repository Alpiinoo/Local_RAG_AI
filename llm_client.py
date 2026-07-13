from openai import OpenAI
import subprocess
import re

def get_foundry_port():
    result = subprocess.run(
        ["foundry", "service", "status"],
        capture_output=True, text=True
    )
    output = result.stdout + result.stderr
    match = re.search(r"http://127\.0\.0\.1:(\d+)", output)
    if match:
        return match.group(1)
    return "55890"

port = get_foundry_port()
print(f"Foundry Local port: {port}")

client = OpenAI(
    api_key="foundry-local",
    base_url=f"http://127.0.0.1:{port}/v1"
)

MODEL_ID = "qwen2.5-7b-instruct-trtrtx-gpu:2"
print("Foundry Local'e bağlanıldı!")

def build_prompt(question, chunks):
    context = ""
    for score, source, content in chunks:
        context += f"\n[Kaynak: {source}]\n{content}\n"

    system_message = (
        "You are a helpful assistant. "
        "Answer ONLY using the provided context below. "
        "Answer in English. "
        "Be direct and concise. "
        "If the answer is not in the context, say: I don't have information about that. "
        "At the end, add: Source: [filename]"
        "Be tolerant of minor typos and grammatical errors in the question. "
    )
    user_message = f"Context:\n{context}\nQuestion: {question}"
    return system_message, user_message

def answer_query(question, chunks):
    system_msg, user_msg = build_prompt(question, chunks)
    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user",   "content": user_msg}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"
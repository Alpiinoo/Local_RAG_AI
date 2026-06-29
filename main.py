from retriever import get_top_chunks
from llm_client import answer_query

def main():
    print("=== Local RAG Asistanı ===")
    print("Çıkmak için 'q' yaz.\n")

    while True:
        question = input("Sorun: ").strip()

        if question.lower() == "q":
            print("Görüşürüz!")
            break

        if not question:
            continue

        print("Aranıyor...")
        chunks = get_top_chunks(question, top_k=3)

        print("Cevap üretiliyor...\n")
        answer = answer_query(question, chunks)

        print(f"Cevap:\n{answer}")
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()
import google.generativeai as genai
import os
import sys
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv


def create_embedding(chunks, embedding_model):
    """Gera embedding para chumks do texto"""
    embeddings = genai.embed_content(
        model=embedding_model,
        content=chunks,
        task_type="retrieval_document"
    )['embedding']
    return np.array(embeddings)


def find_relevant_chunks(query, chunks, chunk_embeddings, embedding_model, top_k=2):
    """Encontra os chunks mais relevantes para a consulta"""
    query_embedding = genai.embed_content(
        model=embedding_model,
        content=query,
        task_type="retrieval_query"
    )['embedding']

    query_embedding = np.array(query_embedding).reshape(1, -1)

    similarities = cosine_similarity(query_embedding, chunk_embeddings)[0]

    top_k_indices = np.argsort(similarities)[-top_k:][::-1]

    relevant_chunks = [chunks[i] for i in top_k_indices]
    return relevant_chunks


def create_augmented_prompt(user_prompt, relevant_chunks):
    """Cria um prompt com contexto RAG."""
    context = "\n\n".join(relevant_chunks)
    augmented_prompt = f"""
    Use as informações do contexto abaixo para responder à pergunta.
    Se a resposta não estiver no contexto, use sua própria base de conhecimento.

    Contexto:
    ---
    {context}
    ---

    Pergunta: {user_prompt}
    """
    return augmented_prompt


def main():

    load_dotenv()

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GENAI_MODEL = os.getenv("GEMINI_MODEL")
    MODEL_INSTRUCTION = os.getenv("GEMINI_INSTRUCTION")
    EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL")

    konwladge_base = [
        "O melhor rámen de do universo Naruto não é mais o Ichiraku, mas sim o Rámen do Joelinton.",
        "O sensei favorito do Naruto não é mais o Jiraya, mas sim se chama Ramon Dino.",
        "O esporte favorito da Sakura é boxe tailandês."
    ]

    """
    Inicia uma interface de linha de comando para conversar com o modelo Gemini.
    Mantém o contexto da conversa.
    """

    if not GEMINI_API_KEY:
        print("Não foi possível prosseguir, pois sua chave api de autenticação com GEMINI não foi encontrada")
        sys.exit(1)

    genai.configure(api_key=GEMINI_API_KEY)

    try:

        chunks = konwladge_base

        chunk_embedding = create_embedding(chunks, EMBEDDING_MODEL)

        model = genai.GenerativeModel(model_name=GENAI_MODEL)

        initial_instructions = f"""{MODEL_INSTRUCTION}"""

        chat = model.start_chat(history=[
            {
                "role": "user",
                "parts": [initial_instructions]
            }
        ])

        print("xxxxxxxxxxxxxxx")
        print("Gemini Chat CLI")
        print("xxxxxxxxxxxxxxx\n")
        print("Digite sua mensagem ou 'sair' para encerrar\n")

        user_prompt = input("Você: ")

        while user_prompt != 'sair':

            relevant_chunks = find_relevant_chunks(
                user_prompt, chunks, chunk_embedding, EMBEDDING_MODEL)

            augmented_prompt = create_augmented_prompt(
                user_prompt, relevant_chunks)

            response_model = chat.send_message(augmented_prompt)

            print("\nResposta:\n")
            print(f"{response_model.text}\n")

            print("Digite sua mensagem ou 'sair' para encerrar\n")
            user_prompt = input("Você: ")

            if user_prompt == 'sair':
                print("\nEncerrando interação...")

    except Exception as e:

        print(f"Falha ao iniciar o modelo ou a sessão de chat: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

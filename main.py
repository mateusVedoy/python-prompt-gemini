import google.generativeai as genai
import os
import sys
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import questionary


def create_embedding(chunks: list, embedding_model: str):
    """Gera embedding para chunks do texto"""

    if len(chunks) == 0:
        return np.array([])

    embeddings = genai.embed_content(
        model=embedding_model,
        content=chunks,
        task_type="retrieval_document"
    )['embedding']
    return np.array(embeddings)


def find_relevant_chunks(query, chunks, chunk_embeddings, embedding_model, top_k=2) -> list:
    """Encontra os chunks mais relevantes para a consulta"""

    if len(chunks) == 0:
        return []

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


def create_augmented_prompt(user_prompt, relevant_chunks) -> str:
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


def define_system_instruction(system_instruction: str) -> str:
    """
    Permite ao usuário definir alguma(s) instrução ao modelo antes de conversar
    """

    user_choice = questionary.select(
        "Deseja passar alguma instrução antes de começarmos a conversa?",
        choices=['Sim', 'Não']
    ).ask()

    if user_choice == 'Sim':

        instruction = input("Instrução: ")
        return instruction

    return system_instruction


def define_knowledge_base() -> list:
    """
    Permite ao usuário adicionar conhecimento para treinar o modelo durante a conversa
    """

    knowledge_base = []

    user_choice = questionary.select(
        "Deseja ensinar algo ao modelo antes de começarmos a conversa?",
        choices=['Sim', 'Não']
    ).ask()

    while (user_choice == 'Sim'):

        know = input("Conhecimento: ")
        knowledge_base.append(know)

        user_choice = questionary.select(
            "Deseja ensinar algo ao modelo antes de começarmos a conversa?",
            choices=['Sim', 'Não']
        ).ask()

    return knowledge_base


def main():

    load_dotenv()

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GENAI_MODEL = os.getenv("GEMINI_MODEL")
    MODEL_INSTRUCTION = os.getenv("GEMINI_INSTRUCTION")
    EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL")

    """
    Inicia uma interface de linha de comando para conversar com o modelo Gemini.
    Mantém o contexto da conversa.
    """

    if not GEMINI_API_KEY:
        print("Não foi possível prosseguir, pois sua chave api de autenticação com GEMINI não foi encontrada")
        sys.exit(1)

    genai.configure(api_key=GEMINI_API_KEY)

    try:

        instructions = define_system_instruction(MODEL_INSTRUCTION)

        knowledge_base = define_knowledge_base()

        chunks = knowledge_base

        chunk_embedding = create_embedding(chunks, EMBEDDING_MODEL)

        model = genai.GenerativeModel(model_name=GENAI_MODEL)

        initial_instructions = f"""{instructions}"""

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

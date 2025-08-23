import google.generativeai as genai
import os
import sys
from dotenv import load_dotenv


def main():

    load_dotenv()

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GENAI_MODEL = os.getenv("GEMINI_MODEL")

    """
    Inicia uma interface de linha de comando para conversar com o modelo Gemini.
    Mantém o contexto da conversa.
    """

    if not GEMINI_API_KEY:
        print("Não foi possível prosseguir, pois sua chave api de autenticação com GEMINI não foi encontrada")
        sys.exit(1)

    genai.configure(api_key=GEMINI_API_KEY)

    try:

        model = genai.GenerativeModel(model_name=GENAI_MODEL)

        chat = model.start_chat(history=[])

        print("xxxxxxxxxxxxxxx")
        print("Gemini Chat CLI")
        print("xxxxxxxxxxxxxxx\n")
        print("Digite sua mensagem ou 'sair' para encerrar\n")

        user_prompt = input("Você: ")

        while user_prompt != 'sair':

            response_model = chat.send_message(user_prompt)

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

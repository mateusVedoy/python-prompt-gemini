# 🤖 Python CLI Gemini Chat

Uma aplicação de linha de comando simples para interagir com a API do Google Gemini. Este projeto foi desenvolvido para demonstrar a criação de um chat interativo que mantém o contexto da conversa, fazendo uso das melhores práticas de gerenciamento de variáveis de ambiente.

## ✨ Funcionalidade

O projeto consiste em um script Python que se conecta à API do Gemini e permite uma conversa contínua com o modelo generativo. Ele:

- Recebe prompts do usuário via terminal.

- Envia as mensagens para o modelo gemini-pro.

- Mantém o histórico da conversa, permitindo que o modelo "lembre" das interações anteriores na mesma sessão.

- Imprime a resposta do modelo diretamente no terminal.

## 🛠️ Pré-requisitos

Para rodar esta aplicação, você precisará de:

- Ambiente de Desenvolvimento: Recomendamos o uso de um Dev Container (o arquivo devcontainer.json já está configurado no projeto). Isso garantirá que todas as dependências sejam instaladas automaticamente.

- Chave da API do Gemini: Uma chave de API é necessária para autenticar as requisições à API do Google. Você pode obtê-la gratuitamente no Google AI Studio.

## 🔒 Gerenciamento da Chave da API

Para garantir a segurança, a chave da API não é armazenada no código. Em vez disso, ela é lida a partir de um arquivo de variáveis de ambiente (.env), que deve ser mantido fora do controle de versão do Git.

### 1. Crie o arquivo .env

Na raiz do seu projeto, crie um arquivo chamado .env e adicione sua chave de API nele no seguinte formato:
Snippet de código

GEMINI_API_KEY='SUA_CHAVE_AQUI'
GEMINI_MODEL'SEU MODELO AQUI'

Observação: Substitua os valores pelo valor real desejado.

### 2. Adicione ao .gitignore

Certifique-se de que o arquivo .env está no seu .gitignore para evitar que seja enviado para o repositório. O arquivo .gitignore deve conter a seguinte linha:
Snippet de código

.env

## 🚀 Como Utilizar

Siga estes passos para colocar a aplicação em funcionamento:

### 1. Clone o repositório:

```Bash

git clone https://github.com/seu-usuario/python-prompt-gemini.git
cd python-prompt-gemini
```

### 2. Abra no VS Code com Dev Containers:

- Abra a pasta do projeto no VS Code.

- O VS Code irá detectar o arquivo .devcontainer/devcontainer.json e perguntará se você deseja "Reabrir no Container".

- Aceite. Isso irá construir o ambiente e instalar automaticamente todas as dependências, incluindo as bibliotecas google-generativeai e python-dotenv.

### 3. Execute a aplicação:

- Com o container já iniciado, abra o terminal do VS Code.

- Execute o script Python:

```Bash

python main.py

```

### 4. Comece a conversar:

- O chat será iniciado, e você poderá digitar suas perguntas.

- Para sair, digite <strong>sair</strong> no terminal.

### Exemplo de Uso:

```Bash

$ python main.py

xxxxxxxxxxxxxxx
Gemini Chat CLI
xxxxxxxxxxxxxxx

Digite sua mensagem ou 'sair' para encerrar

Você: Olá, como você se chama?

Resposta:

Eu sou um grande modelo de linguagem, treinado pelo Google.
Você: Qual é a sua principal função?

Digite sua mensagem ou 'sair' para encerrar

Você: Sim, conte-me!

Resposta:

Minha principal função é ajudar com uma ampla variedade de tarefas

Digite sua mensagem ou 'sair' para encerrar

Você: sair

Encerrando interação...

```

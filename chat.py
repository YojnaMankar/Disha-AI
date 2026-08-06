from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
model = ChatOllama(model="qwen3:1.7b", temperature=0, thinking=False)  #model creat

conversation = [
    SystemMessage(content="You are a friendly AI assistant, Answer clearly and politely")
]

print("Type 'quit' to close the conversation")

while True:
    user_text=lower = input("Your Query:")
    if user_text == "quit":
        print("Goodbye!")
        break

    conversation.append (HumanMessage(content=user_text))

    response = model.invoke(conversation)
    print("Bot:", response.content)
    conversation.append(AIMessage(content=response.content)) #                                           
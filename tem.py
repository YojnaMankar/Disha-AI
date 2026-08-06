from langchain_ollama import ChatOllama
model = ChatOllama(
    model="qwen3:1.7b",
    temperature=0,
    thinking=False  # code fast run hota hai 
)
response = model.invoke("Give me a creative name for an AI Robot Teacher")
print(response)



import ollama

conversation = []

while True:
    user_input = input("You: ")

    if user_input.lower() in ("quit", "exit"):
        break
    conversation.append({"role": "user", "content": user_input})

    response = ollama.chat(
        model="llama3.2",
        messages=conversation,
    )
    reply = response["message"]["content"]
    print("ollama:", reply)

    conversation.append({"role": "assistant", "content": reply})

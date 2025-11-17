from memory_engine import load_long_memory, save_long_memory, summarize_for_memory
from chatbot_core import ask_chatbot

print("🐉 GOT Chatbot (RAG + Memory)")

character = input("Choose character: ")
mode = input("Choose mode: ")
temperature = float(input("Temperature (0–1.5): "))

long_memory = load_long_memory()

conversation_history = [{"role": "system", "content": "Start of conversation."}]

print("\nChat ready. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Farewell, traveler.")
        break

    # Save important details to long-term memory
    if any(
        k in user_input.lower() for k in ["my name", "i like", "my favorite", "i am"]
    ):
        summary = summarize_for_memory(user_input)
        save_long_memory(summary)
        long_memory.append(summary)

    conversation_history.append({"role": "user", "content": user_input})

    reply = ask_chatbot(conversation_history, character, mode, temperature, long_memory)

    print("Bot:", reply, "\n")

    conversation_history.append({"role": "assistant", "content": reply})

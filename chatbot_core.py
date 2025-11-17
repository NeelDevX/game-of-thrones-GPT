import time
from openai import OpenAI, RateLimitError, APIError
from config import OPENAI_API_KEY, MODEL_NAME
from rag_engine import retrieve_lore
from prompts import STRICT_RAG_RULES
from prompts import build_dynamic_system_prompt

client = OpenAI(api_key=OPENAI_API_KEY)


def ask_chatbot(conversation_history, character, mode, temperature, long_memory):
    latest_question = conversation_history[-1]["content"]

    # Retrieve relevant GoT lore
    rag_context = retrieve_lore(latest_question)

    # Build dynamic system prompt that includes long-term memory + RAG
    system_prompt = build_dynamic_system_prompt(character, mode, long_memory)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Relevant GoT Lore:\n{rag_context}"},
    ] + conversation_history[1:]

    # -----------------------------
    # Retry Logic for Rate Limits
    # -----------------------------
    for attempt in range(2):  # Try 5 times
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME, temperature=temperature, messages=messages
            )
            return response.choices[0].message.content

        except RateLimitError:
            wait = 5 * (attempt + 1)
            print(f"Rate limited. Waiting {wait}s and retrying...")
            time.sleep(wait)

        except APIError:
            wait = 3
            print(f"Temporary API error. Retrying in {wait}s...")
            time.sleep(wait)

    # If all failed:
    return "⚠️ The Citadel's ravens are overwhelmed. Try again in a moment, my friend."

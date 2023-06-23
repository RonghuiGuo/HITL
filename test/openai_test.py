import openai
import time
import os

openai.api_key = os.environ.get("openai_api_key")

def ask_chatgpt(messages):
    extra_response_count = 0
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0
            )
        except Exception as e:
            print(e)
            time.sleep(20)
            continue
        if response["choices"][0]["finish_reason"] == "stop":
            break
        else:
            messages.append({"role": "assistant", "content": response["choices"][0]["message"]["content"]})
            messages.append({"role": "user", "content": "continue"})
            extra_response_count += 1
    return response, messages, extra_response_count


messages=[]
messages.append({"role": "user", "content": "hello"})

ask_chatgpt(messages=messages)
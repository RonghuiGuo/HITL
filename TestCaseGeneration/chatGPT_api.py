import openai
import time
import random
import os
import json


def get_response(message, token):
    openai_key = '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'
    response = None
    while response is None:
        # openai_key = random.choice(openai_keys)
        try:
            # time.sleep(5)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=message,
                max_tokens=token,
                temperature=0,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["# END"],
                api_key=openai_key
            )
            return (response['choices'][0]['message']['content'])
        except Exception as e:
            if str(type(e)) == "<class 'openai.error.InvalidRequestError'>":
                response = "null"
                print(type(e), e)
                break
            if str(type(e)) == "<class 'openai.error.AuthenticationError'>":
                print(openai_key)
            print(type(e), e)
            # openai_key = random.choice(openai_keys)
            continue

def get_result():
    prompt = json.load(open('./prompt/SPL_CFG.json', 'r'))
    test_code = open('./test_code.txt', 'r').read()
    prompt = list(prompt)
    #test_dict = {'role': 'user', 'content': test_code}
    prompt.append({'role': 'user', 'content': test_code})
    code_cfg = get_response(prompt, 1000)
    return code_cfg
if __name__ == '__main__':
    CFG = get_result()
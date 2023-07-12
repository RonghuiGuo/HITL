import openai
import pandas as pd
def get_testcase(fixed_code, DFG):
    openai.api_key = "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"
    message = [{"role": "system"}]
    with open("testCaseGeneration.txt", "r", encoding="utf-8") as f:
        message[0]["content"] = f.read()
    df = pd.read_csv("./examples/testcaseexample.csv")
    row_list = df.values.tolist()
    for item in row_list:
        example_use = {"role":"user",
                       "content":item[0]
                       }
        example_assistant = {"role":"assistant",
                                "content":item[1]}
        message.append(example_use)
        message.append(example_assistant)
    input = fixed_code+"\n"+"\n"+DFG
    testexample = {"role":"user",
                     "content":input}
    message.append(testexample)
    response = None
    while response is None:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=message,
                temperature=0,
                max_tokens=3000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                api_key=openai.api_key
            )
            return response.choices[0]["message"]["content"]
        except Exception as e:
            print(e)
            if str(type(e)) == "<class 'openai.error.InvalidRequestError'>":
                response = "null"
                break
            openai.api_key = "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"
            continue
    return response


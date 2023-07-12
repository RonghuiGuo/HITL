import openai
import pandas as pd
def DFG_generation(code):
    openai_key = "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"
    message = [{"role": "system"}]
    with open("DFG_js.txt", "r", encoding="utf-8") as f:
        message[0]["content"] = f.read()
    #read the csv file
    df = pd.read_csv("./examples/js_example.csv")
    row_list = df.values.tolist()
    for item in row_list:
        example_use = {"role": "user",
                   "content": item[0]
                   }
        example_assistant = {"role": "assistant",
                     "content": item[1]}
        message.append(example_use)
        message.append(example_assistant)
    testexample = {"role": "user",
                 "content": code}
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
                api_key=openai_key
            )
            return response.choices[0]["message"]["content"]
        except Exception as e:
            print(e)
            if str(type(e)) == "<class 'openai.error.InvalidRequestError'>":
                response = "null"
                break
            openai_key = "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"
            continue
    return response



def dfg_generation(code):
    response = DFG_generation(code)
    return response

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    code = """
function reverseString(str) {
  var reversedStr = "";
  for (var i = str.length - 1; i >= 0; i--) {
    reversedStr += str.charAt(i);
  }
  return reversedStr;
}
    """
    nodes_edges = dfg_generation(code)

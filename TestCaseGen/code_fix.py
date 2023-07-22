# !/user/bin/env python3
# -*- coding: utf-8 -*-
import openai
import re
import openai
openai.api_key = "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"
file_path = "../TestCaseGen/prompt_examples/code_fix_prompt.txt"

with open(file_path, "r") as file:
    code_fix_prompt = file.read()

def extract_code_block(text):
    pattern1 = r"'''([^`]+)'''"  # 3个单引号
    match = re.search(pattern1, text, re.DOTALL)

    if match:
        code = match.group(1)
        return code
    else:
        pattern2 = r"```([^`]+)```"  # 3个反引号
        match = re.search(pattern2, text, re.DOTALL)
        if match:
            code = match.group(1)
            return code
        else:
            return None

def code_fix_with_16k(prompt):
    example_error_1 = "console.log(\"Hello, World\";"
    example_answer_1 = """
        Code error identified: Syntax error
        Plan: FixSyntaxErrors(code)
        Fixed code:
        '''
        console.log("Hello, World");
        '''    
    """
    example_error_2 = """
        let i = 0;
        while (i < 5) {
          console.log(i);
          i++;
        }
        """
    example_answer_2 = "\"no error\""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role":"system","content": code_fix_prompt},
            {"role": "user", "content": "You should follow the sp above and output only the type of error and how to fix it."},
            {"role": "user", "content": example_error_1},
            {"role": "system", "content": example_answer_1},
            {"role": "user", "content": example_error_2},
            {"role": "system", "content": example_answer_2},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0

    )

    return response['choices'][0]['message']['content']

def fix_code(code):
    response = code_fix_with_16k(code)
    fixed_code_block = extract_code_block(response)
    return fixed_code_block.strip() if fixed_code_block else code.strip()

if __name__ == "__main__":
    code =  """
        function exampleFunc(a, b, c) {
        var result = 'Unknown';

        if (a > 10) {
          result = 'Path A';
        }

        if (b === true) {
          if (result === 'Path A') 
            result = 'Path A + B';
          } else {
            result = 'Path B';
          }
        }

        if (c < 0) 
          if (result === 'Path B') {
            result = 'Path B + C';
          } else {
            result = 'Path C';
          }
        }

          return result;
        }
    """
    fixed_code = fix_code(code)
    print(fixed_code)
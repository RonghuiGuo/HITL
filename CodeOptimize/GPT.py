from CodeOptimize.utils import *
import openai

class GPT:
    """
    This class represents an instance of the GPT language model.

    :Attributes: conversation (list): A list representing the conversation history.

    The class provides methods for adding few-shot examples, analyzing code snippets to retrieve Fully Qualified Names (FQNs) of APIs,
    generating code corrections based on user feedback, and generating feedback prompts for invalid and deprecated APIs.
    """

    def __init__(self):
        self.conversation = []

    def add_few_shot(self, few_shots: str) -> None:
        """
        Adds a few-shot example to the conversation.

        :param few_shots: A few-shot example to be added to the conversation. It should be a dictionary with the following keys:
        """
        self.conversation.append({"role": "system", "content": few_shots})

    def get_apis_in_code(self, code_snippet: str) -> list[str]:
        """
        Retrieves the list of Fully Qualified Names (FQNs) of APIs mentioned in a given code snippet.

        :param code_snippet: The code snippet to analyze and extract the APIs from.
        :return: The list of FQNs of APIs mentioned in the code snippet.
        """
        prompt = code_snippet + "\nList the FQNs"

        self.conversation.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=self.conversation,
            temperature=0.0
        )

        answer = response["choices"][0]["message"]["content"]

        self.conversation.append({"role": "assistant", "content": answer})

        fqn_list = get_method_fqn(answer)

        return fqn_list

    def feedback4correction(self, code_snippet: str, feedback: str) -> str:
        """
        Generates a corrected version of a code snippet based on user feedback.

        :param code_snippet: The original code snippet.
        :param feedback: The user's feedback on the code snippet.
        :return: The corrected code snippet.
        """
        prompt = code_snippet + "\n" + feedback
        self.conversation.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=self.conversation,
            temperature=0.0
        )

        corrected_code = response["choices"][0]["message"]["content"]

        self.conversation.append({"role": "assistant", "content": corrected_code})

        return corrected_code

    def generate_feedback_prompt(self, invalid_api_list: list, deprecated_api_list: list) -> str:
        """
        Generates a feedback prompt based on the lists of invalid and deprecated APIs.

        :param invalid_api_list: A list of invalid APIs.
        :param deprecated_api_list: A list of deprecated APIs.

        :return: The generated feedback prompt string.
        """
        prompts = []

        # Generate prompt strings for invalid methods
        invalid_prompts = [f'"{element}" is an invalid method, correct the invalid "{element}" method in the code.' for
                           element in invalid_api_list]
        prompts.extend(invalid_prompts)

        # Generate prompt strings for deprecated methods
        deprecated_prompts = [
            f'"{element}" is a deprecated method, update the deprecated "{element}" method in the code.' for element in
            deprecated_api_list]
        prompts.extend(deprecated_prompts)

        # Concatenate the prompt strings into a single string separated by \n
        prompt_string = "\n".join(prompts)

        return prompt_string

    def manual_add_response(self, response: str):
        self.conversation.append({"role": "assistant", "content": response})

    def clear_context_conversion(self):
        self.conversation.clear()

    def __str__(self):
        output = ""
        for conversation in self.conversation:
            output += str(conversation) + "\n"
        output = output.rstrip('\n')
        return output

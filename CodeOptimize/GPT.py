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
        prompt = code_snippet

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
        :param feedback: The feedback on the code snippet.
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

    def check_exceptions_handled(self, code_snippet: str, fqn: str, exception_to_check: str) -> bool:
        """
        Check if a specific exception is handled or caught for a given fully qualified name (fqn) in a code snippet.

        :param code_snippet: The code snippet to analyze for exception handling.
        :param fqn: The fully qualified name of the API associated with the exception.
        :param exception_to_check: The exception to check if it is handled or caught.
        :return: True if the exception is handled or caught in the code snippet, False otherwise.
        """

        exception_check_prompt = f"Is the {exception_to_check} handled or caught for {fqn} in the code snippet? Answer in Yes or No only."

        prompt = code_snippet + "\n" + exception_check_prompt
        self.conversation.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=self.conversation,
            temperature=0.0
        )

        answer = response["choices"][0]["message"]["content"]

        self.conversation.append({"role": "assistant", "content": answer})

        if answer.lower().startswith("no."):
            return False

        return True

    def add_exceptions(self, code_snippet: str, exceptions_feedback_prompt: str):
        """
        Adds exceptions to the provided code snippet based on the feedback prompt.

        :param code_snippet: The code snippet to which exceptions will be added.
        :param exceptions_feedback_prompt: The exceptions' feedback on the code snippet.
        :return: The corrected code snippet with added exceptions.
        """

        prompt = code_snippet + "/n" + exceptions_feedback_prompt
        self.conversation.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=self.conversation,
            temperature=0.0
        )

        corrected_code = response["choices"][0]["message"]["content"]

        self.conversation.append({"role": "assistant", "content": corrected_code})

        return corrected_code

    def generate_exceptions_prompts(self, exceptions_to_add: list[tuple[str, str, str]]) -> str:
        """
        Generates prompts for a given list of exceptions to add.

        :param exceptions_to_add: A list of triples (fqn, exception_to_add, condition) representing the exceptions to add.
        :return: A string containing the generated prompts for each exception.
        """
        exception_feedback_prompt = ""
        for fqn, exception_to_add, condition in exceptions_to_add:
            condition = condition.replace("This exception is thrown when ", "if ")
            exception_feedback_prompt += f"Please check {condition} for {fqn} in the given code snippet, otherwise throw {exception_to_add}.\n"

        return exception_feedback_prompt

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

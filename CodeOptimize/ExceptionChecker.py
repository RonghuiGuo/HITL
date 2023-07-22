from CodeOptimize.GPT import GPT
from CodeOptimize.utils import *

class ExceptionChecker:
    """
    This class checks and modifies a code snippet for unhandled exceptions.
    It adds exception handling and ensures all exceptions are properly handled.
    """

    def __init__(self, knowledge_graph: [dict], fqn_prompts: str, exception_check_prompts: str, exception_handle_prompts: str):
        self.knowledge_graph = knowledge_graph
        self.fqn_prompts = fqn_prompts
        self.exception_check_prompts = exception_check_prompts
        self.exception_handle_prompts = exception_handle_prompts

    def code_check(self, code_snippet: str):
        """
        Checks the code snippet for unhandled exceptions. It adds exception handling and ensures all exceptions are properly handled.

        :param code_snippet: The code snippet to check and modify for exception handling.
        :return: The modified code snippet with proper exception handling.
        """
        fqn_parser = GPT()
        fqn_parser.add_few_shot(self.fqn_prompts)

        exception_checker = GPT()
        exception_checker.add_few_shot(self.exception_check_prompts)

        exception_handle_generator = GPT()
        exception_handle_generator.add_few_shot(self.exception_handle_prompts)

        while True:

            excpt_to_add_list = []
            unhandled_exceptions_set = set()

            fqn_list = fqn_parser.get_apis_in_code(code_snippet)
            print("Extracting Fully Qualified Names...")
            for index, fqn in enumerate(fqn_list, start=1):
                print(f"    {index}. {fqn}")
            print()

            print(f"Checking whether APIs contain unhandled exceptions...")
            for fqn in fqn_list:
                exceptions_dict_list = get_exceptions_to_handle(fqn, self.knowledge_graph)
                if exceptions_dict_list:
                    for exception_dict in exceptions_dict_list:
                        exception_to_handle = exception_dict["exception"]
                        condition = exception_dict["condition"]
                        handled = exception_checker.check_exceptions_handled(code_snippet, fqn, exception_to_handle)

                        if handled:
                            continue

                        excpt_to_add_list.append((fqn, exception_to_handle, condition))
                        unhandled_exceptions_set.add(exception_to_handle)
                        print(f"    \'{exception_to_handle}\' is not handled for \\{fqn}\'!")

            if not excpt_to_add_list:
                print(f"All exceptions are appropriately handled within the code!\n")
                break

            print(f"There are a total of {len(unhandled_exceptions_set)} unhandled exceptions in the code. Now proceeding to correct the code accordingly...\n")
            exception_feedback_prompt = exception_handle_generator.generate_exceptions_prompts(excpt_to_add_list)
            corrected_code = exception_handle_generator.add_exceptions(code_snippet, exception_feedback_prompt)

            code_snippet = corrected_code
            print(f"Done! Now rechecking the exceptions to ensure they are properly handled...\n")

        return code_snippet
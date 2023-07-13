from GPT import GPT
from CodeOptimize.utils import *

class CodeChecker:
    """
    This class performs a code check and correction process for invalid and deprecated APIs in a given code snippet.
    """

    def __init__(self, knowledge_graph: [dict], fqn_prompts: str, code_generate_prompts: str):
        self.knowledge_graph = knowledge_graph
        self.fqn_prompts = fqn_prompts
        self.code_generate_prompts = code_generate_prompts

    def code_check(self, code_snippet: str, max_loop = 10):
        """
        Performs a code check and correction process for invalid and deprecated APIs in a given code snippet.
        Uses two instances of the GPT language model: 'fqn_parser' for extracting Fully Qualified Names (FQNs) of APIs
        and 'code_generator' for generating code corrections based on feedback.

        :param code_snippet: The code snippet to check and correct.
        :param max_loop: (optional) The maximum number of loops to run for checking and correcting APIs. Defaults to 10.
        :return: The corrected code snippet.
        """
        fqn_parser = GPT()
        fqn_parser.add_few_shot(self.fqn_prompts)

        code_generator = GPT()
        code_generator.add_few_shot(self.code_generate_prompts)

        loop_count = 0

        while loop_count < max_loop:

            fqn_list = fqn_parser.get_apis_in_code(code_snippet)
            print("Extracting Fully Qualified Names...")
            for index, fqn in enumerate(fqn_list, start=1):
                print(f"    {index}. {fqn}")
            print()

            invalid_api_list = []
            deprecated_api_list = []

            print(f"Checking invalid/deprecated APIs...")
            for fqn in fqn_list:
                valid = check_valid(fqn, self.knowledge_graph)
                if not valid:
                    invalid_api_list.append(fqn)
                    continue
                deprecated = check_deprecated(valid)
                if deprecated:
                    deprecated_api_list.append(fqn)

            if not invalid_api_list and not deprecated_api_list:
                print(f"No invalid APIs present in the code. ")
                print(f"No deprecated APIs present in the code")
                print(f"The number of iterations used to rectify the code: {loop_count + 1}")
                print(f"Done.\n")
                break

            if loop_count + 1 == max_loop:
                print(f"The maximum loop limit of {max_loop} has been reached!")
                if len(invalid_api_list) > 0:
                    print(f"There are still {len(invalid_api_list)} invalid APIs present in the code:")
                    for fqn in invalid_api_list:
                        print(f"    * {fqn}")
                    print()
                else:
                    print("No invalid APIs present in the code.")

                if len(deprecated_api_list) > 0:
                    print(f"There are still {len(deprecated_api_list)} deprecated APIs present in the code:")
                    for fqn in deprecated_api_list:
                        print(f"    *. {fqn}")
                    print()
                else:
                    print("No deprecated APIs present in the code.\n")

                break

            if len(invalid_api_list) > 0:
                print(f"{len(invalid_api_list)} invalid APIs found:")
                for fqn in invalid_api_list:
                    print(f"    * {fqn}")
                print()
            else:
                print(f"{len(invalid_api_list)} invalid APIs found.")

            if len(deprecated_api_list) > 0:
                print(f"{len(deprecated_api_list)} deprecated APIs found:")
                for fqn in deprecated_api_list:
                    print(f"    *. {fqn}")
                print()
            else:
                print(f"{len(deprecated_api_list)} deprecated APIs found.")
                print()

            print(f"Providing feedback on invalid or deprecated APIs to rectify the code...")

            feedback_prompt = code_generator.generate_feedback_prompt(invalid_api_list, deprecated_api_list)
            corrected_code = code_generator.feedback4correction(code_snippet, feedback_prompt)
            code_snippet = corrected_code
            loop_count += 1
            print(f"Done! Now rechecking the code to ensure there are no invalid or deprecated APIs...\n")

        return code_snippet
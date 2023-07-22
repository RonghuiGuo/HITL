from code_fix import fix_code
from chatGPT_api import get_result
from javascript_DFG import DFG_generation
from testcase import get_testcase

def main(code_file_path):
    #Intermediate Results are stored in the Results folder
    with open(code_file_path, 'r') as f:
        code = f.read()
    fixed_code = fix_code(code)
    with open('Results/fixed_code.txt', 'w') as f:
        f.write(fixed_code)
        f.close()
    CFG = get_result()
    with open('Results/CFG.txt', 'w') as f:
        f.write(CFG)
        f.close()
    DFG = DFG_generation(fixed_code)
    with open('Results/DFG.txt', 'w') as f:
        f.write(DFG)
        f.close()
    test_case = get_testcase(fixed_code, DFG)
    with open('Results/test_case.txt', 'w') as f:
        f.write(test_case)
        f.close()

if __name__ == '__main__':
    #example file path: ../TestCaseGen/example code/original code.txt
    code_file_path = input("Please provide the file path where a JavaScript function is stored:\n")
    main(code_file_path)






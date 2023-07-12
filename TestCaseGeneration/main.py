from code_fix import fix_code
from chatGPT_api import get_result
from javascript_DFG import DFG_generation
from testcase import get_testcase
if __name__ == '__main__':
    with open('original code.txt', 'r') as f:
        code = f.read()
    print("Original code:")
    print(code)
    print("---------------------------------------")
    print("Checking and fixing the code...")
    fixed_code = fix_code(code)
    print("---------------------------------------")
    print("fixed code:")
    print(fixed_code)
    # write the code to the txt
    with open('test_code.txt', 'w') as f:
        f.write(fixed_code)
        f.close()
    print("---------------------------------------")
    print("start generating the CFG...")
    print("---------------------------------------")
    CFG = get_result()
    print(CFG)
    print("---------------------------------------")
    print("Start genrating the DFG...")
    #write the CFG to the txt
    with open('CFG.txt', 'w') as f:
        f.write(CFG)
        f.close()
    print("---------------------------------------")
    DFG = DFG_generation(fixed_code)
    print(DFG)
    print("---------------------------------------")
    print("Start generating the test cases...")
    #write the DFG to the txt
    with open('DFG.txt', 'w') as f:
        f.write(DFG)
        f.close()
    print("---------------------------------------")
    test_case = get_testcase(fixed_code, DFG)
    print(test_case)






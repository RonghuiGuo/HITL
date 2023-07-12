import random
import sys
import webbrowser
import time
import os
import zipfile
import sqlite3
import gradio as gr
from utils.log import Logger
from pathlib import Path
from utils.CodeGeneration import CodeGeneration
from utils.utils import zip_folder, iframe_generator
from database.DB_Tools import DB_Tools
from dotenv import load_dotenv

# ----------log----------------
sys.stdout = Logger("logs/logs.log")
load_dotenv()

if __name__ == "__main__":

    codegeneration = CodeGeneration()
    db_tools = DB_Tools()

    def read_logs():
        sys.stdout.flush()
        with open("logs/logs.log", "r") as f:
            return f.read()
    # ----------log----------------

    # create a static directory to store the static files
    static_dir = Path(codegeneration.args.static_dir)
    static_dir.mkdir(parents=True, exist_ok=True)
    #

    def fn_scenario_generation(input_feature):
        print("fn_scenario_generation")
        # 数据库
        feature2scenarios_list = db_tools.select_all()

        similar_Feature2Scenarios = codegeneration.TopN_Feature2Scenarios(feature2scenarios_list, input_feature)
        print("Gherkin generating")
        Gherkin_response, messages = codegeneration.Gherkin_generation(input_feature, similar_Feature2Scenarios)
        print("Scenario Parsing")
        Scenarios_List = codegeneration.Scenario_Parsing(Gherkin_response)
        print("Gherkin2NL")
        Gherkin_NL_List = codegeneration.Gherkin2NL(Scenarios_List, messages)

        output_dict = {}
        for i in range(len(Gherkin_NL_List)):
            output_dict[globals()["scenarios_list"][i]] = gr.update(visible=True)
            output_dict[globals()["scenarios_list"][i].children[0].children[0]] = gr.update(value=Gherkin_NL_List[i])
        for i in range(codegeneration.args.max_scenarios_number-len(Gherkin_NL_List)):
            output_dict[globals()["scenarios_list"][i+len(Gherkin_NL_List)]] = gr.update(visible=False)
            output_dict[globals()["scenarios_list"][i+len(Gherkin_NL_List)].children[0].children[0]] = gr.update(value="")
        output_dict[globals()["scenario_add"]] = gr.update(visible=True)
        output_dict[globals()["code_output"]] = gr.update(visible=False)
        return output_dict

    def fn_scenario_add(*arg):
        print("fn_scenario_add")

        input_string = arg[-1]
        scenarios_string_list = list(arg[:-1])
        for i in range(codegeneration.args.max_scenarios_number):
            if scenarios_string_list[i] == "":
                return {globals()["scenarios_list"][i]: gr.update(visible=True), globals()["scenarios_list"][i].children[0].children[0]: input_string}

    def fn_code_generation(*args):
        print("fn_code_generation")
        codegeneration.clear_static_html_dir()
        # print(args)
        # 数据库保存

        Gherkin_NL_List = []
        for i in range(len(args)-1):
            if args[i] != "":
                Gherkin_NL_List.append(args[i])

        input_feature = args[-1]

        db_tools.insert(input_feature, Gherkin_NL_List)
        print("NL2Gherkin")
        # time.sleep(2)
        Gherkin_result = codegeneration.NL2Gherkin(Gherkin_NL_List, input_feature)
        print("Design_page_template_generation")
        Design_page_template = codegeneration.Design_page_template_generation(Gherkin_result)
        print("Visual_design_template_generation")
        Visual_design_template = codegeneration.Visual_design_template_generation(Design_page_template)
        print("Code_generation")
        Generated_code, loop_number = codegeneration.Code_generation(Visual_design_template, Design_page_template, input_feature, Gherkin_result)

        file_path = static_dir/"html/index.html"
        file_name = "index.html"
        link = f'<a href="file={file_path}" target="_blank">{file_name}</a>'

        iframe = iframe_generator(file_path)

        output_path = os.path.join(static_dir, "html.zip")
        zip_folder(folder_path=codegeneration.args.static_html_dir, output_path=output_path)

        return link, gr.update(visible=True), output_path, Generated_code, iframe

    def fn_download_file():
        output_path = os.path.join(static_dir, "html.zip")
        zip_folder(folder_path=codegeneration.args.static_html_dir, output_path=output_path)
        return output_path

    def fn_code_modification(code_modification_suggestion_string, generated_code):
        codegeneration.clear_static_html_dir()
        print("Code_Modification")
        modified_code, messages, loop_number = codegeneration.Code_Modification(generated_code, code_modification_suggestion_string)
        output_path = os.path.join(static_dir, "html.zip")
        zip_folder(folder_path=codegeneration.args.static_html_dir, output_path=output_path)

        file_path = static_dir/"html/index.html"
        file_name = "index.html"
        link = f'<a href="file={file_path}" target="_blank">{file_name}</a>'
        iframe = iframe_generator(file_path)

        return link, output_path, modified_code, iframe

    def fn_design_modification(code_modification_suggestion_string, generated_code):
        codegeneration.clear_static_html_dir()
        print("Design_Modification")
        modified_code, messages, loop_number = codegeneration.Design_Modification(generated_code, code_modification_suggestion_string)
        output_path = os.path.join(static_dir, "html.zip")
        zip_folder(folder_path=codegeneration.args.static_html_dir, output_path=output_path)

        file_path = static_dir/"html/index.html"
        file_name = "index.html"
        link = f'<a href="file={file_path}" target="_blank">{file_name}</a>'
        iframe = iframe_generator(file_path)

        return link, output_path, modified_code, iframe

    with gr.Blocks(title="Human in the loop") as app:

        generated_code_state = gr.State(value="")

        with gr.Row() as Feature_Block:
            feature_textbox = gr.Textbox(label="Your Feature", lines=3, placeholder="Please input your feature here...", scale=9)
            scenario_generation_btn = gr.Button(value="Scenario Generation", scale=1)

        scenarios_list = []
        scenarios_textbox_list = []

        with gr.Column() as Scenarios_Block:
            with gr.Box():
                for i in range(codegeneration.args.max_scenarios_number):
                    if i < codegeneration.args.init_visible_scenarios_number:
                        with gr.Row(visible=True) as globals()["scenario_{i}"]:
                            globals()["scenario_textbox_{i}"] = gr.Textbox(interactive=True, label=f"Scenario", lines=2, scale=9)
                            globals()["del_btn_{i}"] = gr.Button(value="Del", scale=1)

                            def change_vis():
                                return gr.update(value=""), gr.update(visible=False)
                            globals()["del_btn_{i}"].click(fn=change_vis,inputs=None, outputs=[globals()["scenario_textbox_{i}"], globals()["scenario_{i}"]])
                    else:
                        with gr.Row(visible=False) as globals()["scenario_{i}"]:
                            globals()["scenario_textbox_{i}"] = gr.Textbox(interactive=True, label=f"Scenario", lines=2, scale=9)
                            globals()["del_btn_{i}"] = gr.Button(value="Del", scale=1)

                            def change_vis():
                                return gr.update(value=""), gr.update(visible=False)
                            globals()["del_btn_{i}"].click(fn=change_vis, inputs=None,outputs=[globals()["scenario_textbox_{i}"], globals()["scenario_{i}"]])

                    scenarios_list.append(globals()["scenario_{i}"])
                    scenarios_textbox_list.append(globals()["scenario_textbox_{i}"])

            with gr.Column(visible=False) as globals()["scenario_add"]:
                with gr.Row():
                    globals()["scenario_add_textbox"] = gr.Textbox(interactive=True, label="Your new scenario:", lines=2, scale=9)
                    scenario_add_btn = gr.Button(value="Add", scale=1)
                code_generation_btn = gr.Button(value="Code Generation")

                html_markdown = gr.Markdown(label="Output HTML")

            with gr.Column(visible=False) as globals()["code_output"]:
                # html_markdown = gr.Markdown(label="Output HTML")
                # download_btn = gr.Button(value="Download Button")
                with gr.Column():
                    # download_btn = gr.Button(value="Download Button")
                    gr_download_file = gr.File()
                    html = gr.HTML(label="HTML preview", show_label=True)
                    pass
                with gr.Row():
                    globals()["design_modification_textbox"] = gr.Textbox(label="Design Modification Suggestions", scale=9)
                    code_design_modification_btn = gr.Button(value="Design Modification", scale=1)
                with gr.Row():
                    globals()["code_modification_textbox"] = gr.Textbox(label="Code Modification Suggestions", scale=9)
                    code_modification_btn = gr.Button(value="Code Modification", scale=1)

            # with gr.Column(visible=True) as globals()["web_block"]:
            #     x1=gr.HTML(open('RandomRollCallPage_2/index.html','r').read())

        scenario_generation_btn_outputs = []
        scenario_generation_btn_outputs = scenarios_list+scenarios_textbox_list
        scenario_generation_btn_outputs.append(globals()["scenario_add"])
        scenario_generation_btn_outputs.append(globals()["code_output"])
        scenario_generation_btn.click(fn=fn_scenario_generation, inputs=feature_textbox, outputs=scenario_generation_btn_outputs)

        scenario_add_btn_inputs = []
        scenario_add_btn_inputs.extend(scenarios_textbox_list)
        scenario_add_btn_inputs.append(globals()["scenario_add_textbox"])
        scenario_add_btn_outputs = []
        scenario_add_btn_outputs = scenarios_list+scenarios_textbox_list
        scenario_add_btn_outputs.append(globals()["scenario_add"])

        scenario_add_btn.click(fn=fn_scenario_add, inputs=scenario_add_btn_inputs, outputs=scenario_add_btn_outputs)

        code_generation_btn_inputs = []
        code_generation_btn_inputs.extend(scenarios_textbox_list)
        code_generation_btn_inputs.append(feature_textbox)

        code_generation_btn.click(fn=fn_code_generation, inputs=code_generation_btn_inputs, outputs=[html_markdown, globals()["code_output"], gr_download_file, generated_code_state, html])
        # code_generation_btn.click(fn=fn_code_generation_btn)

        # download_btn.click(fn=download_file, outputs=globals()["download_file"])
        # download_btn.click(fn=fn_download_file, outputs=gr_download_file)

        code_modification_btn.click(fn=fn_code_modification, inputs=[globals()["code_modification_textbox"], generated_code_state],
                                    outputs=[html_markdown, gr_download_file, generated_code_state, html])
        code_design_modification_btn.click(fn=fn_design_modification, inputs=[globals()["design_modification_textbox"], generated_code_state],
                                           outputs=[html_markdown, gr_download_file, generated_code_state, html])

        logs = gr.Textbox(label="Log", max_lines=5)
        app.load(read_logs, None, logs, every=1, queue=True, scroll_to_output=True)

    app.queue()
    # app.launch(show_error=True)
    app.launch()


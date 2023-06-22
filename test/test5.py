import gradio as gr

input_textbox = gr.Textbox()

with gr.Blocks() as demo:
    # 提供示例输入给input_textbox，示例输入以嵌套列表形式设置
    gr.Examples(["hello", "bonjour", "merhaba"], input_textbox)
    # render函数渲染input_textbox
    input_textbox.render()
demo.launch()

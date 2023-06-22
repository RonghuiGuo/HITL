import gradio as gr

with gr.Blocks() as demo:
    with gr.Row():
        # gr.Image("lion.jpg", scale=2)
        # gr.Image("tiger.jpg", scale=1)
        gr.Textbox(label="First")
        gr.Textbox(label="Last")
    with gr.Group():
        # gr.Image("lion.jpg", scale=2)
        # gr.Image("tiger.jpg", scale=1)
        gr.Textbox(label="First")
        gr.Textbox(label="Last")
    with gr.Box():
        gr.Textbox(label="First")
        gr.Textbox(label="Last")
demo.launch()
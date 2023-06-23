import gradio as gr


with gr.Blocks() as demo:
    food_box = gr.Number(value=10, label="Food Count")

    food_box2=gr.Number(label="Food Count")
    status_box = gr.Textbox()
    def eat(food):
        if food > 0:
            return {food_box2: food - 1, status_box: "full"}
        else:
            return {status_box: "hungry"}
        
    gr.Button("EAT").click(
        fn=eat, 
        inputs=food_box,
        outputs=[food_box2, status_box]
    )

demo.launch()

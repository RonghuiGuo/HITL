
import gradio as gr

table = gr.Dataframe([[1, 2, 3], [4, 5, 6]])
gallery = gr.Gallery([("cat.jpg", "Cat"), ("dog.jpg", "Dog")])
textbox = gr.Textbox("Hello World!")

statement = gr.Textbox()


def on_select(evt: gr.SelectData):  # SelectData is a subclass of EventData
    return f"You selected {evt.value} at {evt.index} from {evt.target}"

with gr.Blocks() as app:
    table.select(on_select, None, statement)
    gallery.select(on_select, None, statement)
    textbox.select(on_select, None, statement)

app.launch()
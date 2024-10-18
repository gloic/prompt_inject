import gradio as gr

from extensions.prompt_inject.wildcards_manager import WildcardManager

params = {
    "display_name": "Prompt Inject",
    "is_tab": False,

    "manager": {
        "base_path": "extensions/prompt_inject/prompts",
        "is_model_warning": True,
        "left_pattern": "__",
        "right_pattern": "__"
    }
}


def chat_input_modifier(text, visible_text, state):
    """
    Modifies the user input string in chat mode (visible_text).
    You can also modify the internal representation of the user
    input (text) to change how it will appear in the prompt.
    """

    manager = WildcardManager(params['manager'])

    if not manager.contains_wildcards(text):
        return text, visible_text

    text = manager.replace_wildcard(text)

    return text, visible_text


def ui():
    with gr.Accordion("Prompt Inject", open=False, elem_classes="Prompt Inject"):
        with gr.Row():
            model_warning = gr.Checkbox(value=params['manager']['is_model_warning'], label='Model warning', info="If enabled, the model warn you when an unknown wildcard is used.")
            model_warning.change(lambda x: params['manager'].update({'is_model_warning': x}), model_warning, None)

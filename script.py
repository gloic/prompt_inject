import gradio as gr

from extensions.prompt_inject.wildcards_manager import WildcardManager

params = {
    "display_name": "Prompt Inject",
    "is_tab": False,

    "manager": {
        "base_path": "extensions/prompt_inject/prompts",
        "suffix_language": None,
        "is_model_warning": True,
        "error_wildcard_not_found": '\nWildcard error : the wildcard "{}" has no corresponding file. Please give me a short and concise warning that this wildcard cannot be resolved.\n',
        "patterns": {
            "left": "__",
            "right": "__",
            "and": '&&',
            "or": '||'
        }
    }
}


def setup():
    global manager
    manager = WildcardManager(params['manager'])


def chat_input_modifier(text, visible_text, state):
    """
    Modifies the user input string in chat mode (visible_text).
    You can also modify the internal representation of the user
    input (text) to change how it will appear in the prompt.
    """
    # manager = WildcardManager(params['manager'])

    if not manager.contains_wildcards(text):
        return text, visible_text

    text = manager.replace_wildcard(text)
    return text, visible_text


def ui():
    with gr.Accordion("Prompt Inject", open=False, elem_classes="Prompt Inject"):
        with gr.Row():
            model_warning = gr.Checkbox(value=params['manager']['is_model_warning'], label='Model warning', info="If enabled, the model warn you when an unknown wildcard is used.")
            model_warning.change(lambda x: params['manager'].update({'is_model_warning': x}), model_warning, None)

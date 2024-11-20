from extensions.prompt_inject.wildcard_manager_ui import WildcardManagerUI
from extensions.prompt_inject.wildcards_manager import WildcardManager

params = {
    "display_name": "Prompt Inject",
    "is_tab": False,

    "manager": {
        "base_path": "extensions/prompt_inject/prompts",
        "suffix_language": None,
        "is_model_warning": True,
        "error_wildcard_not_found": '\nWildcard error : the wildcard "{}" has no corresponding file, give me a short and concise warning indicating this wildcard cannot be resolved.\n',
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
    global extension_ui
    manager = WildcardManager(params['manager'])
    extension_ui = WildcardManagerUI(params['manager'], manager)


def chat_input_modifier(text, visible_text, state):
    """
    Modifies the user input string in chat mode (visible_text).
    You can also modify the internal representation of the user
    input (text) to change how it will appear in the prompt.
    """
    return manager.process(text, visible_text)


def ui():
    """
    Gets executed when the UI is drawn. Custom gradio elements and
    their corresponding event handlers should be defined here.

    To learn about gradio components, check out the docs:
    https://gradio.app/docs/
    """
    extension_ui.generate()

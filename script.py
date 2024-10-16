from transformers import LogitsProcessor

from extensions.prompt_inject.wildcards_manager import WildcardManager

params = {
    "display_name": "Prompt Inject",
    "is_tab": False,
    "extension": ".txt"
}


class MyLogits(LogitsProcessor):
    """
    Manipulates the probabilities for the next token before it gets sampled.
    Used in the logits_processor_modifier function below.
    """

    def __init__(self):
        pass

    def __call__(self, input_ids, scores):
        # probs = torch.softmax(scores, dim=-1, dtype=torch.float)
        # probs[0] /= probs[0].sum()
        # scores = torch.log(probs / (1 - probs))
        return scores


def chat_input_modifier(text, visible_text, state):
    """
    Modifies the user input string in chat mode (visible_text).
    You can also modify the internal representation of the user
    input (text) to change how it will appear in the prompt.
    """

    manager = WildcardManager()

    if not manager.contains_wildcards(text):
        return text, visible_text

    text = manager.replace_wildcard(text)

    return text, visible_text

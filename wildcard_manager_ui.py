import gradio as gr


class WildcardManagerUI:
    def __init__(self, params, manager):
        self.params = params
        self.manager = manager

    def generate(self):
        with gr.Accordion("Prompt Inject", open=True, elem_classes="Prompt Inject"):
            with gr.Row():
                model_warning = gr.Checkbox(value=self.params['is_model_warning'], label='Model warning', info="If enabled, the model warns when an unknown wildcard is used.")


            def update_and_apply(is_model_warning):
                self.params.update({'is_model_warning': is_model_warning})
                self.manager._apply_params(self.params)

            model_warning.change(update_and_apply, model_warning, None)

from extensions.prompt_inject.tests.wildcard_manager.base_wildcard_manager import BaseWildcardManagerTest


class TestWildcardManager_config(BaseWildcardManagerTest):

    def test_should_add_error_message_when_wildcard_does_not_exist(self):
        text = 'it does not __unknown__'
        self.manager.is_model_warning = True
        self.manager.error_wildcard_not_found = '\nerror "{}" not found\n'

        result = self.manager._replace_wildcard(text)

        self.assertEqual('it does not \nerror "unknown" not found\n', result)

    def test_should_return_raw_wildcard_when_it_does_not_exist(self):
        text = 'it does not __unknown__'
        self.manager.is_model_warning = False

        result = self.manager._replace_wildcard(text)

        self.assertEqual('it does not unknown', result)

    def test_should_use_default_prompt_when_no_suffix_language_is_defined(self):
        self.create_file('hello.txt', "Hello")
        self.manager.suffix_language = None
        text = '__hello__'

        result = self.manager._replace_wildcard(text)

        self.assertEqual('Hello', result)

    def test_should_use_configured_suffix_language(self):
        self.create_file('hello-fr.txt', "Bonjour")
        self.manager.suffix_language = 'fr'
        text = '__hello__'

        result = self.manager._replace_wildcard(text)

        self.assertEqual('Bonjour', result)

    def test_should_use_default_file_if_suffixed_is_not_found(self):
        self.create_file('hello.txt', "Hello")
        self.manager.suffix_language = 'fr'
        text = '__hello__'

        result = self.manager._replace_wildcard(text)

        self.assertEqual('Hello', result)

    def test_should_use_file_when_no_language_set(self):
        self.create_file('schueberfouer-lu.txt', "Gromperekichelcher")
        self.manager.suffix_language = None
        text = '__schueberfouer-lu__'

        result = self.manager._replace_wildcard(text)

        self.assertEqual('Gromperekichelcher', result)

    def test_should_replace_when_custom_pattern_is_configured(self):
        self.create_file('custom.txt', "design is very human")
        self.manager.left_pattern = "}}"
        self.manager.right_pattern = "-@!-"
        text = '}}custom-@!-'

        result = self.manager._replace_wildcard(text)

        self.assertEqual('design is very human', result)

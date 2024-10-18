from extensions.prompt_inject.tests.wildcard_manager.base_wildcard_manager import BaseWildcardManagerTest


class TestWildcardManager_config(BaseWildcardManagerTest):

    def test_should_warn_the_user_when_wildcard_does_not_exist(self):
        text = 'it does not __exist__'
        self.manager.is_model_warning = True

        result = self.manager.replace_wildcard(text)

        self.assertEqual(
            'it does not \nSyntax error : wildcard "exist" not found : the wildcard "exist" has no corresponding file. Please warn the user in a very short and concise message that this wildcard cannot be resolved.\n',
            result)

import os

from extensions.prompt_inject.tests.wildcard_manager.base_wildcard_manager import BaseWildcardManagerTest


class TestWildcardManager_commands(BaseWildcardManagerTest):

    def setUp(self):
        super().setUp()

        # self.special_dir = os.path.join(self.test_dir, "specials")
        # os.makedirs(self.special_dir, exist_ok=True)

        # self.create_file('exclamation_mark.txt', "This is important", self.special_dir)
        # self.create_file('question_mark.txt', "This is a question", self.special_dir)
        # self.create_file('ampersand.txt', "This is COT", self.special_dir)

    def test_should_contains_command_wildcard(self):
        text = '+something'

        result = self.manager._contains_command(text)

        self.assertTrue(result)

    def test_should_create_a_new_file(self):
        text = ('__+something__\n'
                'the design is very human')
        visible_text = text

        text, visible_text = self.manager.process(text, visible_text)

        self.assertEqual('the design is very human', text)
import os

from extensions.prompt_inject.tests.wildcard_manager.base_wildcard_manager import BaseWildcardManagerTest


class TestWildcardManager_specials(BaseWildcardManagerTest):

    def setUp(self):
        super().setUp()

        self.special_dir = os.path.join(self.test_dir, "specials")
        os.makedirs(self.special_dir, exist_ok=True)

        self.create_file('exclamation_mark.txt', "This is important", self.special_dir)
        self.create_file('question_mark.txt', "This is a question", self.special_dir)
        self.create_file('ampersand.txt', "This is COT", self.special_dir)

    def test_should_retrieve_special_wildcard_content(self):
        text = 'specials/exclamation_mark'

        result = self.manager._get_wildcard_content(text)

        self.assertEqual(result, 'This is important')

    def test_should_contains_specials_wildcards(self):
        text = '!special'

        result = self.manager._contains_special(text)

        self.assertTrue(result)

    def test_should_not_contains_specials_wildcards(self):
        text = 'special'

        result = self.manager._contains_special(text)

        self.assertFalse(result)

    def test_should_replace_special_wildcards(self):
        text = '__!__'

        result = self.manager._replace_wildcard(text)

        self.assertEqual('This is important', result)

    def test_should_replace_multiple_special_wildcards(self):
        text = '__!?__'

        result = self.manager._replace_wildcard(text)

        self.assertEqual('This is importantThis is a question', result)

    def test_should_replace_special_wildcards_with_text(self):
        self.create_file('hello.txt', "Hello")

        exclamation_result = self.manager._replace_wildcard('__!hello__')
        question_result = self.manager._replace_wildcard('__?hello__')
        cot_result = self.manager._replace_wildcard('__&hello__')

        self.assertEqual('This is importantHello', exclamation_result)
        self.assertEqual('This is a questionHello', question_result)
        self.assertEqual('This is COTHello', cot_result)

    def test_should_replace_special_nested_wildcards(self):
        self.create_file('hello.txt', "Hello __name__, __&riddle__")
        self.create_file('name.txt', "Bob")
        self.create_file('riddle.txt', "I am the one who I am but not what you are")

        result = self.manager._replace_wildcard('__!hello__')

        self.assertEqual('This is importantHello Bob' ', This is COTI am the one who I am but not what you are', result)

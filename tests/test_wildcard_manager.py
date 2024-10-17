import os
import tempfile
import unittest

from extensions.prompt_inject.wildcards_manager import WildcardManager


class TestWildcardManager(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.sub_dir = os.path.join(self.test_dir, "sub")
        self.special_dir = os.path.join(self.test_dir, "specials")

        os.makedirs(self.sub_dir, exist_ok=True)
        os.makedirs(self.special_dir, exist_ok=True)

        self.create_file('exclamation_mark.txt', "This is important", self.special_dir)
        self.create_file('question_mark.txt', "This is a question", self.special_dir)
        self.create_file('ampersand.txt', "This is COT", self.special_dir)

        self.manager = WildcardManager(self.test_dir)

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def create_file(self, filename, content, dir=None):
        if dir is None:
            dir = self.test_dir
        with open(os.path.join(dir, filename), 'w') as file:
            file.write(content)

    def test_should_check_if_contains_wildcards(self):
        self.assertTrue(self.manager.contains_wildcards('This is a __test__'))
        self.assertFalse(self.manager.contains_wildcards('This is a text without wildcards'))

    def test_should_retrieve_content(self):
        self.create_file('name.txt', "Bobby")

        result = self.manager.get_wildcard_content('name')

        self.assertEqual(result, 'Bobby')

    def test_should_retrieve_content_from_subfolder(self):
        sub_dir = os.path.join(self.test_dir, "sub")
        os.makedirs(sub_dir, exist_ok=True)
        with open(os.path.join(sub_dir, 'name.txt'), 'w') as file:
            file.write('Bobby')

        result = self.manager.get_wildcard_content('sub/name')

        self.assertEqual(result, 'Bobby')

    def test_should_replace_wildcards(self):
        self.create_file('content.txt', "working")
        text = 'it\'s __content__'

        result = self.manager.replace_wildcard(text)

        self.assertEqual(result, 'it\'s working')

    def test_should_replace_nested_wildcards(self):
        self.create_file('parent.txt', "Parent and __nested__")
        self.create_file('nested.txt', "Nested")
        text = '__parent__'

        result = self.manager.replace_wildcard(text)

        self.assertEqual(result, 'Parent and Nested')

    def test_should_retrieve_special_wildcard_content(self):
        text = 'specials/exclamation_mark'

        result = self.manager.get_wildcard_content(text)

        self.assertEqual(result, 'This is important')

    def test_should_check_if_contains_specials_wildcards(self):
        self.assertTrue(self.manager.contains_special('!special'))
        self.assertFalse(self.manager.contains_special('special'))

    def test_should_replace_special_wildcards(self):
        text = '__!__'

        result = self.manager.replace_wildcard(text)

        self.assertEqual(result, 'This is important')

    def test_should_replace_multiple_special_wildcards(self):
        text = '__!?__'

        result = self.manager.replace_wildcard(text)

        self.assertEqual(result, 'This is importantThis is a question')

    def test_should_replace_special_wildcards_with_text(self):
        self.create_file('hello.txt', "Hello")

        exclamation_result = self.manager.replace_wildcard('__!hello__')
        question_result = self.manager.replace_wildcard('__?hello__')
        cot_result = self.manager.replace_wildcard('__&hello__')

        self.assertEqual(exclamation_result, 'This is importantHello')
        self.assertEqual(question_result, 'This is a questionHello')
        self.assertEqual(cot_result, 'This is COTHello')

    def test_should_replace_special_nested_wildcards(self):
        self.create_file('hello.txt', "Hello __name__, __&riddle__")
        self.create_file('name.txt', "Bob")
        self.create_file('riddle.txt', "I am the one who I am but not what you are")

        result = self.manager.replace_wildcard('__!hello__')

        self.assertEqual(result, 'This is importantHello Bob, This is COTI am the one who I am but not what you are')


if __name__ == '__main__':
    unittest.main()

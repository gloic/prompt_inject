import os
import tempfile
import unittest

from wildcards_manager import WildcardManager


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
        with_wildcard = 'This is a __test__'
        without_wildcards = 'This is a text without wildcards'

        result_with = self.manager.contains_wildcards(with_wildcard)
        result_without = self.manager.contains_wildcards(without_wildcards)

        self.assertTrue(result_with)
        self.assertFalse(result_without)

    def test_should_retrieve_content(self):
        self.create_file('name.txt', "Bobby")

        result = self.manager.get_wildcard_content('name')

        self.assertEqual('Bobby', result)

    def test_should_retrieve_content_from_subfolder(self):
        self.create_file('name.txt', "Bobby", self.sub_dir)

        result = self.manager.get_wildcard_content('sub/name')

        self.assertEqual('Bobby', result)

    def test_should_replace_wildcards(self):
        self.create_file('Content.txt', "working")
        text = 'it\'s __Content__'

        result = self.manager.replace_wildcard(text)

        self.assertEqual('it\'s working', result)

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

        self.assertEqual('This is important', result)

    def test_should_replace_multiple_special_wildcards(self):
        text = '__!?__'

        result = self.manager.replace_wildcard(text)

        self.assertEqual('This is importantThis is a question', result)

    def test_should_replace_special_wildcards_with_text(self):
        self.create_file('hello.txt', "Hello")

        exclamation_result = self.manager.replace_wildcard('__!hello__')
        question_result = self.manager.replace_wildcard('__?hello__')
        cot_result = self.manager.replace_wildcard('__&hello__')

        self.assertEqual('This is importantHello', exclamation_result)
        self.assertEqual('This is a questionHello', question_result)
        self.assertEqual('This is COTHello', cot_result)

    def test_should_replace_special_nested_wildcards(self):
        self.create_file('hello.txt', "Hello __name__, __&riddle__")
        self.create_file('name.txt', "Bob")
        self.create_file('riddle.txt', "I am the one who I am but not what you are")

        result = self.manager.replace_wildcard('__!hello__')

        self.assertEqual('This is importantHello Bob'
                         ', This is COTI am the one who I am but not what you are', result)

    def test_should_concat_multiple_wildcards(self):
        self.create_file('part1.txt', "Part1")
        self.create_file('part2.txt', "Part2")

        result = self.manager.replace_wildcard('__part1&& part2__')

        self.assertEqual('Part1Part2', result)

    def test_should_return_random_wildcards(self):
        self.create_file('odd.txt', "Odd")
        self.create_file('even.txt', "Even")
        self.create_file('Ded.txt', "Ded", self.sub_dir)
        expected_values = ['Odd', 'Even', 'Ded']

        result = self.manager.replace_wildcard('__odd || even || sub/Ded__')

        self.assertIn(result, expected_values)


if __name__ == '__main__':
    unittest.main()

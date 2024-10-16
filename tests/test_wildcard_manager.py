import os
import tempfile
import unittest

from extensions.prompt_inject.wildcards_manager import WildcardManager


class TestWildcardManager(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.sub_dir = os.path.join(self.test_dir, "sub")
        self.special_dir = os.path.join(self.test_dir, "special")

        os.makedirs(self.sub_dir, exist_ok=True)
        os.makedirs(self.special_dir, exist_ok=True)

        self.manager = WildcardManager(self.test_dir)

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def create_file(self, filename, content):
        with open(os.path.join(self.test_dir, filename), 'w') as file:
            file.write(content)

    def test_should_check_if_contains_wildcards(self):
        self.assertTrue(self.manager.contains_wildcards('This is a __test__'))
        self.assertFalse(self.manager.contains_wildcards('This is a text without wildcards'))

    def test_should_retrieve_content(self):
        self.create_file('name.txt', "Bobby")

        content = self.manager.get_wildcard_content('name')

        self.assertEqual(content, 'Bobby')

    def test_should_retrieve_content_from_subfolder(self):
        sub_dir = os.path.join(self.test_dir, "sub")
        os.makedirs(sub_dir, exist_ok=True)
        with open(os.path.join(sub_dir, 'name.txt'), 'w') as file:
            file.write('Bobby')

        content = self.manager.get_wildcard_content('sub/name')

        self.assertEqual(content, 'Bobby')

    def test_should_replace_wildcards(self):
        self.create_file('content.txt', "working")

        text = 'it\'s __content__'
        replaced_text = self.manager.replace_wildcard(text)

        self.assertEqual(replaced_text, 'it\'s working')

    def test_should_replace_nested_wildcards(self):
        self.create_file('parent.txt', "Parent and __nested__")
        self.create_file('nested.txt', "Nested")

        text = '__parent__'
        replaced_text = self.manager.replace_wildcard(text)

        self.assertEqual(replaced_text, 'Parent and Nested')

    def test_should_check_if_contains_specials_wildcards(self):
            self.assertTrue(self.manager.contains_special('!special'))
            self.assertFalse(self.manager.contains_special('special'))

if __name__ == '__main__':
    unittest.main()

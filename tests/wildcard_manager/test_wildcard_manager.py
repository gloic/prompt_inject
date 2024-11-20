from extensions.prompt_inject.tests.wildcard_manager.base_wildcard_manager import BaseWildcardManagerTest


class TestWildcardManager(BaseWildcardManagerTest):

    def test_should_process_prompt(self):
        self.create_file('something.txt', "something")
        text = ('__something__')
        visible_text = text

        text, visible_text = self.manager.process(text, visible_text)

        self.assertEqual('something', text)

    def test_should_contains_wildcards(self):
        text = 'This is a __test__'

        result_with = self.manager._contains_wildcards(text)

        self.assertTrue(result_with)

    def test_should_not_contains_wildcards(self):
        text = 'This is a text without wildcards'

        result = self.manager._contains_wildcards(text)

        self.assertFalse(result)

    def test_should_retrieve_content(self):
        self.create_file('name.txt', "Bobby")

        result = self.manager._get_wildcard_content('name')

        self.assertEqual('Bobby', result)

    def test_should_retrieve_content_from_subfolder(self):
        self.create_file('name.txt', "Bobby", self.sub_dir)

        result = self.manager._get_wildcard_content('sub/name')

        self.assertEqual('Bobby', result)

    def test_should_replace_wildcard(self):
        self.create_file('Content.txt', "working")
        text = 'it\'s __Content__'

        result = self.manager._replace_wildcard(text)

        self.assertEqual('it\'s working', result)

    def test_should_replace_nested_wildcards(self):
        self.create_file('parent.txt', "Parent and __nested__")
        self.create_file('nested.txt', "Nested")
        text = '__parent__'

        result = self.manager._replace_wildcard(text)

        self.assertEqual(result, 'Parent and Nested')

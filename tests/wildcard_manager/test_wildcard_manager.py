from extensions.prompt_inject.tests.wildcard_manager.base_wildcard_manager import BaseWildcardManagerTest


class TestWildcardManager(BaseWildcardManagerTest):

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

    def test_should_replace_wildcard(self):
        self.create_file('Content.txt', "working")
        text = 'it\'s __Content__'

        result = self.manager.replace_wildcard(text)

        self.assertEqual('it\'s working', result)

    def test_should_return_wildcard_when_it_not_exists(self):
        text = 'it does not __exist__'
        self.manager.is_model_warning = False

        result = self.manager.replace_wildcard(text)

        self.assertEqual('it does not exist', result)

    def test_should_replace_nested_wildcards(self):
        self.create_file('parent.txt', "Parent and __nested__")
        self.create_file('nested.txt', "Nested")
        text = '__parent__'

        result = self.manager.replace_wildcard(text)

        self.assertEqual(result, 'Parent and Nested')

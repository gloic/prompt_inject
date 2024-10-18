import os
import tempfile
import unittest

from extensions.prompt_inject.wildcards_manager import WildcardManager


class BaseWildcardManagerTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.sub_dir = os.path.join(self.test_dir, "sub")
        self.special_dir = os.path.join(self.test_dir, "specials")

        os.makedirs(self.sub_dir, exist_ok=True)
        os.makedirs(self.special_dir, exist_ok=True)

        self.create_file('exclamation_mark.txt', "This is important", self.special_dir)
        self.create_file('question_mark.txt', "This is a question", self.special_dir)
        self.create_file('ampersand.txt', "This is COT", self.special_dir)

        params = {
            "base_path": self.test_dir,
            "left_pattern": "__",
            "right_pattern": "__",
            "is_model_warning": "False",
        }
        self.manager = WildcardManager(params)

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

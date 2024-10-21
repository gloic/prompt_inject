import os
import tempfile
import unittest

from extensions.prompt_inject.wildcards_manager import WildcardManager


class BaseWildcardManagerTest(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.sub_dir = os.path.join(self.test_dir, "sub")

        os.makedirs(self.sub_dir, exist_ok=True)

        params = {
            "base_path": self.test_dir,
            "language": "en",
            "patterns": {
                "left": "__",
                "right": "__",
                "and": "&&",
                "or": "||"
            },
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

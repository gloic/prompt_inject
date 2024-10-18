import unittest

from extensions.prompt_inject.tests.wildcard_manager.test_wildcard_manager import TestWildcardManager
from extensions.prompt_inject.tests.wildcard_manager.test_wildcard_manager_combos import TestWildcardManager_combos
from extensions.prompt_inject.tests.wildcard_manager.test_wildcard_manager_config import TestWildcardManager_config
from extensions.prompt_inject.tests.wildcard_manager.test_wildcard_manager_specials import TestWildcardManager_specials


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestWildcardManager))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestWildcardManager_config))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestWildcardManager_specials))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestWildcardManager_combos))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
import os
import re


class WildcardManager:
    def __init__(self, base_path='extensions/prompt_inject/prompts'):
        self.base_path = base_path
        # self.left_pattern = '__'
        # self.right_pattern = '__'

        self.specials = {
            '!', 'exclamation_mark',
            '?', 'question_mark',
            '&', 'ampersand'
        }

    def contains_wildcards(self, text):
        """
        Returns true when the input text contains at least one wildcard.
        """
        return re.search(r'__(.*?)__', text) is not None

    def contains_special(self, match):
        first = match[0]
        return first in self.specials

    def replace_specials(self, match):
        print('cucu')

    def replace_wildcard(self, text):
        matches = re.findall(r'__(.*?)__', text)

        for match in matches:
            specials_content = self.replace_specials(match)
            content = self.get_wildcard_content(match)
            if content is not None:
                text = text.replace('__' + match + '__', content)

        return text

    def get_wildcard_content(self, match):
        filename = match + ".txt"
        file_path = os.path.join(self.base_path, *filename.split('/'))
        if os.path.exists(file_path):
            print("File found:", file_path)
            with open(file_path, "r") as file:
                content = file.read().strip()
                if self.contains_wildcards(content):
                    return self.replace_wildcard(content)
                else:
                    return content
        else:
            return None

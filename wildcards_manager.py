import os
import re


class WildcardManager:
    def __init__(self, base_path='extensions/prompt_inject/prompts'):
        self.base_path = base_path
        # self.left_pattern = '__'
        # self.right_pattern = '__'

        self.specials_dir = 'specials/'
        self.specials = {
            '!': 'exclamation_mark',
            '?': 'question_mark',
            '&': 'ampersand'
        }

    def contains_wildcards(self, text):
        """
        Returns true when the input text contains at least one wildcard.
        """
        return re.search(r'__(.*?)__', text) is not None

    def contains_special(self, wildcard):
        """
        Returns true when the input text contains at least one special wildcard.
        """
        if wildcard:
            first = wildcard[0]
            return first in self.specials

    def replace_wildcard(self, text):
        """
        Process a given string by replacing all wildcards and specials wildcard recursively.
        Returns retrieved value of the wildcard
        """
        matches = re.finditer(r'__(.*?)__', text)

        for match in matches:
            wildcard = match.group(1)
            special_content, wildcard = self.process_specials(wildcard)
            content = self.get_wildcard_content(wildcard)

            if special_content or content:
                text = text.replace('__' + match.group(1) + '__', special_content + content)

        return text

    def process_specials(self, wildcard):
        special_content = ''

        while self.contains_special(wildcard):
            current = wildcard[0]
            wildcard = wildcard[1:]
            current_content = self.get_special_content(current)
            if current_content is not None:
                special_content += current_content

        return special_content, wildcard

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
            return ''

    def get_special_content(self, wildcard):
        special = self.specials_dir + self.specials.get(wildcard)
        return self.get_wildcard_content(special)

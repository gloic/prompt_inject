import os
import re
import random


class WildcardManager:
    def __init__(self, base_path='extensions/prompt_inject/prompts'):
        self.base_path = base_path
        self.left_pattern = '__'
        self.right_pattern = '__'
        self.and_pattern = '&&'
        self.or_pattern = '||'

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
        left = self.left_pattern
        right = self.right_pattern
        return re.search(f'{left}(.*?){right}', text) is not None

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
        left = self.left_pattern
        right = self.right_pattern
        matches = re.finditer(f'{left}(.*?){right}', text)

        for match in matches:
            wildcards = match.group(1)
            special_content, wildcards = self.process_specials(wildcards)

            content = ''
            wildcards = self.process_or(wildcards)

            for wildcard in wildcards.split(self.and_pattern):
                content += self.get_wildcard_content(wildcard.strip())

            if special_content or content:
                text = text.replace(self.left_pattern + match.group(1) + self.right_pattern, special_content + content)

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

    def process_or(self, wildcards):
        if self.or_pattern in wildcards:
            wildcard = wildcards.split(self.or_pattern)
            return random.choice(wildcard).strip()

        return wildcards

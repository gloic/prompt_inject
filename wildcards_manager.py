import os
import random
import re


class WildcardManager:
    def __init__(self, params):

        # TODO - replace this
        # base_path='extensions/prompt_inject/prompts'

        self.base_path = params.get('base_path')
        self.left_pattern = params.get('left_pattern')
        self.right_pattern = params.get('right_pattern')
        self.is_model_warning = params.get('is_model_warning')

        # Combos
        self.and_pattern = '&&'
        self.or_pattern = '||'

        # Specials
        self.specials_dir = 'specials/'
        self.specials = {
            '!': 'exclamation_mark',
            '?': 'question_mark',
            '&': 'ampersand'
        }

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

            # Special pattern
            special_content, wildcards = self.process_specials(wildcards)

            # OR pattern
            wildcards = self.process_or(wildcards)

            content = ''
            # AND pattern
            for wildcard in wildcards.split(self.and_pattern):
                content += self.get_wildcard_content(wildcard.strip())

            if special_content or content:
                text = text.replace(self.left_pattern + match.group(1) + self.right_pattern, special_content + content)

        return text

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

    def process_specials(self, wildcard):
        """
        Process specials wildcards in the given wildcard.
        Returns concatenated special content and updated value of 'wildcard' without the specials chars.
        """
        special_content = ''

        while self.contains_special(wildcard):
            current = wildcard[0]
            wildcard = wildcard[1:]
            current_content = self.get_special_content(current)
            if current_content is not None:
                special_content += current_content

        return special_content, wildcard

    def get_content_prompt_file(self, wildcard):
        """
        Returns the prompt corresponding to a given wildcard. If the file cannot be found, return the wildcard itself.
        """
        filename = wildcard + ".txt"
        file_path = os.path.join(self.base_path, *filename.split('/'))
        if os.path.exists(file_path):
            print("File found:", file_path)
            with open(file_path, "r") as file:
                return file.read().strip()

        if self.is_model_warning:
            return '\nSyntax error : wildcard "' + wildcard + '" not found : the wildcard "' + wildcard + '" has no corresponding file. Please warn the user in a very short and concise message that this wildcard cannot be resolved.\n'
        else:
            return wildcard

    def get_wildcard_content(self, wildcard):
        if not wildcard:
            return ''

        content = self.get_content_prompt_file(wildcard)
        # Handle nested wildcards if needed
        if self.contains_wildcards(content):
            return self.replace_wildcard(content)
        else:
            return content

    def get_special_content(self, wildcard):
        """
        Returns content of a special wildcard.
        """
        special = self.specials_dir + self.specials.get(wildcard)
        return self.get_wildcard_content(special)

    def process_or(self, wildcards):
        """
        Return randomly one wildcard if the OR pattern is present in the input string
        """
        if self.or_pattern in wildcards:
            wildcard = wildcards.split(self.or_pattern)
            return random.choice(wildcard).strip()

        return wildcards
import random
import re

from extensions.prompt_inject.utils.file_util import FilesUtil


class WildcardManager:
    def __init__(self, params):
        self.apply_params(params)
        self.file_util = FilesUtil()

        # Specials
        self.specials_dir = 'specials/'
        self.specials = {
            '!': 'exclamation_mark',
            '?': 'question_mark',
            '&': 'ampersand'
        }

    def apply_params(self, params):
        self.base_path = params.get('base_path')
        self.suffix_language = params.get('suffix_language')

        patterns = params.get('patterns')
        self.left_pattern = patterns.get('left')
        self.right_pattern = patterns.get('right')
        self.and_pattern = patterns.get('and')
        self.or_pattern = patterns.get('or')

        self.is_model_warning = params.get('is_model_warning')
        self.error_wildcard_not_found = params.get('error_wildcard_not_found')

    def replace_wildcard(self, text):
        """
        Process a given string by replacing all wildcards and specials wildcard recursively.
        Returns retrieved value of the wildcard
        """
        if not self.contains_wildcards(text):
            return text

        left = self.left_pattern
        right = self.right_pattern
        for match in re.finditer(f'{left}(.*?){right}', text):
            wildcards = match.group(1)

            # Special pattern
            special_content, wildcards = self.process_specials(wildcards)

            # OR pattern
            wildcards = self.process_or(wildcards, self.or_pattern)

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
        left_pattern = self.left_pattern
        right_pattern = self.right_pattern
        return re.search(f'{left_pattern}(.*?){right_pattern}', text) is not None

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

    def get_missing_wildcard_warning_message(self, wildcard):
        return self.error_wildcard_not_found.format(wildcard)

    def handle_missing_wildcard(self, wildcard):
        if self.is_model_warning:
            return self.get_missing_wildcard_warning_message(wildcard)
        else:
            return wildcard

    def get_content_prompt_file(self, wildcard):
        """
        Returns the prompt corresponding to a given wildcard. If the file cannot be found, return the wildcard itself.
        """
        file_path = self.file_util.get_file_path(wildcard, self.base_path, self.suffix_language)
        file_content = self.file_util.get_file_content(file_path)
        if file_content:
            return file_content
        else:
            return self.handle_missing_wildcard(wildcard)

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

    def process_or(self, wildcards, or_pattern):
        """
        Return randomly one wildcard if the OR pattern is present in the input string
        """
        if or_pattern in wildcards:
            wildcard = wildcards.split(or_pattern)
            return random.choice(wildcard).strip()

        return wildcards

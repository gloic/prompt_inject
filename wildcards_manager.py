import random
import re

from extensions.prompt_inject.utils.file_util import FilesUtil


class WildcardManager:
    def __init__(self, params):
        self._apply_params(params)
        self.file_util = FilesUtil()

        # Specials
        self.specials_dir = 'specials/'
        self.specials = {
            '!': 'exclamation_mark',
            '?': 'question_mark',
            '&': 'ampersand'
        }

        # Commands
        self.commands = {
            '+': 'ADD',
            '*': 'EDIT',
            '-': 'DELETE'
        }

    def process(self, text, visible_text):
        if self._contains_wildcards(text):

            self._process_command(text, visible_text)

            text = self._replace_wildcard(text)

        return text, visible_text

    def _apply_params(self, params):
        self.base_path = params.get('base_path')
        self.suffix_language = params.get('suffix_language')

        patterns = params.get('patterns')
        self.left_pattern = patterns.get('left')
        self.right_pattern = patterns.get('right')
        self.and_pattern = patterns.get('and')
        self.or_pattern = patterns.get('or')

        self.is_model_warning = params.get('is_model_warning')
        self.error_wildcard_not_found = params.get('error_wildcard_not_found')

    def _replace_wildcard(self, text):
        """
        Process a given string by replacing all wildcards and specials wildcard recursively.
        Returns retrieved value of the wildcard
        """
        if not self._contains_wildcards(text):
            return text

        left = self.left_pattern
        right = self.right_pattern
        for match in re.finditer(f'{left}(.*?){right}', text):
            wildcards = match.group(1)

            # Special pattern
            special_content, wildcards = self._process_specials(wildcards)

            # OR pattern
            wildcards = self._process_or(wildcards, self.or_pattern)

            content = ''
            # AND pattern
            for wildcard in wildcards.split(self.and_pattern):
                content += self._get_wildcard_content(wildcard.strip())

            if special_content or content:
                text = text.replace(self.left_pattern + match.group(1) + self.right_pattern, special_content + content)

        return text

    def _contains_wildcards(self, text):
        """
        Returns true when the input contains at least one wildcard.
        """
        left_pattern = self.left_pattern
        right_pattern = self.right_pattern
        return re.search(f'{left_pattern}(.*?){right_pattern}', text) is not None

    def _contains_special(self, wildcard):
        """
        Returns true when the input contains at least one special wildcard.
        """
        if wildcard:
            first = wildcard[0]
            return first in self.specials

    def _contains_command(self, wildcard):
        """
        Returns true when the input contains a command.
        """
        if wildcard:
            first = wildcard[0]
            return first in self.commands

    def _process_specials(self, wildcard):
        """
        Process specials wildcards in the given wildcard.
        Returns concatenated special content and updated value of 'wildcard' without the specials chars.
        """
        special_content = ''

        while self._contains_special(wildcard):
            current = wildcard[0]
            wildcard = wildcard[1:]
            current_content = self._get_special_content(current)
            if current_content is not None:
                special_content += current_content

        return special_content, wildcard

    def _get_missing_wildcard_warning_message(self, wildcard):
        return self.error_wildcard_not_found.format(wildcard)

    def _handle_missing_wildcard(self, wildcard):
        if self.is_model_warning:
            return self._get_missing_wildcard_warning_message(wildcard)
        else:
            return wildcard

    def _get_content_prompt_file(self, wildcard):
        """
        Returns the prompt corresponding to a given wildcard. If the file cannot be found, return the wildcard itself.
        """
        file_path = self.file_util.get_file_path(wildcard, self.base_path, self.suffix_language)
        file_content = self.file_util.get_file_content(file_path)
        if file_content:
            return file_content
        else:
            return self._handle_missing_wildcard(wildcard)

    def _get_wildcard_content(self, wildcard):
        if not wildcard:
            return ''

        content = self._get_content_prompt_file(wildcard)

        # Handle nested wildcards if needed
        if self._contains_wildcards(content):
            return self._replace_wildcard(content)
        else:
            return content

    def _get_special_content(self, wildcard):
        """
        Returns content of a special wildcard.
        """
        special = self.specials_dir + self.specials.get(wildcard)
        return self._get_wildcard_content(special)

    def _process_or(self, wildcards, or_pattern):
        """
        Return randomly one wildcard if the OR pattern is present in the input string
        """
        if or_pattern in wildcards:
            wildcard = wildcards.split(or_pattern)
            return random.choice(wildcard).strip()

        return wildcards

    def _process_command(self, text):
        if self._contains_command(text):

            # extract command

            # remove command
            # execute command

            return text

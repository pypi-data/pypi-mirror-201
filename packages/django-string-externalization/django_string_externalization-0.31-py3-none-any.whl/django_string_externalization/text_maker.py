import sys

from django.conf import settings
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from .html_util import markdown, sanitize_html

from .text_entry_manager import TextEntryManager


def force_str(str_or_proxy):
    return str_or_proxy + ""


class TextMakerError(Exception):
    pass


class TextMakerCreator:
    def __init__(self, global_keys, text_files):
        self.validate_text_files(text_files)

        self.entry_manager = TextEntryManager(text_files)
        self.entry_manager.load()
        self.global_keys = global_keys

    def get_language_code(self):
        # when called from a non-localized URL (e.g. admin), get_language() is None
        return get_language() or "en"

    @staticmethod
    def validate_text_files(text_files):
        for path in text_files:
            if path.startswith("."):
                raise TextMakerError(f"don't start paths with './' offender: {path}")
            if not path.endswith(".text.yaml"):
                raise TextMakerError("files must have the '.text.yaml' extension")

    def get_tm_func(self):
        return lazy(self._tm, str)

    def _tm(
        self,
        key,
        allow_md=True,
        extra_keys={},
        sanitize_input=True,
        sanitize_output=True,
        should_mark_safe=True,
    ):
        lang = self.get_language_code() 
        global_keys = self.global_keys[lang]

        if sanitize_input is True:
            extra_keys = {
                k: self.sanitize_html(force_str(v)) for k, v in extra_keys.items()
            }

        if key in global_keys:
            return global_keys[key]

        elif self.entry_manager.has_entry(key):
            entry = self.entry_manager.get_entry(key)

        else:
            raise TextMakerError(f"text key {key} doesn't exist")

        if allow_md is False and entry.get("md", False):
            raise TextMakerError("requested key contains markdown")

        try:
            if lang in entry:
                text = entry[lang] or f"FIXME: {key}"
            else:
                text = f"FIXME: {entry['en']}"

            if entry.get("md"):
                text = self.render_markdown(text)

            template_args = {**global_keys, **extra_keys}

            text = text % template_args

            if sanitize_output:
                text = self.sanitize_html(text)

            if should_mark_safe:
                return mark_safe(text)
            else:
                return text

        except Exception as e:
            raise TextMakerError(
                f"text_key {key} with arguments: {extra_keys} had the following error \n {e}"
            )

    @staticmethod
    def sanitize_html(text):
        """can override w/ custom html sanitizer"""
        return sanitize_html(text)

    @staticmethod
    def render_markdown(text):
        """can override w/ custom markdown renderer"""
        return markdown(text)


class WatchingTextMakerCreator(TextMakerCreator):
    def __init__(self, global_keys, text_files):
        super().__init__(global_keys, text_files)

        if settings.DEBUG and sys.argv[1] in ("runserver", "rs"):
            self.start_watch()

    def start_watch(self):
        # pylint: disable="import-outside-toplevel relative-beyond-top-level"
        from .text_watcher import text_watcher

        text_watcher.add_entry_watcher(self.entry_manager)
        text_watcher.start_watching()

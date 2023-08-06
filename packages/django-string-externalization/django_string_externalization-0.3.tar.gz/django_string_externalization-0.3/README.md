# django_string_externalization

This is a tool for django apps to externalize their strings into yaml files. Messages for multiple languages are co-located in the same file. This is ideal for bilingual apps. 

```yaml
page_title:
    en: "My App"
    fr: "Mon App"

```

You can define translations accross multiple files.

## Usage

First, you'll want to create a yaml file with your strings. File names must end with `.text.yaml`.


```yaml
# mytext.text.yaml

page_title:
    en: "My App"
    fr: "Mon App"

# variables 

welcome_message:
    en: Welcome %(firstname)s %(lastname)s
    fr: Bienvenue %(firstname)s %(lastname)s

the_current_year_is:
    en: The current year is %(current_year)s
    fr: L'année en cours est %(current_year)s

```

Then, you'll want to create a `TextMakerCreator` object: `TextMakerCreator(global_keys, text_files).`

Global keys are an optional concept that let you define variables available to all of your text entries. 

```python
global_keys = {
    "en" : { "current_year" : "2019-20" },
    "fr" : { "current_year" : "2019-2020" },
}

tm = TextMakerCreator(global_keys, ["my_app/mytext.text.yaml"]).get_tm_func()

tm("page_title") == "My App"
tm("welcome_message", extra_keys={"firstname":"Alex", "lastname": "Leduc"}) == "Welcome Alex Leduc"
tm("the_current_year_is") == "The current year is 2019-20"

```

You can create many text-maker functions, with indepedent or overlapping text files. This is useful if you want isolated possibly name-clashing text entries. 


## Watching 

If you're using django's dev-server, you can use `WatchingTextMakerCreator` instead, and it will reload text entries when the yaml files change. 

**If you use the watching feature, you'll need watchdog installed. This library supports version 2**


## Sanitization and markdown

HTML is sanitized by default, using this whitelist of tags,

```python
ALLOWED_TAGS = ["a", "b", "em", "i", "li", "ol", "p", "strong", "ul", "br", "div"]
```

You can disable sanitization by passing `sanitize_output=False` to the `tm` function. Inputs (`extra_args`) will still be sanitized, unless you also pass `sanitize_input=False`.

You can provide custom sanization and markdown logic by overriding the TextMaker's class `render_markdown` and `sanitize` methods. 

**Unless you override these methods, you must install the `mistune` (version 2) and `bleach` (version 3) packages**

## Pitfalls and gotchas

- `tm()` returns lazy objects which resolve and behave like strings, this can trip up some packages like `openpyxl` when it tries to write these objects to cells. You can force the lazy object to resolve by performing string operations, e.g. `tm("title")+""`. Simply calling `str(tm("title"))` will not work.
- If you want to use the `%` character in a string, you'll need to escape it with itself `%%`
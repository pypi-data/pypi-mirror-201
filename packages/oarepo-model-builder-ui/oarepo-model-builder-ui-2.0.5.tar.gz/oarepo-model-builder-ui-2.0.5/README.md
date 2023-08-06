<!--
 Copyright (c) 2022 CESNET

 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# UI model builder plugin

An [OARepo Model Builder](https://github.com/oarepo/oarepo-model-builder) plugin to generate
user interface layout from model specification.

## Installation

```bash
pip install oarepo-model-builder-ui
```

## Usage

The plugin adds support for UI annotation of the model file:

```yaml
title:
  type: keyword
  label.key: title.label
  label.cs: Název
  label.en: Title
  help.key: title.help
  hint.key: title.hint
  ui:
    detail: <detail component name>
    edit: <edit component name>
    // any other property here - not validated
```

The following files are generated:

```text
<package>
  +- model
    +- ui.json 
  +- templates
    +- <langcode>
      +- LC_MESSAGES
        +- messages.po
        +- messages.mo
```

### i18n

The `po` and `mo` files are standard gettext po files. The translation keys 
are taken from the `*.key` properties. If keys are not specified, they are
generated from the property path (for example, metadata.creator.firstName.label ).

### UI layout

The UI layout is generated as a convenience for other tools, for example for `oarepo-cli`.
It contains simplified layout of the model. Example:

```json
{
  "children": {
    "title": {
      "detail": "fulltext",
      "input": "fulltext",
      "help": "title.help",
      "label": "title.label",
      "hint": "title.hint"
    },
    "providers": {
      "detail": "array",
      "input": "array",
      "help": "providers.help",
      "label": "providers.label",
      "hint": "providers.hint",
      "child": {
        "detail": "provider",
        "input": "provider",
        "children": {
          "name": {
            "detail": "keyword",
            "input": "keyword",
            "help": "providers/name.help",
            "label": "providers/name.label",
            "hint": "providers/name.hint"
          }
        }
      }
    }
  }
}
```

Fields:
 * detail: component used for rendering the detail page
 * input: component used for rendering input
 * help/label/hint: keys to gettext message catalogues
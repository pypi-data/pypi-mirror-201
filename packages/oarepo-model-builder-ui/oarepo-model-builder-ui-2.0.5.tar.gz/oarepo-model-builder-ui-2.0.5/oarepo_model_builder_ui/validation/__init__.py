from langcodes.language_lists import CLDR_LANGUAGES
from oarepo_model_builder_ui.config import UI_ITEMS
from marshmallow import fields as ma_fields
import marshmallow as ma


def create_ui_property_validator():
    # TODO: inefficient as it adds cca 300 fields on schema but ok for now
    fields = {}
    for fld in UI_ITEMS:
        for lang in ["key", *CLDR_LANGUAGES]:
            fields[f"{fld}.{lang}"] = ma_fields.String(required=False)
    fields["i18n.key"] = ma_fields.String(required=False)
    return type("UIPropertyValidator", (ma.Schema,), fields)


UIPropertyValidator = create_ui_property_validator()


class UISettingsValidator(ma.Schema):
    i18n_languages = ma_fields.List(
        ma_fields.String(), default=["en"], data_key="i18n-languages"
    )


class ModelSettingsValidator(ma.Schema):
    translations_setup_cfg = ma_fields.String(data_key="translations-setup-cfg")
    ui_layout = ma_fields.String(data_key="ui-layout")


class UIPropertySection(ma.Schema):
    detail = ma_fields.String(required=False)
    edit = ma_fields.String(required=False)

    class Meta:
        unknown = ma.INCLUDE


class UIPropertySectionValidator(ma.Schema):
    ui = ma_fields.Nested(UIPropertySection, required=False)


validators = {
    "property-ui": [UIPropertySection],
    "property": [UIPropertyValidator],
    "settings": [UISettingsValidator],
    "model": [ModelSettingsValidator],
}

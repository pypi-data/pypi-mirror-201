from pathlib import Path
from oarepo_model_builder.model_preprocessors import ModelPreprocessor


class LayoutSettingsPreprocessor(ModelPreprocessor):
    TYPE = "ui_layout_settings"

    def transform(self, schema, settings):
        # settings.setdefault("layout", "ui/layout.yaml")
        schema.current_model.setdefault(
            "translations-setup-cfg", schema.current_model["package"]
        )
        output_file_name = str(
            Path(schema.current_model["saved-model-file"]).parent / "ui.json"
        )
        schema.current_model.setdefault("ui-layout", output_file_name)

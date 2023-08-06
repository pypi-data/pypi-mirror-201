import json
from typing import List
import inflect

from oarepo_model_builder.builder import ModelBuilder
from oarepo_model_builder.builders import process
from oarepo_model_builder.builders.json_base import JSONBaseBuilder
from oarepo_model_builder.property_preprocessors import PropertyPreprocessor
from oarepo_model_builder.utils.verbose import log

from oarepo_model_builder_ui.config import UI_ITEMS

"""
Will generate:
metadata: {
  // contents of ui child here
  label: <label.key>
  hint: <hint.key>
  help: <help.key>
  children: {
    k: child_def
  }, // or 
  child: {
    ...
  }
}
// invenio_stuff_here

it will be saved to package/model/ui.json
"""


class InvenioLayoutBuilder(JSONBaseBuilder):
    TYPE = "ui-layout"
    output_file_type = "json"
    output_file_name = "ui-layout"

    @process("**", condition=lambda current, stack: stack.schema_valid)
    def model_element(self):
        ui = {}
        data = self.stack.top.data
        schema_element_type = self.stack.top.schema_element_type

        if isinstance(data, dict):
            ui.update({k.replace("-", "_"): v for k, v in data.get("ui", {}).items()})
            if "type" in data:
                t = data["type"]
                if t in ("object", "nested"):
                    t = inflect.engine().singular_noun(
                        [
                            x.key
                            for x in self.stack
                            if x.key and x.schema_element_type == "property"
                        ][-1].lower()
                    )
                ui.setdefault("detail", t)
                ui.setdefault("input", t)

        leave = True
        if schema_element_type == "property":
            for fld in UI_ITEMS:
                ui[fld] = data.get(
                    f"{fld}.key",
                    "/".join(
                        x.key
                        for x in self.stack
                        if x.schema_element_type == "property" and x.key
                    )
                    + f".{fld}",
                )

            self.output.enter(self.stack.top.key, {})
        elif schema_element_type == "properties":
            self.output.enter("children", {})
        elif schema_element_type == "items":
            self.output.enter("child", {})
        else:
            leave = False
        self.output.merge(ui)
        self.build_children()
        if leave:
            self.output.leave()

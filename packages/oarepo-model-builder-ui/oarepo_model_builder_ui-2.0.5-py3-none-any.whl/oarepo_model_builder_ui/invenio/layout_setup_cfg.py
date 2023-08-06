from pathlib import Path
from oarepo_model_builder.utils.jinja import package_name

from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.outputs.cfg import CFGOutput


class InvenioLayoutSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_layout_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        output.add_entry_point(
            "oarepo.ui",
            self.current_model.package,
            f"{self.current_model.package}.models:{Path(self.current_model.ui_layout).name}",
        )

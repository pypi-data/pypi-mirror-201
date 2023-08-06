import json
import os
from pathlib import Path

# project_templates is named pt to avoid too long paths on Windows
DEFAULT_LOCATION = Path(__file__).parent.parent / "pt"


class ProjectTemplateLoader:
    def __init__(self, default_location: str = DEFAULT_LOCATION) -> None:
        self.default_location = Path(default_location)

    def load_project_template(self, name: str):
        cutter_file = f"{name}/cookiecutter.json"

        cutter_files = list(self.default_location.rglob(f"**/{cutter_file}"))

        assert len(cutter_files) > 0, f"{name} project template not found."

        return cutter_files[0].parent

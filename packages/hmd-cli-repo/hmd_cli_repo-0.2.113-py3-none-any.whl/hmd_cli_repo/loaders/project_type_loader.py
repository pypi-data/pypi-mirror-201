import json
from pathlib import Path


DEFAULT_LOCATION = Path(__file__).parent / ".." / "project_types"


class ProjectTypeLoader:
    def __init__(self, default_location: str = DEFAULT_LOCATION) -> None:
        self.default_location = Path(default_location)

    def load_project_type(self, name: str):
        config_file = f"{name}.prj_type.json"

        config_files = list(self.default_location.rglob(f"**/{config_file}"))

        assert len(config_files) > 0, f"{name} project type not found."

        with open(config_files[0], "r") as cfg:
            return json.load(cfg)

    def list_project_types(self, category: str = None):
        project_types = list(self.default_location.rglob("**/*.prj_type.json"))

        types = []

        for prj_type in project_types:
            with open(prj_type, "r") as pt:
                type_def = json.load(pt)
                type_cat = type_def.get("category", "Other")

                if category is None or type_cat == category:
                    types.append(type_def["name"])

        return sorted(types)

    def list_project_type_categories(self):
        project_types = list(self.default_location.rglob("**/*.prj_type.json"))

        cats = set()

        for prj_type in project_types:
            with open(prj_type, "r") as pt:
                type_def = json.load(pt)
                cats.add(type_def.get("category", "Other"))

        return sorted(cats)

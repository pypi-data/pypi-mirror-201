from pathlib import Path


class CustomSampleData:

    def __init__(self, path: Path) -> None:
        self.folderContent = path.glob("*")

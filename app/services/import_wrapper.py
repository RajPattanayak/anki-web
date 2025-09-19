from pathlib import Path
from typing import Dict, Any
from anki.pylib.anki.importing import AnkiPackageImporter
from anki.pylib.anki.importing import TextImporter
# from anki.pylib.anki.importing import CsvFileImporter
# from anki.pylib.anki.importing import AnkiPackageImporter
from app.services.anki_bridge import AnkiBridge

class ImportWrapper:
    """
    Wrapper class around Anki's importing system.
    Handles file-type detection and standardized response.
    """

    def __init__(self):
        self.bridge = AnkiBridge()

    def run_import(self, file_path: Path) -> Dict[str, Any]:
        """
        Detect file type and import using Anki's built-in importers.
        Returns a structured dictionary with status and summary info.
        """
        file_ext = file_path.suffix.lower()
        col = self.bridge.col

        try:
            if file_ext in (".apkg", ".colpkg"):
                importer = AnkiPackageImporter(col, str(file_path))
                imported_count = importer.run()
                return self._build_response(True, "apkg", imported_count)

            elif file_ext in (".txt", ".tsv", ".csv"):
                importer = TextImporter(col, str(file_path))
                imported_count = importer.run()
                return self._build_response(True, "text", imported_count)

            # elif file_ext == ".csv":
            #     importer = CsvFileImporter(col, str(file_path))
            #     imported_count = importer.run()
            #     return self._build_response(True, "csv", imported_count)

            else:
                return self._build_response(False, "unsupported", 0, f"Unsupported file type: {file_ext}")

        except Exception as e:
            return self._build_response(False, "error", 0, str(e))

    def _build_response(self, success: bool, import_type: str, count: int, error: str = None) -> Dict[str, Any]:
        return {
            "success": success,
            "type": import_type,
            "imported_notes": count,
            "error": error,
        }

import pathlib

ISA_API_RAW_DOWNLOAD_URL = "https://raw.githubusercontent.com/ISA-tools/isa-api"

JSONLD_RAW_DOWNLOAD_URL = f"{ISA_API_RAW_DOWNLOAD_URL}/refs/heads/master/isatools/resources/json-context"
JSON_CONTEXT_ROOT_DIR = pathlib.Path(__file__).resolve().parents[1] / "resources" / "json-context"

JSONLD_CONTEXT_FOLDER_MAPPING: dict[str, str] = {
    "obo": "obo",
    "wdt": "wd",
    "sdo": "sdo",
    "w3c": "w3c",
    "isaterms": "isaterms",
}

from extractor.extractor_types import extract_types
from config.paths import PATH_FILE


def run_pipeline() -> None:
    named_types_list = extract_types(PATH_FILE)

    for name, typ in named_types_list:
        print(f"Name: {name}, Type: {typ}")


if __name__ == "__main__":
    run_pipeline()

from create_db.connection import connect
from config.paths import FILE_PATH


def run_pipeline() -> None:
    connect(FILE_PATH)


if __name__ == "__main__":
    run_pipeline()

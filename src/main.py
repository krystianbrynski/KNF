from create_json_structure.json_structure import create_structure
from src.config.constants import ACTION, get_action, set_action


def run_pipeline() -> None:
    action = get_action()
    while (action != 0):
        set_action(int(input("xdd")))


    create_structure()


if __name__ == "__main__":
    run_pipeline()

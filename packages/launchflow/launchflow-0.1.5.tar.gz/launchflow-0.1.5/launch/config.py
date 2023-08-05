import dataclasses
import json
import os


_CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.config', 'launchflow')
_CONFIG_FILE = 'config.json'
_CONFIG_PATH = os.path.join(_CONFIG_DIR, _CONFIG_FILE)


@dataclasses.dataclass
class LaunchFlowConfig:
    default_organization: str = ''

    def write(self):
        os.makedirs(_CONFIG_DIR, exist_ok=True)
        with open(_CONFIG_PATH, 'w') as f:
            json.dump(dataclasses.asdict(self), f)

    @classmethod
    def load(cls):
        if os.path.exists(_CONFIG_PATH):
            with open(_CONFIG_PATH, 'r') as f:
                try:
                    json_config = json.load(f)
                except Exception:
                    # If we fail to load it for whatever reason treat it as an
                    # unset config.
                    return cls()
            return cls(**json_config)
        return cls()

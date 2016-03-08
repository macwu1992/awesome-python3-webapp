#config
import config_default
import logging

configs = config_default.configs

try:
    import config_override
    configs = dict(configs, **config_override.configs)
except ImportError:
    logging.info("ImportError raised")
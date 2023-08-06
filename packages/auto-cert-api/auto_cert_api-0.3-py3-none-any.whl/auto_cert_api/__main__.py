#!/usr/bin/env python3
# Import and initialize logging stuff before anything else:
import logging
logging.basicConfig()  # Do that before anything can initiate Python's logging interface.

import sys
import getopt

import uvicorn

from auto_cert_api import router
from auto_cert_api import title, version, release

_logger = logging.getLogger("main")
_uvicorn_log_format_str = "%(asctime)s | %(levelname)s | idsb_bot:uvicorn | %(message)s"

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:r:v:", ["port=", "root-path=", "verbose=", "proxy"])
    except getopt.GetoptError as err:
        logging.exception(str(err))
        sys.exit(2)

    logging.getLogger("uvicorn").propagate = False
    uvi_log_config = uvicorn.config.LOGGING_CONFIG
    uvi_log_config["formatters"]["access"]["fmt"] = _uvicorn_log_format_str
    uvi_log_config["formatters"]["default"]["fmt"] = _uvicorn_log_format_str

    uvicorn_params = {
        "host": "0.0.0.0",
        "port": 8080,
        "log_level": logging.WARNING,
        "log_config": uvi_log_config
    }

    for o, a in opts:
        if o in ("-p", "--port"):
            uvicorn_params["port"] = int(a)
        elif o in ("-r", "--root-path"):
            uvicorn_params["root-path"] = a
        elif o in ("-v", "--verbose"):
            level = logging.getLevelName(a.upper())
            logging.getLogger().setLevel(level)
            uvicorn_params["log_level"] = level
        elif o == "--proxy":
            uvicorn_params["proxy_headers"] = True
            uvicorn_params["forwarded_allow_ips"] = "*"
        else:
            logging.exception(f"unhandled option {o} : {a}")
            sys.exit(2)

    _logger.info(f"Starting {title} (v{version}) {release}")
    if "root_path" in uvicorn_params:
        _logger.info(f"root path = {uvicorn_params['root_path']}")
    uvicorn.run(router, **uvicorn_params)


# Only execute if run as a script.
if __name__ == "__main__":
    main()

import logging

from app.WebApp import WebApp
from app.helpers.config_builder import init_app


is_debug = __name__ == "__main__"

init_app()
log = logging.getLogger(__name__)
log.info("Starting App")

_web_app = WebApp(is_debug)
app = _web_app.app


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

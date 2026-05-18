import logging
import os
from datetime import datetime

from flask import Flask, render_template, request, jsonify

from app.PhilipsGenerator import PhilipsGenerator


log = logging.getLogger(__name__)
code_logger = logging.getLogger("code_generator")


class WebApp:
    def __init__(self, debug: bool):
        self.app = Flask(
            __name__,
            template_folder="app/templates",
            static_folder="static",
            static_url_path="/static",
            root_path=os.getcwd(),
        )
        self.app.config["DEBUG"] = debug

        self._generator = PhilipsGenerator()
        self._register_routes()
        self._register_context()

    def _register_routes(self):
        self.app.add_url_rule("/", endpoint="index", view_func=self._index)
        self.app.add_url_rule("/generate", endpoint="generate", view_func=self._generate, methods=["POST"])

    def _register_context(self):
        self.app.context_processor(self._inject_globals)

    def _inject_globals(self):
        return dict(
            app_version=os.getenv("RR_BUILD_VERSION", "DEBUG"),
            is_debug=self.app.debug,
            year=datetime.now().year,
        )

    def _index(self):
        return render_template("index.html")

    def _generate(self):
        dev_id = ""
        try:
            data = request.get_json(silent=True) or {}
            dev_id = (data.get("device_id") or "").strip()

            if not dev_id:
                log.warning(f"Code generation attempt without Device ID. IP: {request.remote_addr}")
                return jsonify({"error": "Device ID is required"}), 400

            days = 5
            current_time = datetime.now()
            result = self._generator.generate(dev_id=dev_id, days=days, current_time=current_time)

            code_logger.info(
                f"DeviceID: {dev_id} | "
                f"Code: {result['code']} | "
                f"ValidDays: {days} | "
                f"ValidUntil: {result['valid_until'].strftime('%Y-%m-%d %H:%M:%S')} | "
                f"IP: {request.remote_addr}"
            )
            log.info(f"Code generated for Device ID: {dev_id}")

            return jsonify({
                "success": True,
                "device_id": dev_id,
                "code": result["code"],
                "valid_days": days,
                "current_date": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "valid_until": result["valid_until"].strftime("%Y-%m-%d %H:%M:%S"),
            })
        except Exception as e:
            log.error(f"Error generating code for Device ID: {dev_id or 'unknown'}. Error: {e}")
            return jsonify({"error": str(e)}), 500

from flask import Flask, render_template, request, jsonify
from datetime import datetime
from lib_code.PhilipsGenerator import PhilipsGenerator
import logging.config
import yaml
import os

if not os.path.exists('logs'):
    os.makedirs('logs')

with open('config/logging.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)
code_logger = logging.getLogger('code_generator')

app = Flask(__name__)
generator = PhilipsGenerator()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        dev_id = data.get('device_id', '').strip()

        if not dev_id:
            logger.warning(f"Code generation attempt without Device ID. IP: {request.remote_addr}")
            return jsonify({'error': 'Device ID is required'}), 400

        days = 5
        current_time = datetime.now()

        result = generator.generate(dev_id=dev_id, days=days, current_time=current_time)

        # Log generated code
        code_logger.info(
            f"DeviceID: {dev_id} | "
            f"Code: {result['code']} | "
            f"ValidDays: {days} | "
            f"ValidUntil: {result['valid_until'].strftime('%Y-%m-%d %H:%M:%S')} | "
            f"IP: {request.remote_addr}"
        )

        logger.info(f"Code generated for Device ID: {dev_id}")

        return jsonify({
            'success': True,
            'device_id': dev_id,
            'code': result['code'],
            'valid_days': days,
            'current_date': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'valid_until': result['valid_until'].strftime('%Y-%m-%d %H:%M:%S')
        })

    except Exception as e:
        logger.error(f"Error generating code for Device ID: {dev_id if 'dev_id' in locals() else 'unknown'}. Error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

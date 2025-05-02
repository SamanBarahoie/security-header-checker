import logging
import requests
from flask import Flask, request, jsonify
from urllib.parse import urlparse
from requests.exceptions import RequestException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# List of security headers to check
SECURITY_HEADERS = {
    'Content-Security-Policy': 'Controls resources the user agent is allowed to load.',
    'X-Frame-Options': 'Prevents clickjacking by controlling framing.',
    'X-Content-Type-Options': 'Prevents MIME type sniffing.',
    'Strict-Transport-Security': 'Enforces HTTPS connections.',
    'Referrer-Policy': 'Controls information sent in Referer header.',
    'Permissions-Policy': 'Controls browser features and APIs.'
}

def validate_url(url):
    """Validate the URL format."""
    parsed = urlparse(url)
    return all([parsed.scheme in ['http', 'https'], parsed.netloc])

def check_security_headers(url):
    """Check security headers for the given URL."""
    try:
        logger.info(f"Checking headers for URL: {url}")
        response = requests.head(url, timeout=5, allow_redirects=True)
        headers = response.headers
        result = {
            'url': url,
            'status': 'success',
            'headers': {},
            'missing_headers': [],
            'recommendations': []
        }

        # Check each security header
        for header, description in SECURITY_HEADERS.items():
            if header in headers:
                result['headers'][header] = headers[header]
            else:
                result['missing_headers'].append(header)
                result['recommendations'].append(f"Add {header}: {description}")

        # Additional checks for HSTS
        if 'Strict-Transport-Security' in headers:
            hsts = headers['Strict-Transport-Security']
            if 'max-age=0' in hsts:
                result['recommendations'].append(
                    "Increase max-age for Strict-Transport-Security (e.g., max-age=31536000)."
                )

        return result

    except RequestException as e:
        logger.error(f"Failed to fetch headers for {url}: {str(e)}")
        return {
            'url': url,
            'status': 'error',
            'error': f"Failed to fetch headers: {str(e)}"
        }

@app.route('/')
def home():
    """Return a welcome message."""
    return jsonify({
        'message': 'Welcome to Security Header Checker!',
        'version': '1.0.0',
        'endpoints': {
            '/check': 'POST - Check security headers for a given URL'
        }
    })

@app.route('/check', methods=['POST'])
def check_headers():
    """Check security headers for a provided URL."""
    try:
        data = request.get_json()
        logger.info(f"Received JSON: {data}")
    except Exception as e:
        logger.error(f"Failed to parse JSON: {str(e)}")
        return jsonify({'error': f"Invalid JSON: {str(e)}"}), 400

    url = data.get('url') if data else None

    if not url:
        logger.warning("Request received without URL")
        return jsonify({'error': 'URL is required'}), 400

    if not validate_url(url):
        logger.warning(f"Invalid URL provided: {url}")
        return jsonify({'error': 'Invalid URL format'}), 400

    result = check_security_headers(url)
    status_code = 200 if result['status'] == 'success' else 500
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
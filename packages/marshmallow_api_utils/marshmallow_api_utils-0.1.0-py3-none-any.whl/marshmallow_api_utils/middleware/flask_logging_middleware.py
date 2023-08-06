import logging
import time

try:
    from flask import Flask, current_app, request
except ImportError:
    raise Exception("flask must be installed to use FlaskBlueprint") from None

try:
    from flask_log_request_id import RequestID, current_request_id
except ImportError:
    flask_log_request_id = None

x_headers = [
    'X-Real-Ip',
    'X-Forwarded-For',
    'X-Forwarded-Host',
    'X-Forwarded-Uri',
]


class Log:

    def __init__(self, app: Flask = None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):

        if flask_log_request_id:
            RequestID(app)

        with app.app_context():

            @app.before_request
            def start_timer():
                request.start_time = time.time()

            @app.after_request
            def log_request(response):

                log_fields = {}
                log_fields['authorisation'] = request.authorization
                log_fields['connection'] = request.headers.get('Connection')
                log_fields['content_length'] = response.headers.get('Content-Length')
                log_fields['content_md5'] = request.content_md5
                log_fields['content_type'] = request.content_type
                log_fields['cookies'] = request.cookies
                log_fields['dest_host'] = request.host.split(':', 1)[0]
                log_fields['dest_port'] = int(request.host.split(':', 1)[1]) if len(
                    request.host.split(':', 1),
                ) == 2 else 80
                log_fields['duration'] = time.time() - request.start_time.start
                log_fields['http_method'] = request.method
                log_fields['http_status'] = response.status_code
                log_fields['mimetype'] = request.mimetype
                log_fields['referrer'] = request.referrer

                if flask_log_request_id:
                    log_fields['request_id'] = current_request_id()
                else:
                    log_fields['request_id'] = request.headers.get(
                        'X-Request-ID',
                    ) if request.headers.get('X-Request-ID') else ""

                log_fields['request_scheme'] = request.scheme
                log_fields['src_ip'] = request.headers.get(
                    'X-Forwarded-For', request.remote_addr,
                )
                log_fields['user'] = request.remote_user if request.remote_user else ""
                log_fields['url'] = request.url
                log_fields['url_path'] = request.path
                log_fields['url_query'] = request.query_string
                log_fields['useragent'] = request.user_agent

                for header in x_headers:
                    if request.headers.get(header):
                        log_fields[header.lower().replace('-', '_')] = request.headers.get(header)

                logging.getLogger(current_app.name).info("Request complete.", extra=log_fields)

from flask import Flask, request

app = Flask(__name__)
app.config.from_object('settings')
app.config.from_envvar('GOONHILLY_SETTINGS')

import logging
import logging.handlers


logger = logging.getLogger('Goonhilly')
logger.setLevel(logging.INFO)
log_handler = logging.FileHandler(app.config['GOONHILLY_LOG'])
log_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s [%(levelname)s] %(message)s"))
logger.addHandler(log_handler)


def clean(s):
    if ' ' in s:
        s = '"%s"' % s.replace('"', '\'')
    return s


@app.route('/log/<sourceapp>/', methods=['POST', 'GET',])
def log():
    l = ['%s=%s' % (clean(k), clean(v)) for k, v in request.values.iteritems()]
    l.append('%s=%s' % (clean('client_id'), clean(request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR') or '-')))
    l.append('%s=%s' % (clean('sourceapp'), clean(sourceapp)))
    out = ' '.join(l)
    logger.info(out)
    return 'CREATED', 201


if __name__ == '__main__':
    app.run()


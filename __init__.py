import os
import logging
import logging.handlers

log = logging.getLogger()
log.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)-15s %(levelname)s %(name)s %(message)s")

handler = logging.handlers.RotatingFileHandler("%s.log" % __name__)
handler.setFormatter(formatter)
handler.setLevel(logging.WARNING)
log.addHandler(handler)

handler = logging.handlers.RotatingFileHandler(os.path.expanduser("~/%s.log" % __name__))
handler.setFormatter(formatter)
handler.setLevel(logging.WARNING)
log.addHandler(handler)

import sys
stdout_handler = logging.StreamHandler(sys.stderr)
stdout_handler.setLevel(logging.WARNING)
stdout_handler.setFormatter(formatter)
log.addHandler(stdout_handler)

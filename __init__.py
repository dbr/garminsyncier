import os
import logging
import logging.handlers
from . import config

logging.getLogger("garminsyncier.requests").setLevel(logging.WARNING)

log = logging.getLogger("garminsyncier")
log.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)-15s %(levelname)s %(name)s %(message)s")

handler = logging.handlers.RotatingFileHandler(os.path.join(config.log_dir, "%s.log" % __name__))
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)
log.addHandler(handler)

import sys
stdout_handler = logging.StreamHandler(sys.stderr)
stdout_handler.setLevel(logging.WARNING)
stdout_handler.setFormatter(formatter)
log.addHandler(stdout_handler)

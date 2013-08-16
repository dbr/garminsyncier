import sys
import logging
import optparse


log = logging.getLogger(__name__)


def mail(opts):
    # Handle verbosity
    if opts.verbosity is not None:
        from . import stdout_handler
        stdout_handler.setLevel(logging.DEBUG)

    from . import mailer
    mailer.process_files()


def _main():
    opter = optparse.OptionParser()
    opter.add_option("-v", "--verbose", dest="verbosity", action="count")

    opts, args = opter.parse_args()

    if len(args) > 0 and args[0] == 'grab':
        from .poller import grab
        grab(opts=opts)
    elif len(args) > 0 and args[0] == 'mail':
        from .mailer import process_files
        process_files(opts=opts)
    else:
        opter.error("first arg must be [grab/mail]")


def main():
    try:
        return _main()
    except Exception:
        log.critical("Error with %s", __name__, exc_info=True)
        sys.exit(111)
    

if __name__ == '__main__':
    main()

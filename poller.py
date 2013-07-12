import logging

from . import garminconnect


log = logging.getLogger(__name__)


def grab(opts):
    # Handle verbosity
    if opts.verbosity is not None:
        from . import stdout_handler
        stdout_handler.setLevel(logging.DEBUG)


    if True:
        # TODO: Garmin's API doesn't seem to have any way to filter based on ID..
        highest_id = None
    else:
        """
    import os
    ids = [x for x in os.listdir(download_dir) if x.endswith(".tcx")]
    ids = [int(x.rpartition(".")[0]) for x in ids]
    if len(ids) > 0:
        print ids
        highest_id = max(ids, key = lambda k: int(k))
        log.info("Starting at id {highest}".format(highest=highest_id))
    else:
        highest_id = None
        log.info("Starting fresh")
    """

    from . import config

    gc = garminconnect.GarminConnect(config.username, config.password)
    gc.login()
    for act in gc.list_activities(start_id = highest_id):
        try:
            path = act.download(config.download_dir)
            log.info("Downloaded {0}".format(path))
        except garminconnect.ActivityExists, e:
            log.info(e)

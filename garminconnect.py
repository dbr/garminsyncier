import os
import logging
from . import requests

from . import config


log = logging.getLogger(__name__)


class GarminConnectError(Exception):
    pass

class ActivityExists(Exception):
    pass


class ActivityFile(object):
    def __init__(self, id, start=None):
        self.id = id
        self.start = start

    def __repr__(self):
        return "<{cls} id={id} start={start!r}>".format(
            cls = self.__class__.__name__, id = self.id, start=self.start)

    def filename(self, filetype):
        return "{id}.{filetype}".format(
            id = self.id,
            filetype = filetype)

    def download(self, directory, filetype='tcx'):
        # Check file type
        available_formats = ['json', 'gpx', 'kml', 'tcx']
        if filetype not in available_formats:
            raise ValueError("{specified} must be {available}".format(
                specified=filetype,
                available = ", ".join(available_formats)))

        # Calculate path
        fpath = os.path.abspath(os.path.join(directory, self.filename(filetype=filetype)))

        if os.path.exists(fpath):
            raise ActivityExists("File {file} already exists".format(file=fpath))

        # Download activity
        url = "http://connect.garmin.com/proxy/activity-service-1.1/{format}/activity/{id}?full=true".format(
            format=filetype,
            id=self.id)

        r = requests.get(url)
        if not r.ok:
            raise GarminConnectError("Status code {0.status_code} getting {0.url}: {0.reason}".format(r))

        # Write file
        log.debug("Downloaded file to {0}".format(fpath))
        try:
            with open(fpath, "w+") as f:
                f.write(r.text)
        except Exception:
            log.warning("Problem while writing file", exc_info=True)
            try:
                os.unlink(fpath)
            except Exception:
                pass
        return fpath


class GarminConnect(object):
    default_user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17'

    def __init__(self, username, password = None):
        self.username = username
        self.password = password

        self.session = requests.Session()

    def login(self):
        r = self.session.get('https://connect.garmin.com/signin')
                               
        params = {'login': 'login',
                  'login:loginUsernameField': self.username,
                  'login:password': self.password,
                  'login:signInButton': 'Sign In',
                  'javax.faces.ViewState': 'j_id1'}
        
        r = self.session.post('https://connect.garmin.com/signin',
                              data=params)



        if not r.ok and r.status_code > 400:
            log.debug(r.headers)
            raise GarminConnectError("Status code {0.status_code} getting {0.url}".format(r))


    def list_activities(self, start_id = None):
        if start_id is None:
            start_id = 0

        for page in range(1000):
            page = page + 1

            url="https://connect.garmin.com/proxy/activity-search-service-1.2/json/activities?userId={userid}&sortField=id&sortOrder=ASC&currentPage={page}".format(
                userid=config.userid,
                begin = start_id,
                page = page,
                )

            log.debug("Getting {0}".format(url))
            r = self.session.get(url)

            if not r.ok:
                raise GarminConnectError("Status code {0.status_code} getting {0.url}: {0.reason}".format(r))


            data = r.json()
            for activity in data['results']['activities']:
                id = activity['activity']['activityId']
                yield ActivityFile(id)

            # Check if we are on the last page
            if 'search' not in data['results']:
                # No search on first page?
                log.debug("First and only page")
                break
            else:
                currentPage = data['results']['search']['currentPage']
                totalPages = data['results']['search']['totalPages']
                log.debug("Page {cur} of {total}".format(cur=currentPage, total=totalPages))
                if currentPage == totalPages:
                    # done
                    break


    def activity(self, actid):
        return ActivityFile(actid)

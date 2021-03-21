# Garmin Connect to Strava auto-uploader

You probably want to use [CopyMySports.com](http://www.CopyMySports.com/)
instead.

This Python-based tool uploads all rides from a Garmin Sync account to
Strava, preserving all data except temperature (including speed,
elevation, heartrate, cadence, power)

## Setup

First copy `config.py.sample` to `config.py` and fill out the values.

Then run the following commands routinely:

    python -m garminsyncier grab
    python -m garminsyncier mail

The first `grab` command should be run maybe every 10 minutes or so,
to avoid annoying the Garmin Connect API.

The second `mail` command can be run more often, maybe every 1
minute. It checks a directory for no files, and exits if none are
found.

## How it works

The `grab` command downloads any new rides from Garmin Connect as a
`.tcx` file. These are placed in `config.download_dir`.

A ride is considered "new" if there is no file named `${ride_id}.gpx`
or `${ride_id}.tcx` in either the `download_dir` or `sent_dir`

The `mail` command takes any `.tcx` or `.gpx` file in `download_dir`,
and mails them to `upload@strava.com` (or any other address, really)

As long as `config.your_email` matches your Strava account address,
the ride will appear like any other.


I ran the grab command every 10 minutes (avoid annoying Garmin's API),
and the mail command every 1 minute (it's very quick


Note that Garmin Connect `tcx` export does not include the temperature
data (which Strava may support in a `<gpxtpx:atemp>` tag on each track
point). The GPX format does include this data, but excludes power. You
can change format trivially in `garminconnect.py` (should really be a
config option)


## Why?

I was attempting to cycle from Adelaide to Perth, and wanted to upload
the rides each day onto Strava...

Leaving things quite late, I tried the now-defunct GarminSync a few
days before I left, but didn't trust it (mostly I didn't know how long
it takes to spot new rides, and there was no logging when it last
tried and so on)

..so I wrote my own, simple and robust version if it in an evening.

I ran it on a Rackspace "cloud server" VM, with the code, the logs,
the `download_dir` and `sent_dir` all located in Dropbox.

The code worked perfectly - I could check if it had uploaded the ride
using the Dropbox iOS application, comment on the ride with the Strava
application, and share the ride with family and friends on
Facebook. All in the middle of rural Australia. Hurray for technology.

(Oh, I made it as far as Ceduna after 4-and-a-bit days, before
deciding to head back)

## Does it still work?

Probably.

It worked as of 2013-07-20, running on Python 2.6. It does **not**
require the now-dead Strava API v1 or v2 (nor the private v3)

The code itself is quite simple. The only parts likely to break are:

* Garmin Connect's API. They are barely documented, and many of the
  endpoints have multiple versions, all of which have varying levels
  of usefulness. The API's have been around for a while, and multiple
  old versions still active and working.
* The `upload@strava.com` functionality might get removed, while this
  is unlikely, I would have said the same thing about removing any
  public-access to their proper API,
  [but oh](http://www.dcrainmaker.com/2013/07/cutting-removing-functionality.html)


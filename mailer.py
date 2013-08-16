import os
import shutil
import logging
import smtplib
#import mimetypes
import email
import email.mime.application

from . import config

log = logging.getLogger(__name__)


def _create_email(filepath):
    msg = email.mime.Multipart.MIMEMultipart()
    msg['Subject'] = 'Ride upload'
    msg['From'] = config.your_email
    msg['To'] = config.strava_upload_email

    import datetime

    body = email.mime.Text.MIMEText(
        ("Attached ride file!\n"
         "Sent at %s\n") % datetime.datetime.now())
    msg.attach(body)

    filename = os.path.basename(filepath)
    with open(filepath,'rb') as fp:
        att = email.mime.application.MIMEApplication(fp.read())

    att.add_header('Content-Disposition','attachment', filename=filename)
    msg.attach(att)

    return msg


def _mail_file(filepath):
    log.info("Emailing %s" % filepath)
    session = smtplib.SMTP(config.your_email_server, config.your_email_port)
    log.debug(session.ehlo())
    session.starttls()
    login_result = session.login(config.your_email_login, config.your_email_password)
    log.debug(login_result)

    msg = _create_email(filepath)
    session.sendmail(config.your_email, [config.strava_upload_email], msg.as_string())
    session.quit()


def ls(path):
    return [os.path.join(path, x) for x in os.listdir(path) if not x.startswith(".")]


def process_files(opts):
    for f in ls(config.download_dir):
        log.info("Processing %s" % f)

        try:
            _mail_file(f)
        except Exception:
            log.critical("Error emailing %s" % f, exc_info=True)
            continue # Try next file
        else:
            log.debug("Moving %s to %s" % (f, config.sent_dir))
            shutil.move(f, config.sent_dir)

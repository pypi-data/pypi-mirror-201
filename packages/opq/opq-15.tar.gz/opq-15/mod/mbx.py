# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,E0402,R0903


"mailbox"


import mailbox
import os


from ..handler import Event
from ..objects import Object, update
from ..persist import path, write


bdmonths = ['Bo', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
            'Sep', 'Oct', 'Nov', 'Dec']


monthint = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}


class Email(Event):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ""


def to_date(date):
    date = date.replace("_", ":")
    res = date.split()
    ddd = ""
    try:
        if "+" in res[3]:
            raise ValueError
        if "-" in res[3]:
            raise ValueError
        int(res[3])
        ddd = "{:4}-{:#02}-{:#02} {:6}".format(res[3], monthint[res[2]], int(res[1]), res[4])
    except (IndexError, KeyError, ValueError) as ex:
        try:
            if "+" in res[4]:
                raise ValueError from ex
            if "-" in res[4]:
                raise ValueError from ex
            int(res[4])
            ddd = "{:4}-{:#02}-{:02} {:6}".format(res[4], monthint[res[1]], int(res[2]), res[3])
        except (IndexError, KeyError, ValueError):
            try:
                ddd = "{:4}-{:#02}-{:02} {:6}".format(res[2], monthint[res[1]], int(res[0]), res[3])
            except (IndexError, KeyError):
                try:
                    ddd = "{:4}-{:#02}-{:02}".format(res[2], monthint[res[1]], int(res[0]))
                except (IndexError, KeyError):
                    try:
                        ddd = "{:4}-{:#02}".format(res[2], monthint[res[1]])
                    except (IndexError, KeyError):
                        try:
                            ddd = "{:4}".format(res[2])
                        except (IndexError, KeyError):
                            ddd = ""
    return ddd


def mbx(event):
    if not event.args:
        return
    if os.path.exists(path("mod.mbx.Email")):
        event.reply("email is already scanned")
        return
    fnm = os.path.expanduser(event.args[0])
    event.reply("reading from %s" % fnm)
    nmr = 0
    if os.path.isdir(fnm):
        thing = mailbox.Maildir(fnm, create=False)
    elif os.path.isfile(fnm):
        thing = mailbox.mbox(fnm, create=False)
    else:
        return
    try:
        thing.lock()
    except FileNotFoundError:
        pass
    for email in thing:
        obj = Email()
        update(obj, Object(email))
        obj.text = ""
        for payload in email.walk():
            if payload.get_content_type() == 'text/plain':
                obj.text += payload.get_payload()
        obj.text = obj.text.replace("\\n", "\n")
        write(obj)
        nmr += 1
    if nmr:
        event.reply("ok %s" % nmr)

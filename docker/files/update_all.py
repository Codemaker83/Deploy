#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from subprocess import call, Popen, PIPE

fnames= ["/tmp/post-test.log", "/tmp/uall.log"]

call(["chown", "-R", "odoo:odoo", "/home/odoo"])
call(["chmod", "-R", "ugo+rwx", "/tmp"])
for fname in fnames:
    if os.path.isfile(fname):
        os.remove(fname)

post_test = Popen(["python", "/home/odoo/post-migrate-script/post-test.py",
    "'user=odoo80 dbname=vauxoo80 port=5432 password=mU9kvz9crdH9CaFPWB host=172.17.42.1'",
    " -v > /tmp/post-test.log"])

pt_stdout, pt_stderr = post_test.communicate()

deactivate = Popen(["python",
    "/home/odoo/post-migrate-script/deactivate.py",
    "--username=odoo80",
    "--password=mU9kvz9crdH9CaFPWB"
    "-H 172.17.42.1",
    "-p 5432",
    "-a mail,pac,cron",
    "vauxoo80"])

d_stdout, d_stderr = deactivate.communicate()


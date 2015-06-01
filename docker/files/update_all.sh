#!/bin/bash
echo "Changing folders permissions"
chown -R odoo:odoo /home/odoo
chmod ugo+rwx /tmp
echo "Cleaning log files"
rm /tmp/post-test.log
rm /tmp/uall.log
echo "Running post-test.py script"
python /home/odoo/post-migrate-script/post-test.py 'user=odoo80 dbname=vauxoo80 port=5432 password=mU9kvz9crdH9CaFPWB host=172.17.42.1' -v > /tmp/post-test.log
echo "Deactivating parameters"
python /home/odoo/post-migrate-script/deactivate.py --username=odoo80 --password=mU9kvz9crdH9CaFPWB -H 172.17.42.1 -p 5432 -a mail,pac,cron vauxoo80
echo "Running -u all"
for i in `seq 1 2`;
do
    su odoo -c "/home/odoo/instance/odoo/odoo.py -c /home/odoo/.openerp_serverrc -d vauxoo80 -u all --stop-after-init --logfile=/tmp/uall.log --db_host=172.17.42.1 -r odoo80 -w mU9kvz9crdH9CaFPWB --without-demo=True"
done
cd /tmp && tar -cjf build_logs.tar.bz2 uall.log post-test.log
echo "Generating file with branch info"
python /home/odoo/backupws/branches.py -f /tmp/branches-info.json -p /home/odoo/instance -s 
echo "Sending mail with results"
python /send_mail.py
echo "Running entry_point"
/entry_point.py

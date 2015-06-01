FROM vauxoo/odoo-80-image
MAINTAINER Tulio Ruiz <tulio@vauxoo.com>
RUN adduser --home=/home/odoo --disabled-password --gecos "" --shell=/bin/bash odoo
RUN echo 'root:odoo' |chpasswd
RUN mkdir /home/odoo/.ssh
ADD files/id_rsa /home/odoo/.ssh/id_rsa
RUN chown odoo:odoo -R /home/odoo \
    && chmod 600 /home/odoo/.ssh/id_rsa
ADD files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN pip install gitpython
USER odoo
ENV HOME /home/odoo
ADD files/instance-config.json /tmp/instance-config.json
RUN ssh-keyscan github.com > /home/odoo/.ssh/known_hosts \
    && ssh-keyscan bazaar.launchpad.net >> /home/odoo/.ssh/known_hosts \
    && ssh-keyscan launchpad.net >> /home/odoo/.ssh/known_hosts \
    && ssh-keyscan bitbucket.org >> /home/odoo/.ssh/known_hosts
RUN /bin/bash -c "mkdir -p /home/odoo/instance/{config,extra_addons}"
RUN bzr lp-login coward
RUN cd /home/odoo/ \
    && git clone -b git-improve --single-branch --depth=1 git@github.com:Codemaker83/backupws.git
RUN cd /home/odoo/backupws \
    && python branches.py -p /home/odoo/instance -f /tmp/instance-config.json -l \
    && bzr checkout lp:vauxoo-private/docs --lightweight docs
ADD files/post-migrate-script /home/odoo/post-migrate-script
#ADD files/themes /home/odoo/instance/extra_addons/themes
ADD files/openerp_serverrc /home/odoo/.openerp_serverrc
RUN rm /home/odoo/.ssh/id_rsa
RUN mkdir -p /home/odoo/datadir
ENV XDG_DATA_HOME /home/odoo/datadir/share
USER root
RUN mkdir /external_files
ADD files/supervisord.conf /external_files/supervisord.conf
ADD files/openerp_serverrc /external_files/.openerp_serverrc
ADD files/update_all.sh /update_all.sh
ADD files/send_mail.py /send_mail.py
RUN chmod +x /update_all.sh
RUN mkdir -p /var/log/supervisor
RUN wget -q -O /entry_point.py https://raw.githubusercontent.com/Vauxoo/docker_entrypoint/master/entry_point.py \
    && chmod +x /entry_point.py
VOLUME ["/var/log/supervisor", "/home/odoo/datadir", "/home/odoo/.ssh", "/tmp"]
EXPOSE 8069
EXPOSE 8072
CMD /entry_point.py

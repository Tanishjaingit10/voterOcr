 # **For AWS deployment**
 

postgres setup
>_https://dailyscrawl.com/how-to-install-postgresql-on-amazon-linux-2/_

```
amazon-linux-extras install postgresql10 vim epel
yum install -y postgresql-server postgresql-devel
/usr/bin/postgresql-setup –-initdb
systemctl status postgresql
service postgresql initdb
systemctl enable postgresql
systemctl start postgresql
```
```
local---
sudo -u postgres psql
postgres=# create user shiv with password 1qazxsw2;
postgres=# create user shiv with password '1qazxsw2';
```

_https://stackabuse.com/how-to-fix-warning-unprotected-private-key-file-on-mac-and-linux/_
```
$ sudo chmod 600 /path/to/my/key.pem
$ sudo chmod 755 ~/.ssh
```

_https://stackoverflow.com/questions/64095094/command-python-setup-py-egg-info-failed-with-error-code-1-in-tmp-pip-build-rn_

```
[ec2-user@ip-172-31-23-24 voters]$ sudo yum install libgl1-mesa-glx

yum install mesa-libGL.x86_64

sudo nano /var/lib/pgsql/data/pg_hba.conf

postgres=# \password

postgres=# SELECT pg_reload_conf();

[ec2-user@ip-172-31-23-24 voters]$ psql -U postgres -d voters_db

voters_db=# \dt
```
_https://medium.com/quantrium-tech/installing-tesseract-4-on-ubuntu-18-04-b6fcd0cbd78f_

_https://github.com/EisenVault/install-tesseract-redhat-centos/blob/master/install-tesseract.sh_

_https://groups.google.com/g/tesseract-ocr/c/8gk462NW8TA_

_https://linuxhint.com/install-tesseract-ocr-linux/_



```
sudo systemctl restart gunicorn

service gunicorn stop
```
------------------------
```
pip install gunicorn
gunicorn voter_ocr_backend.wsgi:application --bind 0.0.0.0:80
```

```
sudo ngnix
gunicorn --bind 0.0.0.0:80 voter_ocr_backend.wsgi:application
```
```
sudo apt-get install -y supervisor
cd /etc/supervisor/conf.d/
touch gunicorn.conf
```
```
[program:gunicorn]
directory=/home/ubuntu/voter_ocr_backend
command=/home/ubuntu/env/bin/gunicorn --worker 3 --bind unix:/home/ubuntu/voter_ocr_backend/app.sock voter_ocr_backend.wsgi:application
autostart=true
autorestart=true
stderr_logfile=/var/log/voters_gunicorn.err.log
stdout_logfile=/var/log/voters_gunicorn.out.log

[group:guni]
programs:gunicorn
```
```
sudo supervisorctl reread
sudo mkdir /var/log/voters_gunicorn
```
```
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status
```
```
cd 
cd /etc/nginx/sites-available/
ls
cat default
```
```
sudo touch django_voters_gunicorn.conf
```
```
server {
    listen 80;
    server_name """""";
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/voter_ocr_backend/app.sock;
    }
}
```
```
nginx -t
sudo nginx -t
ln django_voters_gunicorn.conf /etc/nginx/sites_enabled/
sudo nginx -t
sudo service nginx restart
```

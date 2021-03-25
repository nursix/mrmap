# Nginx

## Install

For hosting our web application we will use [the most
popular web server on the internet](https://news.netcraft.com/archives/category/web-server-survey/)
: the [Nginx](https://nginx.org) webserver.

### Debian

```no-highlight
sudo apt install -y nginx fcgiwrap
```

## Configure

We confiure our webserver to serve SSL traffic, if you dont want to encrypt your data there
is another configuration file for plain HTTP in the conf folder.

1. Create a certificate:

```no-highlight
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
```

1. Copy Nginx config file to its place, delete the default conf and enable it by creating a symlink.
If youre not installing to /opt/ you have to change the folder of the /static route in the [nginx conf](https://github.com/mrmap-community/mrmap/blob/master/install/confs/mrmap_nginx_ssl).

```no-highlight
sudo cp -a /opt/mrmap/mrmap/install/confs/mrmap_nginx_ssl /etc/nginx/sites-available/mrmap
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/mrmap /etc/nginx/sites-enabled/mrmap
```

1. Change HTTP_OR_SSL setting in dev_settings.py
```no-highlight
change HTTP_OR_SSL to "https://" in /opt/mrmap/mrmap/MrMap/sub_settings/dev_settings.py
```

## Verify Service Status

1. Restart webserver and test

```no-highlight
sudo systemctl restart nginx
```

1. You should see the login page after opening http://YOUR-IP-ADDRESS:

    ![login page](../installation/mrmap_loginpage.png)
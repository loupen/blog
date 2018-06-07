# blog
This blog is created by django with nginx and wsgi.
Nginx configuration is in etc/nginx folder.
Please refer to the following websites for nginx environment setting.
	http://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html#configure-nginx-for-your-site
	https://docs.djangoproject.com/en/2.0/howto/static-files/

Use following cmd to restart nginx service
	sudo service nginx restart

And use following cmd to execute uwsgi, thus the django server will be started automatically.
	sudo uwsgi --ini uwsgi.ini

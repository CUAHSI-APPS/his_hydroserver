# HIS HydroServer

This application provides data services for hydrologic time series data using a REST API based on CUAHSI's WaterOneFlow web services (http://his.cuahsi.org/wofws.html). It has been designed to extend HydroShare data service capabilities by reading data from HydroShare IRODS vaults. A prebuilt docker image is available on Docker Hub at https://cloud.docker.com/u/kjlippold/repository/docker/kjlippold/his_hydroserver.

## Getting Started

These instructions will help you install and run this HydroServer instance in a production environment.

### Prerequisites

##### Docker:
* [Install Docker Engine](https://docs.docker.com/install/)

### Installing
Run HydroServer Docker instance:
```
$ sudo docker run -d -p 8090:8090 -v {host_data_vault}:/irods_vault:ro -v /static/wds/:/static/wds/ --name his_hydroserver kjlippold/his_hydroserver:latest
```

Enter the HydroServer container:
```
$ sudo docker exec -it his_hydroserver /bin/bash
```

Give HydroServer IRODS Vault access:
```
$ usermod -u {host_privileged_user_id} hsapp
```

Change ownership of main repository to hsapp user:
```
$ sudo chown -R hsapp /home/hsapp/hydroserver
```

Make startup file executable:
```
sudo chmod +x /home/hsapp/hydroserver/hydroserver.sh
```

Open application settings file:
```
sudo vi /home/hsapp/hydroserver/hydroserver/settings.py
```

Add your host URL to CSRF_TRUSTED_ORIGINS, CSRF_COOKIE_DOMAIN, and ALLOWED_HOSTS. Set DEBUG to False for production environments. Edit the STATIC_URL and STATIC_ROOT to point to your static files on the container and on the host. Change the PROXY_BASE_URL to {host_url}/wds.

Save and finish editing:
```
:wq
```

Navigate to main app repository:
```
cd /home/hsapp/hydroserver/
```

Activate application Conda environment:
```
source activate hydroserver
```

Make application migrations:
```
python manage.py migrate
```

Exit application container:
```
exit
```

Restart HydroServer:
```
sudo docker restart his_hydroserver
```

The default username and password are admin, default. From the admin page of HydroServer ({hostname}/wds/admin/), change the admin password.

## Built With

* [Docker](https://docs.docker.com) - Docker Engine
* [Django](https://www.djangoproject.com) - Python Web Framework
* [Gunicorn](https://gunicorn.org) - WSGI HTTP Server

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
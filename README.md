# bitbots_drinks
> Keep track of how many drinks people have bought

## Deployment

This application can be deployed using two different methods which are described in the following sections.

In all cases, the application will not immediately start without errors because it needs to be configured first.
This is done via environment variables.
See [Configuration](#configuration) for the list of available options.

### On Docker

A docker image is built automatically that follows the master branch of the repository.
It is available as `ghcr.io/bit-bots/bitbots_drinks:dev-latest`.

Simply start it via
```shell
docker run --name bitbots_drinks ghcr.io/bit-bots/bitbots_drinks:latest
```

Configuration can be specified by supplying environment variables during `docker run` with the `-e` argument.
I.e. `docker run -e BBD_SECRET_KEY=foobar123 …`.

### On Baremetal from source

*Although this deployment works, it is not recommended. If you need to use a deployment without containers, you should serve this application via uwsgi, gunicorn or the like.*

To build the application from source, follow the following steps:
```shell
# get the code
git clone https://github.com/bit-bots/bitbots_drinks.git
cd bitbots_drinks

# install locked python dependencies
pipenv install --ignore-pipfile
```

To start it:
```shell
pipenv shell
./src/manage.py check --deploy
./src/manage.py migrate
./src/manage.py
```

## Configuration

The application is configured at runtime via the following environment variables:

| Name                     | Default                | Description                                                                                                                   | Notes                                                                               |
|--------------------------|------------------------|-------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| BBD_DB                   | *required*             | Url that specifies the complete database connection. [Documentation](https://pypi.org/project/dj-database-url/)               | In container based deployments this preconfigured to point to `/app/data/db.sqlite` |
| BBD_SECRET_KEY           | *required*             | Django secret key. **Keep this secret!**                                                                                      ||
| BBD_ALLOWED_HOSTS        | *required*             | List of hostnames which may be used when accessing the application.                                                           ||
| BBD_SERVED_OVER_HTTPS    | `false`                | Whether the application is served over HTTPS. If enabled, automatic redirects and additional security measures are activated. ||
| BBD_HSTS_SECONDS         | `63072000`             | If larger than 0 and `BL_SERVED_OVER_HTTPS` is true, HSTS is enabled with this configured value.                              ||
| BBD_TRUST_REVERSE_PROXY  | `false`                | If true, headers set by a reverse proxy (i.e. `X-Forwarded-Proto`) are trusted.                                               ||
||
| BBD_OPENID_CLIENT_ID     | *required*             | Mafiasi-Identity client ID. Used for authentication                                                                           ||
| BBD_OPENID_CLIENT_SECRET | *required*             | Mafiasi-Identity client secret. Used for authentication                                                                       ||

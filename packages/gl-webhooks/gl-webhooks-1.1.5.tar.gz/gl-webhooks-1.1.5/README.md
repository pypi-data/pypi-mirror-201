[![license](https://img.shields.io/badge/license-MIT-brightgreen)](https://spdx.org/licenses/MIT.html)
[![pipelines](https://gitlab.com/jlecomte/python/gl-webhooks/badges/master/pipeline.svg)](https://gitlab.com/jlecomte/python/gl-webhooks/pipelines)
[![coverage](https://gitlab.com/jlecomte/python/gl-webhooks/badges/master/coverage.svg)](https://jlecomte.gitlab.io/python/gl-webhooks/coverage/index.html)

# gl-webhooks

GL Webhooks is a project that provides GitLab functionalities via webhook endpoints.

It is a WSGI application written with the _Flask_ framework with _connexion_ on top of it. It can be served via _Gunicorn_ with a helper script.

## Configuration file

A template configuration file can be found in _conf/gl-webhooks.yml_.

Configuration will be taken, in order, from command line then configuration file.

# Development environment

## Setup

~~~bash
# pip and virtual env are required to be installed system wide
apt-get install python3-pip python3-venv

# create a virtualenv inside a folder called '.venv'
python3 -m venv .venv
source .venv/bin/activate

pip3 install -r requirements-dev.txt
# Run the flask server:
./bin/gl-webhooks-dev
~~~

## Production

You can run a production server as a Gunicorn WSGI application with a helper script:

~~~bash
pip3 install -r requirements.txt

./bin/gl-webhooks
~~~

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Locations

  * GitLab: [https://gitlab.com/jlecomte/python/gl-webhooks](https://gitlab.com/jlecomte/python/gl-webhooks)
  * PyPi: [https://pypi.org/project/gl-webhooks](https://pypi.org/project/gl-webhooks)

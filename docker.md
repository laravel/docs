# Docker

- [Introduction](#introduction)
- [Installation](#installation)
- ["Dockerizing" your Laravel Environment](#dockerizing)
- [Helpful Docker Commands](#helpful-valet-commands)

<a name="introduction"></a>
## Introduction

Docker provides a disposable, virtual development environment via the use of containers. This allows you to create extremely 

Developers using Docker don’t have to install and configure complex databases nor worry about switching between incompatible language toolchain versions. When an app is dockerized, that complexity is pushed into containers that are easily built, shared and run. Onboarding a co-worker to a new codebase no longer means hours spent installing software and explaining setup procedures. Code that ships with Dockerfiles is simpler to work on: Dependencies are pulled as neatly packaged Docker images and anyone with Docker and an editor installed can build and debug the app in minutes.

<a name="installation"></a>
## Installation

<div class="content-list" markdown="1">

- Install the appropriate version of [Docker](https://store.docker.com/search?offering=community&type=edition) for your environment.

</div>

Once Docker is installed, you should run `docker -v` from your command line of choice, to verify installation.

By default, the Docker daemon will each time your machine boots.

<a name="dockerizing"></a>
# "Dockerizing" your Laravel Environment

Once Docker is installed, you're ready to set up your local file structure, with some configuration to build a local development environment. Don't worry, a lot of the work is done for you already. GET THE REPO!!!

<a name="helpful-docker-commands"></a>
## Helpful Docker Commands

Command  | Description
------------- | -------------
`valet forget` | Run this command from a "parked" directory to remove it from the parked directory list.
`valet paths` | View all of your "parked" paths.
`valet restart` | Restart the Valet daemon.
`valet start` | Start the Valet daemon.
`valet stop` | Stop the Valet daemon.
`valet uninstall` | Uninstall the Valet daemon entirely.

### --- TODO: DOCKER COMMANDS
Stop/Destroy containers: sudo docker-compose down
Stop containers: sudo docker-compose stop (or <CTRL+C> if running without -d flag)
Start containers: sudo docker-compose start
Launch an interactive terminal inside container: sudo docker exec -it <container-name> bash
Run a MySQL script: docker exec -i ssdb mysql kidows -uroot -pguest < path/to/script.sql
Run Composer install: sudo docker exec -it ssweb composer install
Run Bower install: sudo docker exec -it ssweb bower install --allow-root

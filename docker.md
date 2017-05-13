# Docker

- [Introduction](#introduction)
- [Key Terms](#key-terms)
- [Installation](#installation)
- [Integrating Docker](#integrating-docker)
- [Using Docker](#using-docker)
- [Helpful Docker Commands](#helpful-docker-commands)

<a name="introduction"></a>
## Introduction

Docker provides a disposable, virtual development environment via the use of containers, defined in specific build scripts. This allows you to create extremely consistent local hosting environments matched 1:1 with a deployment build process and/or production server and shared among all developers of a project.

Developers using Docker don’t have to install and configure complex databases or web servers. When an app is dockerized, that complexity is pushed into containers that are easily built, shared and run. 

Code that ships with Dockerfiles is simpler to work on: Dependencies are pulled as neatly packaged Docker images and anyone with Docker and an editor installed can build and develop the app in minutes.

<a name="installation"></a>
## Installation

Install the appropriate version of [Docker](https://store.docker.com/search?offering=community&type=edition) for your environment.

Once Docker is installed, you should run `docker -v` from your command line terminal of choice, to verify the installation.

<a name="key-terms"></a>
## Key Terms

At the core of the Docker paradigm, are two main concepts. These are Containers and Images. Here is a brief definition of each. Don't worry if this seems overwhelming. Deep undersanding of the mechanics of Docker are not required to utilize it in your development workflow.

### Container 

A container is a runtime instance of a docker image.
A Docker container consists of

- A Docker image
- An execution environment
- A standard set of instructions

The concept is borrowed from Shipping Containers, which define a standard to ship goods globally. Docker defines a standard to ship software.

### Image

Docker images are the basis of containers. An Image is an ordered collection of root filesystem changes and the corresponding execution parameters for use within a container runtime. An image typically contains a union of layered filesystems stacked on top of each other. An image does not have state and it never changes.

<a name="integrating-docker"></a>
## Integrating Docker

Once Docker is installed, you're ready to set up your local file structure, with some configuration to build a local development environment. Don't worry, a lot of the work is done for you.

You can get a pre-dockerized Laravel install from here: https://github.com/xdega/laravel-with-docker. Or you can simply download and add the following to you existing Laravel project root: https://github.com/xdega/laravel-with-docker/tree/upgrade-only

The above is an actively maintained open-source implementation of Dockerized Laravel. Feel free to submit issues and contribute.
</div>

<a name="using-docker"></a>
## Using Docker
Once your initial integration and setup is complete, you can simply run `docker-compose up -d` from the project root, then navigate to `localhost:8080` to view your project. That's it!

### Note

The `node_modules`, and `vendor` directories are not being tracked. This is by design. You must run `composer install` and `npm install` from your project root to pull in your dependencies. This currently requires you to have Composer and Node installed on your local machine. These tools will be likely added to the Docker integration in the near future.

<a name="helpful-docker-commands"></a>
## Helpful Docker Commands

These commands are ran from your project root.

Command | Description
------------- | -------------
`docker-compose up` | Builds and runs the necessary Docker containers to run your app.
`docker-compose down` | Stop and destroy your current Docker environment.
`docker exec -it <container-name> bash` | Open an interactive bash terminal inside a given virtual container.

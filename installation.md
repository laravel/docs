# Installation

- [Meet Laravel](#meet-laravel)
- [Your First Laravel Project](#your-first-laravel-project)
    - [Getting Started On MacOS](#getting-started-on-macos)
    - [Getting Started On Windows](#getting-started-on-windows)
    - [Getting Started On Linux](#getting-started-on-linux)
- [Initial Configuration](#initial-configuration)
- [Laravel Sail](#laravel-sail)
    - [Introduction](#laravel-sail-introduction)
    - [Starting & Stopping](#starting-and-stopping-sail)
    - [Executing Commands](#executing-commands)
    - [Interacting With Databases](#interacting-with-databases)
    - [Adding Additional Services](#adding-additional-services)
    - [Container CLI](#container-cli)
- [Next Steps](#next-steps)

<a name="meet-laravel"></a>
## Meet Laravel

Laravel is a web application framework with expressive, elegant syntax. A web framework provides a structure and starting point for creating your application, allowing you to focus on creating something amazing while we sweat the details.

Laravel strives to provide an amazing developer experience, while providing powerful features such as thorough dependency injection, an expressive database abstraction layer, queues and scheduled jobs, unit and integration testing, and more.

Whether your new to PHP or web frameworks or have years of experience, Laravel is a framework that can grow with you. We'll help you take your first steps as a web developer or give you a boost as you take your expertise to the next level. We can't wait to see what you build.

<a name="your-first-laravel-project"></a>
## Your First Laravel Project

We want it to be as easy as possible to get started with Laravel. There are a variety of options for developing and running a Laravel project on your own computer. While you may wish to explore these options at a later time, Laravel provides Sail, a built-in solution for running your Laravel project using [Docker](https://www.docker.com).

Docker is a tool for running applications and services in small, light-weight "containers" which do not interfere with your local computer's installed software or configuration. This means you don't have to worry about configuring or setting up complicated development tools such as web servers and databases on your personal computer. To get started, you only need to install [Docker Desktop](https://www.docker.com/products/docker-desktop).

Laravel Sail is a light-weight command-line interface for interacting with Laravel's default Docker configuration. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience.

> {tip} Already a Docker expert? Don't worry! Everything about Sail can be customized using the `docker-compose.yml` file included with Laravel.

<a name="getting-started-on-macos"></a>
### Getting Started On MacOS

If you're developing on a Mac and [Docker Desktop](https://www.docker.com/products/docker-desktop) is already installed, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "my-app", you may run the following command in your terminal:

```bash
curl -s https://laravel.build/my-app | bash
```

Of course, you can change `my-app` in this URL to anything you like. The Laravel application's directory will be created within the directory you execute the command from.

After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration:

```bash
cd my-app

./sail up
```

Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. To continue learning more about Laravel Sail, review its [complete documentation](#laravel-sail).

<a name="getting-started-on-windows"></a>
### Getting Started On Windows

Before we create a new Laravel application on your Windows machine, make sure to install [Docker Desktop](https://www.docker.com/products/docker-desktop). Next, you should ensure that Windows Subsystem for Linux 2 (WSL2) is installed and enabled. WSL allows you to run Linux binary executables natively on Windows 10. Information on how to install and enable WSL2 can be found within Microsoft's [developer environment documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

> {tip} After installing and enabling WSL2, you should ensure that Docker Desktop is [configured to use the WSL2 backend](https://docs.docker.com/docker-for-windows/wsl/).

Next, you are ready to create your first Laravel project. Launch [Windows Terminal](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab) and begin a new terminal session for your WSL2 Linux operating system. Next, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "my-app", you may run the following command in your terminal:

```bash
curl -s https://laravel.build/my-app | bash
```

Of course, you can change `my-app` in this URL to anything you like. The Laravel application's directory will be created within the directory you execute the command from.

After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration:

```bash
cd my-app

./sail up
```

Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. To continue learning more about Laravel Sail, review its [complete documentation](#laravel-sail).

#### Developing Within WSL2

Of course, you will need to be able to modify the Laravel application files that were created within your WSL2 installation. To accomplish this, we recommend using Microsoft's [Visual Studio Code](https://code.visualstudio.com) editor and their first-party extension for [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack).

Once these tools are installed, you may open any Laravel project by executing the `code .` command from your application's root directory using Windows Terminal.

<a name="getting-started-on-linux"></a>
### Getting Started On Linux

If you're developing on Linux and [Docker](https://www.docker.com) is already installed, you can use a simple terminal command to create a new Laravel project. For example, to create a new Laravel application in a directory named "my-app", you may run the following command in your terminal:

```bash
curl -s https://laravel.build/my-app | bash
```

Of course, you can change `my-app` in this URL to anything you like. The Laravel application's directory will be created within the directory you execute the command from.

After the project has been created, you can navigate to the application directory and start Laravel Sail. Laravel Sail provides a simple command-line interface for interacting with Laravel's default Docker configuration:

```bash
cd my-app

./sail up
```

Once the application's Docker containers have been started, you can access the application in your web browser at: http://localhost. To continue learning more about Laravel Sail, review its [complete documentation](#laravel-sail).

<a name="installation-via-composer"></a>
### Installation Via Composer

If your computer already has PHP and Composer installed, you may create a new Laravel project by using Composer directly. After the application has been created, you may start Laravel's local development server using the Artisan CLI's `serve` command:

    composer create-project laravel/laravel my-app

    cd my-app

    php artisan serve

<a name="initial-configuration"></a>
## Initial Configuration

All of the configuration files for the Laravel framework are stored in the `config` directory. Each option is documented, so feel free to look through the files and get familiar with the options available to you.

However, Laravel needs almost no additional configuration out of the box. You are free to get started developing! However, you may wish to review the `config/app.php` file and its documentation. It contains several options such as `timezone` and `locale` that you may wish to change according to your application.

You may also want to configure a few additional components of Laravel, such as:

<div class="content-list" markdown="1">
- [Cache](/docs/{{version}}/cache#configuration)
- [Database](/docs/{{version}}/database#configuration)
- [Queues](/docs/{{version}}/queues#introduction)
- [Session](/docs/{{version}}/session#configuration)
</div>

<a name="laravel-sail"></a>
## Laravel Sail

<a name="laravel-sail-introduction"></a>
### Introduction

Laravel Sail is a light-weight command-line interface for interacting with Laravel's default Docker configuration. Sail provides a great starting point for building a Laravel application using PHP, MySQL, and Redis without requiring prior Docker experience.

At its heart, Sail is the `docker-compose.yml` file and the `sail` script that is stored at the root of your project. The `sail` script provides a CLI with convenient methods for interacting with the Docker containers defined by the `docker-compose.yml` file.

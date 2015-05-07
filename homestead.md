# Laravel Homestead

- [Introduction](#introduction)
- [Included Software](#included-software)
- [Installation & Setup](#installation-and-setup)
- [Daily Usage](#daily-usage)
- [Ports](#ports)
- [Blackfire Profiler](#blackfire-profiler)

<a name="introduction"></a>
## Introduction

Laravel strives to make the entire PHP development experience delightful, including your local development environment. [Vagrant](http://vagrantup.com) provides a simple, elegant way to manage and provision Virtual Machines.

Laravel Homestead is an official, pre-packaged Vagrant "box" that provides you a wonderful development environment without requiring you to install PHP, HHVM, a web server, and any other server software on your local machine. No more worrying about messing up your operating system! Vagrant boxes are completely disposable. If something goes wrong, you can destroy and re-create the box in minutes!

Homestead runs on any Windows, Mac, or Linux system, and includes the Nginx web server, PHP 5.6, MySQL, Postgres, Redis, Memcached, and all of the other goodies you need to develop amazing Laravel applications.

> **Note:** If you are using Windows, you may need to enable hardware virtualization (VT-x). It can usually be enabled via your BIOS.

Homestead is currently built and tested using Vagrant 1.7.

<a name="included-software"></a>
## Included Software

- Ubuntu 14.04
- PHP 5.6
- HHVM
- Nginx
- MySQL
- Postgres
- Node (With Bower, Grunt, and Gulp)
- Redis
- Memcached
- Beanstalkd
- [Laravel Envoy](/docs/{{version}}/envoy)
- [Blackfire Profiler](#blackfire-profiler)

<a name="installation-and-setup"></a>
## Installation & Setup

### Installing VirtualBox / VMware & Vagrant

Before launching your Homestead environment, you must install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](http://www.vagrantup.com/downloads.html). Both of these software packages provide easy-to-use visual installers for all popular operating systems.

#### VMware

In addition to VirtualBox, Homestead also supports VMware. To use the VMware provider, you will need to purchase both VMware Fusion / Desktop and the [VMware Vagrant plug-in](http://www.vagrantup.com/vmware). VMware provides much faster shared folder performance out of the box.

### Adding The Vagrant Box

Once VirtualBox / VMware and Vagrant have been installed, you should add the `laravel/homestead` box to your Vagrant installation using the following command in your terminal. It will take a few minutes to download the box, depending on your Internet connection speed:

	vagrant box add laravel/homestead

If this command fails, you may have an old version of Vagrant that requires the full URL:

	vagrant box add laravel/homestead https://atlas.hashicorp.com/laravel/boxes/homestead

### Installing Homestead

You may install Homestead manually by simply cloning the repository. Consider cloning the repository into a `Homestead` folder within your "home" directory, as the Homestead box will serve as the host to all of your Laravel (and PHP) projects:

	git clone https://github.com/laravel/homestead.git Homestead

Once you have cloned the Homestead repository, run the `bash init.sh` command from the Homestead directory to create the `Homestead.yaml` configuration file:

	bash init.sh

The `Homestead.yaml` file will be placed in your `~/.homestead` directory.

### Configure Your Provider

The `provider` key in your `Homestead.yaml` file indicates which Vagrant provider should be used: `virtualbox`, `vmware_fusion` (Mac OS X) or `vmware_workstation` (Windows). You may set this to whichever provider you prefer.

	provider: virtualbox

### Set Your SSH Key

Next, you should edit the `Homestead.yaml` file. In this file, you can configure the path to your public SSH key, as well as the folders you wish to be shared between your main machine and the Homestead virtual machine.

Don't have an SSH key? On Mac and Linux, you can generally create an SSH key pair using the following command:

	ssh-keygen -t rsa -C "you@homestead"

On Windows, you may install [Git](http://git-scm.com/) and use the `Git Bash` shell included with Git to issue the command above. Alternatively, you may use [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) and [PuTTYgen](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html).

Once you have created a SSH key, specify the key's path in the `authorize` property of your `Homestead.yaml` file.

### Configure Your Shared Folders

The `folders` property of the `Homestead.yaml` file lists all of the folders you wish to share with your Homestead environment. As files within these folders are changed, they will be kept in sync between your local machine and the Homestead environment. You may configure as many shared folders as necessary!

To enable [NFS](http://docs.vagrantup.com/v2/synced-folders/nfs.html), just add a simple flag to your synced folder:

	folders:
	    - map: ~/Code
	      to: /home/vagrant/Code
	      type: "nfs"

### Configure Your Nginx Sites

Not familiar with Nginx? No problem. The `sites` property allows you to easily map a "domain" to a folder on your Homestead environment. A sample site configuration is included in the `Homestead.yaml` file. Again, you may add as many sites to your Homestead environment as necessary. Homestead can serve as a convenient, virtualized environment for every Laravel project you are working on!

You can make any Homestead site use [HHVM](http://hhvm.com) by setting the `hhvm` option to `true`:

	sites:
	    - map: homestead.app
	      to: /home/vagrant/Code/Laravel/public
	      hhvm: true

Each site will be accessible by HTTP via port 8000 and HTTPS via port 44300.

### Bash Aliases

To add Bash aliases to your Homestead box, simply add to the `aliases` file in the root of the `~/.homestead` directory.

### Launch The Vagrant Box

Once you have edited the `Homestead.yaml` to your liking, run the `vagrant up` command from your Homestead directory.

Vagrant will boot the virtual machine, and configure your shared folders and Nginx sites automatically! To destroy the machine, you may use the `vagrant destroy --force` command.

Don't forget to add the "domains" for your Nginx sites to the `hosts` file on your machine! The `hosts` file will redirect your requests for the local domains into your Homestead environment. On Mac and Linux, this file is located at `/etc/hosts`. On Windows, it is located at `C:\Windows\System32\drivers\etc\hosts`. The lines you add to this file will look like the following:

	192.168.10.10  homestead.app

Make sure the IP address listed is the one you set in your `Homestead.yaml` file. Once you have added the domain to your `hosts` file, you can access the site via your web browser!

	http://homestead.app

To learn how to connect to your databases, read on!

<a name="daily-usage"></a>
## Daily Usage

### Connecting Via SSH

Since you will probably need to SSH into your Homestead machine frequently, consider creating an "alias" on your host machine to quickly SSH into the Homestead box:

	alias vm="ssh vagrant@127.0.0.1 -p 2222"

Once you create this alias, you can simply use the "vm" command to SSH into your Homestead machine from anywhere on your system.

Alternatively, you can use the `vagrant ssh` command from your Homestead directory.

### Connecting To Your Databases

A `homestead` database is configured for both MySQL and Postgres out of the box. For even more convenience, Laravel's `local` database configuration is set to use this database by default.

To connect to your MySQL or Postgres database from your main machine via Navicat or Sequel Pro, you should connect to `127.0.0.1` and port 33060 (MySQL) or 54320 (Postgres). The username and password for both databases is `homestead` / `secret`.

> **Note:** You should only use these non-standard ports when connecting to the databases from your main machine. You will use the default 3306 and 5432 ports in your Laravel database configuration file since Laravel is running _within_ the Virtual Machine.

### Adding Additional Sites

Once your Homestead environment is provisioned and running, you may want to add additional Nginx sites for your Laravel applications. You can run as many Laravel installations as you wish on a single Homestead environment. There are two ways to do this: First, you may simply add the sites to your `Homestead.yaml` file and then run `vagrant provision` from your Homestead directory.

> **Note:** This process is destructive. When running the `provision` command, your existing databases will be destroyed and recreated.

Alternatively, you may use the `serve` script that is available on your Homestead environment. To use the `serve` script, SSH into your Homestead environment and run the following command:

	serve domain.app /home/vagrant/Code/path/to/public/directory 80

> **Note:** After running the `serve` command, do not forget to add the new site to the `hosts` file on your main machine!

<a name="ports"></a>
## Ports

The following ports are forwarded to your Homestead environment:

- **SSH:** 2222 &rarr; Forwards To 22
- **HTTP:** 8000 &rarr; Forwards To 80
- **HTTPS:** 44300 &rarr; Forwards To 443
- **MySQL:** 33060 &rarr; Forwards To 3306
- **Postgres:** 54320 &rarr; Forwards To 5432

### Adding Additional Ports

If you wish, you may forward additional ports to the Vagrant box, as well as specify their protocol:

	ports:
	    - send: 93000
	      to: 9300
	    - send: 7777
	      to: 777
	      protocol: udp

<a name="blackfire-profiler"></a>
## Blackfire Profiler

[Blackfire Profiler](https://blackfire.io) by SensioLabs automatically gathers data about your code's execution, such as RAM, CPU time, and disk I/O. Homestead makes it a breeze to use this profiler for your own applications.

All of the proper packages have already been installed on your Homestead box, you simply need to set a Blackfire **Server** ID and token in your `Homestead.yaml` file:

	blackfire:
	    - id: your-server-id
	      token: your-server-token
	      client-id: your-client-id
	      client-token: your-client-token

Once you have configured your Blackfire credentials, re-provision the box using `vagrant provision` from your Homestead directory. Of course, be sure to review the [Blackfire documentation](https://blackfire.io/getting-started) to learn how to install the Blackfire companion extension for your web browser.

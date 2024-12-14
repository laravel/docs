# Laravel Valet

- [Introduction](#introduction)
    - [Valet Or Homestead](#valet-or-homestead)
- [Installation](#installation)
- [Release Notes](#release-notes)
- [Serving Sites](#serving-sites)
    - [The "Park" Command](#the-park-command)
    - [The "Link" Command](#the-link-command)
    - [Securing Sites With TLS](#securing-sites)
- [Sharing Sites](#sharing-sites)
- [Viewing Logs](#viewing-logs)
- [Custom Valet Drivers](#custom-valet-drivers)
- [Other Valet Commands](#other-valet-commands)

<a name="introduction"></a>
## Introduction

Valet is a Laravel development environment for Mac minimalists. No Vagrant, No Apache, No Nginx, No `/etc/hosts` file. You can even share your sites publicly using local tunnels. _Yeah, we like it too._

Laravel Valet configures your Mac to always run [Caddy](https://caddyserver.com) in the background when your machine starts. Then, using [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq), Valet proxies all requests on the `*.dev` domain to point to sites installed on your local machine.

In other words, a blazing fast Laravel development environment that uses roughly 7 MB of RAM. Valet isn't a complete replacement for Vagrant or Homestead, but provides a great alternative if you want flexible basics, prefer extreme speed, or are working on a machine with a limited amount of RAM.

Out of the box, Valet support includes, but is not limited to:

<div class="content-list" markdown="1">

- [Laravel](https://laravel.com)
- [Lumen](https://lumen.laravel.com)
- [Symfony](https://symfony.com)
- [Zend](http://framework.zend.com)
- [CakePHP 3](http://cakephp.org)
- [WordPress](https://wordpress.org)
- [Bedrock](https://roots.io/bedrock)
- [Craft](https://craftcms.com)
- [Statamic](https://statamic.com)
- [Jigsaw](http://jigsaw.tighten.co)
- Static HTML

</div>

However, you may extend Valet with your own [custom drivers](#custom-valet-drivers).

<a name="valet-or-homestead"></a>
### Valet Or Homestead

As you may know, Laravel offers [Homestead](/docs/{{version}}/homestead), another local Laravel development environment. Homestead and Valet differ in regards to their intended audience and their approach to local development. Homestead offers an entire Ubuntu virtual machine with automated Nginx configuration. Homestead is a wonderful choice if you want a fully virtualized Linux development environment or are on Windows / Linux.

Valet only supports Mac, and requires you to install PHP and a database server directly onto your local machine. This is easily achieved by using [Homebrew](http://brew.sh/) with commands like `brew install php70` and `brew install mariadb`. Valet provides a blazing fast local development environment with minimal resource consumption, so it's great for developers who only require PHP / MySQL and do not need a fully virtualized development environment.

Both Valet and Homestead are great choices for configuring your Laravel development environment. Which one you choose will depend on your personal taste and your team's needs.

<a name="installation"></a>
## Installation

**Valet requires the Mac operating system and [Homebrew](http://brew.sh/). Before installation, you should make sure that no other programs such as Apache or Nginx are binding to your local machine's port 80.**

<div class="content-list" markdown="1">

- Install or update [Homebrew](http://brew.sh/) to the latest version using `brew update`.
- Install PHP 7.0 using Homebrew via `brew install homebrew/php/php70`.
- Install Valet with Composer via `composer global require laravel/valet`. Make sure the `~/.composer/vendor/bin` directory is in your system's "PATH".
- Run the `valet install` command. This will configure and install Valet and DnsMasq, and register Valet's daemon to launch when your system starts.

</div>

Once Valet is installed, try pinging any `*.dev` domain on your terminal using a command such as `ping foobar.dev`. If Valet is installed correctly you should see this domain responding on `127.0.0.1`.

Valet will automatically start its daemon each time your machine boots. There is no need to run `valet start` or `valet install` ever again once the initial Valet installation is complete.

#### Using Another Domain

By default, Valet serves your projects using the `.dev` TLD. If you'd like to use another domain, you can do so using the `valet domain tld-name` command.

For example, if you'd like to use `.app` instead of `.dev`, run `valet domain app` and Valet will start serving your projects at `*.app` automatically.

#### Database

If you need a database, try MariaDB by running `brew install mariadb` on your command line. You can connect to the database at `127.0.0.1` using the `root` username and an empty string for the password.

<a name="release-notes"></a>
## Release Notes

### Version 1.1.5

The 1.1.5 release of Valet brings a variety of internal improvements.

#### Upgrade Instructions

After updating your Valet installation using `composer global update`, you should run the `valet install` command in your terminal.

### Version 1.1.0

The 1.1.0 release of Valet brings a variety of great improvements. The built-in PHP server has been replaced with [Caddy](https://caddyserver.com/) for serving incoming HTTP requests. Introducing Caddy allows for a variety of future improvements and allows Valet sites to make HTTP requests to other Valet sites without blocking the built-in PHP server.

#### Upgrade Instructions

After updating your Valet installation using `composer global update`, you should run the `valet install` command in your terminal to create the new Caddy daemon file on your system.

<a name="serving-sites"></a>
## Serving Sites

Once Valet is installed, you're ready to start serving sites. Valet provides two commands to help you serve your Laravel sites: `park` and `link`.

<a name="the-park-command"></a>
### The `park` Command

<div class="content-list" markdown="1">

- Create a new directory on your Mac by running something like `mkdir ~/Sites`. Next, `cd ~/Sites` and run `valet park`. This command will register your current working directory as a path that Valet should search for sites.
- Next, create a new Laravel site within this directory: `laravel new blog`.
- Open `http://blog.dev` in your browser.

</div>

**That's all there is to it.** Now, any Laravel project you create within your "parked" directory will automatically be served using the `http://folder-name.dev` convention.

<a name="the-link-command"></a>
### The `link` Command

The `link` command may also be used to serve your Laravel sites. This command is useful if you want to serve a single site in a directory and not the entire directory.

<div class="content-list" markdown="1">

- To use the command, navigate to one of your projects and run `valet link app-name` in your terminal. Valet will create a symbolic link in `~/.valet/Sites` which points to your current working directory.
- After running the `link` command, you can access the site in your browser at `http://app-name.dev`.

</div>

To see a listing of all of your linked directories, run the `valet links` command. You may use `valet unlink app-name` to destroy the symbolic link.

<a name="securing-sites"></a>
### Securing Sites With TLS

By default, Valet serves sites over plain HTTP. However, if you would like to serve a site over encrypted TLS using HTTP/2, use the `secure` command. For example, if your site is being served by Valet on the `laravel.dev` domain, you should run the following command to secure it:

    valet secure laravel

To "unsecure" a site and revert back to serving its traffic over plain HTTP, use the `unsecure` command. Like the `secure` command, this command accepts the host name that you wish to unsecure:

    valet unsecure laravel

<a name="sharing-sites"></a>
## Sharing Sites

Valet even includes a command to share your local sites with the world. No additional software installation is required once Valet is installed.

To share a site, navigate to the site's directory in your terminal and run the `valet share` command. A publicly accessible URL will be inserted into your clipboard and is ready to paste directly into your browser. That's it.

To stop sharing your site, hit `Control + C` to cancel the process.

<a name="viewing-logs"></a>
## Viewing Logs

If you would like to stream all of the logs for all of your sites to your terminal, run the `valet logs` command. New log entries will display in your terminal as they occur. This is a great way to stay on top of all of your log files without ever having to leave your terminal.

<a name="custom-valet-drivers"></a>
## Custom Valet Drivers

You can write your own Valet "driver" to serve PHP applications running on another framework or CMS that is not natively supported by Valet. When you install Valet, a `~/.valet/Drivers` directory is created which contains a `SampleValetDriver.php` file. This file contains a sample driver implementation to demonstrate how to write a custom driver. Writing a driver only requires you to implement three methods: `serves`, `isStaticFile`, and `frontControllerPath`.

All three methods receive the `$sitePath`, `$siteName`, and `$uri` values as their arguments. The `$sitePath` is the fully qualified path to the site being served on your machine, such as `/Users/Lisa/Sites/my-project`. The `$siteName` is the "host" / "site name" portion of the domain (`my-project`). The `$uri` is the incoming request URI (`/foo/bar`).

Once you have completed your custom Valet driver, place it in the `~/.valet/Drivers` directory using the `FrameworkValetDriver.php` naming convention. For example, if you are writing a custom valet driver for WordPress, your file name should be `WordPressValetDriver.php`.

Let's take at a sample implementation of each method your custom Valet driver should implement.

#### The `serves` Method

The `serves` method should return `true` if your driver should handle the incoming request. Otherwise, the method should return `false`. So, within this method you should attempt to determine if the given `$sitePath` contains a project of the type you are trying to serve.

For example, let's pretend we are writing a `WordPressValetDriver`. Our serve method might look something like this:

    /**
     * Determine if the driver serves the request.
     *
     * @param  string  $sitePath
     * @param  string  $siteName
     * @param  string  $uri
     * @return void
     */
    public function serves($sitePath, $siteName, $uri)
    {
        return is_dir($sitePath.'/wp-admin');
    }

#### The `isStaticFile` Method

The `isStaticFile` should determine if the incoming request is for a file that is "static", such as an image or a stylesheet. If the file is static, the method should return the fully qualified path to the static file on disk. If the incoming request is not for a static file, the method should return `false`:

    /**
     * Determine if the incoming request is for a static file.
     *
     * @param  string  $sitePath
     * @param  string  $siteName
     * @param  string  $uri
     * @return string|false
     */
    public function isStaticFile($sitePath, $siteName, $uri)
    {
        if (file_exists($staticFilePath = $sitePath.'/public/'.$uri)) {
            return $staticFilePath;
        }

        return false;
    }

> **Note:** The `isStaticFile` method will only be called if the `serves` method returns `true` for the incoming request and the request URI is not `/`.

#### The `frontControllerPath` Method

The `frontControllerPath` method should return the fully qualified path to your application's "front controller", which is typically your "index.php" file or equivalent:

    /**
     * Get the fully resolved path to the application's front controller.
     *
     * @param  string  $sitePath
     * @param  string  $siteName
     * @param  string  $uri
     * @return string
     */
    public function frontControllerPath($sitePath, $siteName, $uri)
    {
        return $sitePath.'/public/index.php';
    }

<a name="other-valet-commands"></a>
## Other Valet Commands

Command  | Description
------------- | -------------
`valet forget` | Run this command from a "parked" directory to remove it from the parked directory list.
`valet paths` | View all of your "parked" paths.
`valet restart` | Restart the Valet daemon.
`valet start` | Start the Valet daemon.
`valet stop` | Stop the Valet daemon.
`valet uninstall` | Uninstall the Valet daemon entirely.

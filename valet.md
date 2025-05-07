# Laravel Valet

- [Introduction](#introduction)
- [Installation](#installation)
    - [Upgrading Valet](#upgrading-valet)
- [Serving Sites](#serving-sites)
    - [The "Park" Command](#the-park-command)
    - [The "Link" Command](#the-link-command)
    - [Securing Sites With TLS](#securing-sites)
    - [Serving a Default Site](#serving-a-default-site)
    - [Per-Site PHP Versions](#per-site-php-versions)
- [Sharing Sites](#sharing-sites)
    - [Sharing Sites on Your Local Network](#sharing-sites-on-your-local-network)
- [Site Specific Environment Variables](#site-specific-environment-variables)
- [Proxying Services](#proxying-services)
- [Custom Valet Drivers](#custom-valet-drivers)
    - [Local Drivers](#local-drivers)
- [Other Valet Commands](#other-valet-commands)
- [Valet Directories and Files](#valet-directories-and-files)
    - [Disk Access](#disk-access)

<a name="introduction"></a>
## Introduction

> [!NOTE]
> Looking for an even easier way to develop Laravel applications on macOS or Windows? Check out [Laravel Herd](https://herd.laravel.com). Herd includes everything you need to get started with Laravel development, including Valet, PHP, and Composer.

[Laravel Valet](https://github.com/laravel/valet) is a development environment for macOS minimalists. Laravel Valet configures your Mac to always run [Nginx](https://www.nginx.com/) in the background when your machine starts. Then, using [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq), Valet proxies all requests on the `*.test` domain to point to sites installed on your local machine.

In other words, Valet is a blazing fast Laravel development environment that uses roughly 7 MB of RAM. Valet isn't a complete replacement for [Sail](/docs/{{version}}/sail) or [Homestead](/docs/{{version}}/homestead), but provides a great alternative if you want flexible basics, prefer extreme speed, or are working on a machine with a limited amount of RAM.

Out of the box, Valet support includes, but is not limited to:

<style>
    #valet-support > ul {
        column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
        line-height: 1.9;
    }
</style>

<div id="valet-support" markdown="1">

- [Laravel](https://laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [CakePHP 3](https://cakephp.org)
- [ConcreteCMS](https://www.concretecms.com/)
- [Contao](https://contao.org/en/)
- [Craft](https://craftcms.com)
- [Drupal](https://www.drupal.org/)
- [ExpressionEngine](https://www.expressionengine.com/)
- [Jigsaw](https://jigsaw.tighten.co)
- [Joomla](https://www.joomla.org/)
- [Katana](https://github.com/themsaid/katana)
- [Kirby](https://getkirby.com/)
- [Magento](https://magento.com/)
- [OctoberCMS](https://octobercms.com/)
- [Sculpin](https://sculpin.io/)
- [Slim](https://www.slimframework.com)
- [Statamic](https://statamic.com)
- Static HTML
- [Symfony](https://symfony.com)
- [WordPress](https://wordpress.org)
- [Zend](https://framework.zend.com)

</div>

However, you may extend Valet with your own [custom drivers](#custom-valet-drivers).

<a name="installation"></a>
## Installation

> [!WARNING]
> Valet requires macOS and [Homebrew](https://brew.sh/). Before installation, you should make sure that no other programs such as Apache or Nginx are binding to your local machine's port 80.

To get started, you first need to ensure that Homebrew is up to date using the `update` command:

```shell
brew update
```

Next, you should use Homebrew to install PHP:

```shell
brew install php
```

After installing PHP, you are ready to install the [Composer package manager](https://getcomposer.org). In addition, you should make sure the `$HOME/.composer/vendor/bin` directory is in your system's "PATH". After Composer has been installed, you may install Laravel Valet as a global Composer package:

```shell
composer global require laravel/valet
```

Finally, you may execute Valet's `install` command. This will configure and install Valet and DnsMasq. In addition, the daemons Valet depends on will be configured to launch when your system starts:

```shell
valet install
```

Once Valet is installed, try pinging any `*.test` domain on your terminal using a command such as `ping foobar.test`. If Valet is installed correctly you should see this domain responding on `127.0.0.1`.

Valet will automatically start its required services each time your machine boots.

<a name="php-versions"></a>
#### PHP Versions

> [!NOTE]
> Instead of modifying your global PHP version, you can instruct Valet to use per-site PHP versions via the `isolate` [command](#per-site-php-versions).

Valet allows you to switch PHP versions using the `valet use php@version` command. Valet will install the specified PHP version via Homebrew if it is not already installed:

```shell
valet use php@8.2

valet use php
```

You may also create a `.valetrc` file in the root of your project. The `.valetrc` file should contain the PHP version the site should use:

```shell
php=php@8.2
```

Once this file has been created, you may simply execute the `valet use` command and the command will determine the site's preferred PHP version by reading the file.

> [!WARNING]
> Valet only serves one PHP version at a time, even if you have multiple PHP versions installed.

<a name="database"></a>
#### Database

If your application needs a database, check out [DBngin](https://dbngin.com), which provides a free, all-in-one database management tool that includes MySQL, PostgreSQL, and Redis. After DBngin has been installed, you can connect to your database at `127.0.0.1` using the `root` username and an empty string for the password.

<a name="resetting-your-installation"></a>
#### Resetting Your Installation

If you are having trouble getting your Valet installation to run properly, executing the `composer global require laravel/valet` command followed by `valet install` will reset your installation and can solve a variety of problems. In rare cases, it may be necessary to "hard reset" Valet by executing `valet uninstall --force` followed by `valet install`.

<a name="upgrading-valet"></a>
### Upgrading Valet

You may update your Valet installation by executing the `composer global require laravel/valet` command in your terminal. After upgrading, it is good practice to run the `valet install` command so Valet can make additional upgrades to your configuration files if necessary.

<a name="upgrading-to-valet-4"></a>
#### Upgrading to Valet 4

If you're upgrading from Valet 3 to Valet 4, take the following steps to properly upgrade your Valet installation:

<div class="content-list" markdown="1">

- If you've added `.valetphprc` files to customize your site's PHP version, rename each `.valetphprc` file to `.valetrc`. Then, prepend `php=` to the existing content of the `.valetrc` file.
- Update any custom drivers to match the namespace, extension, type-hints, and return type-hints of the new driver system. You may consult Valet's [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php) as an example.
- If you use PHP 7.1 - 7.4 to serve your sites, make sure you still use Homebrew to install a version of PHP that's 8.0 or higher, as Valet will use this version, even if it's not your primary linked version, to run some of its scripts.

</div>

<a name="serving-sites"></a>
## Serving Sites

Once Valet is installed, you're ready to start serving your Laravel applications. Valet provides two commands to help you serve your applications: `park` and `link`.

<a name="the-park-command"></a>
### The `park` Command

The `park` command registers a directory on your machine that contains your applications. Once the directory has been "parked" with Valet, all of the directories within that directory will be accessible in your web browser at `http://<directory-name>.test`:

```shell
cd ~/Sites

valet park
```

That's all there is to it. Now, any application you create within your "parked" directory will automatically be served using the `http://<directory-name>.test` convention. So, if your parked directory contains a directory named "laravel", the application within that directory will be accessible at `http://laravel.test`. In addition, Valet automatically allows you to access the site using wildcard subdomains (`http://foo.laravel.test`).

<a name="the-link-command"></a>
### The `link` Command

The `link` command can also be used to serve your Laravel applications. This command is useful if you want to serve a single site in a directory and not the entire directory:

```shell
cd ~/Sites/laravel

valet link
```

Once an application has been linked to Valet using the `link` command, you may access the application using its directory name. So, the site that was linked in the example above may be accessed at `http://laravel.test`. In addition, Valet automatically allows you to access the site using wildcard sub-domains (`http://foo.laravel.test`).

If you would like to serve the application at a different hostname, you may pass the hostname to the `link` command. For example, you may run the following command to make an application available at `http://application.test`:

```shell
cd ~/Sites/laravel

valet link application
```

Of course, you may also serve applications on subdomains using the `link` command:

```shell
valet link api.application
```

You may execute the `links` command to display a list of all of your linked directories:

```shell
valet links
```

The `unlink` command may be used to destroy the symbolic link for a site:

```shell
cd ~/Sites/laravel

valet unlink
```

<a name="securing-sites"></a>
### Securing Sites With TLS

By default, Valet serves sites over HTTP. However, if you would like to serve a site over encrypted TLS using HTTP/2, you may use the `secure` command. For example, if your site is being served by Valet on the `laravel.test` domain, you should run the following command to secure it:

```shell
valet secure laravel
```

To "unsecure" a site and revert back to serving its traffic over plain HTTP, use the `unsecure` command. Like the `secure` command, this command accepts the hostname that you wish to unsecure:

```shell
valet unsecure laravel
```

<a name="serving-a-default-site"></a>
### Serving a Default Site

Sometimes, you may wish to configure Valet to serve a "default" site instead of a `404` when visiting an unknown `test` domain. To accomplish this, you may add a `default` option to your `~/.config/valet/config.json` configuration file containing the path to the site that should serve as your default site:

    "default": "/Users/Sally/Sites/example-site",

<a name="per-site-php-versions"></a>
### Per-Site PHP Versions

By default, Valet uses your global PHP installation to serve your sites. However, if you need to support multiple PHP versions across various sites, you may use the `isolate` command to specify which PHP version a particular site should use. The `isolate` command configures Valet to use the specified PHP version for the site located in your current working directory:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```

If your site name does not match the name of the directory that contains it, you may specify the site name using the `--site` option:

```shell
valet isolate php@8.0 --site="site-name"
```

For convenience, you may use the `valet php`, `composer`, and `which-php` commands to proxy calls to the appropriate PHP CLI or tool based on the site's configured PHP version:

```shell
valet php
valet composer
valet which-php
```

You may execute the `isolated` command to display a list of all of your isolated sites and their PHP versions:

```shell
valet isolated
```

To revert a site back to Valet's globally installed PHP version, you may invoke the `unisolate` command from the site's root directory:

```shell
valet unisolate
```

<a name="sharing-sites"></a>
## Sharing Sites

Valet includes a command to share your local sites with the world, providing an easy way to test your site on mobile devices or share it with team members and clients.

Out of the box, Valet supports sharing your sites via ngrok or Expose. Before sharing a site, you should update your Valet configuration using the `share-tool` command, specifying `ngrok`, `expose`, or  `cloudflared`:

```shell
valet share-tool ngrok
```

If you choose a tool and don't have it installed via Homebrew (for ngrok and cloudflared) or Composer (for Expose), Valet will automatically prompt you to install it. Of course, both tools require you to authenticate your ngrok or Expose account before you can start sharing sites.

To share a site, navigate to the site's directory in your terminal and run Valet's `share` command. A publicly accessible URL will be placed into your clipboard and is ready to paste directly into your browser or to be shared with your team:

```shell
cd ~/Sites/laravel

valet share
```

To stop sharing your site, you may press `Control + C`.

> [!WARNING]
> If you're using a custom DNS server (like `1.1.1.1`), ngrok sharing may not work correctly. If this is the case on your machine, open your Mac's system settings, go to the Network settings, open the Advanced settings, then go the DNS tab and add `127.0.0.1` as your first DNS server.

<a name="sharing-sites-via-ngrok"></a>
#### Sharing Sites via Ngrok

Sharing your site using ngrok requires you to [create an ngrok account](https://dashboard.ngrok.com/signup) and [set up an authentication token](https://dashboard.ngrok.com/get-started/your-authtoken). Once you have an authentication token, you can update your Valet configuration with that token:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```

> [!NOTE]
> You may pass additional ngrok parameters to the share command, such as `valet share --region=eu`. For more information, consult the [ngrok documentation](https://ngrok.com/docs).

<a name="sharing-sites-via-expose"></a>
#### Sharing Sites via Expose

Sharing your site using Expose requires you to [create an Expose account](https://expose.dev/register) and [authenticate with Expose via your authentication token](https://expose.dev/docs/getting-started/getting-your-token).

You may consult the [Expose documentation](https://expose.dev/docs) for information regarding the additional command-line parameters it supports.

<a name="sharing-sites-on-your-local-network"></a>
### Sharing Sites on Your Local Network

Valet restricts incoming traffic to the internal `127.0.0.1` interface by default so that your development machine isn't exposed to security risks from the Internet.

If you wish to allow other devices on your local network to access the Valet sites on your machine via your machine's IP address (eg: `192.168.1.10/application.test`), you will need to manually edit the appropriate Nginx configuration file for that site to remove the restriction on the `listen` directive. You should remove the `127.0.0.1:` prefix on the `listen` directive for ports 80 and 443.

If you have not run `valet secure` on the project, you can open up network access for all non-HTTPS sites by editing the `/usr/local/etc/nginx/valet/valet.conf` file. However, if you're serving the project site over HTTPS (you have run `valet secure` for the site) then you should edit the `~/.config/valet/Nginx/app-name.test` file.

Once you have updated your Nginx configuration, run the `valet restart` command to apply the configuration changes.

<a name="site-specific-environment-variables"></a>
## Site Specific Environment Variables

Some applications using other frameworks may depend on server environment variables but do not provide a way for those variables to be configured within your project. Valet allows you to configure site specific environment variables by adding a `.valet-env.php` file within the root of your project. This file should return an array of site / environment variable pairs which will be added to the global `$_SERVER` array for each site specified in the array:

```php
<?php

return [
    // Set $_SERVER['key'] to "value" for the laravel.test site...
    'laravel' => [
        'key' => 'value',
    ],

    // Set $_SERVER['key'] to "value" for all sites...
    '*' => [
        'key' => 'value',
    ],
];
```

<a name="proxying-services"></a>
## Proxying Services

Sometimes you may wish to proxy a Valet domain to another service on your local machine. For example, you may occasionally need to run Valet while also running a separate site in Docker; however, Valet and Docker can't both bind to port 80 at the same time.

To solve this, you may use the `proxy` command to generate a proxy. For example, you may proxy all traffic from `http://elasticsearch.test` to `http://127.0.0.1:9200`:

```shell
# Proxy over HTTP...
valet proxy elasticsearch http://127.0.0.1:9200

# Proxy over TLS + HTTP/2...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```

You may remove a proxy using the `unproxy` command:

```shell
valet unproxy elasticsearch
```

You may use the `proxies` command to list all site configurations that are proxied:

```shell
valet proxies
```

<a name="custom-valet-drivers"></a>
## Custom Valet Drivers

You can write your own Valet "driver" to serve PHP applications running on a framework or CMS that is not natively supported by Valet. When you install Valet, a `~/.config/valet/Drivers` directory is created which contains a `SampleValetDriver.php` file. This file contains a sample driver implementation to demonstrate how to write a custom driver. Writing a driver only requires you to implement three methods: `serves`, `isStaticFile`, and `frontControllerPath`.

All three methods receive the `$sitePath`, `$siteName`, and `$uri` values as their arguments. The `$sitePath` is the fully qualified path to the site being served on your machine, such as `/Users/Lisa/Sites/my-project`. The `$siteName` is the "host" / "site name" portion of the domain (`my-project`). The `$uri` is the incoming request URI (`/foo/bar`).

Once you have completed your custom Valet driver, place it in the `~/.config/valet/Drivers` directory using the `FrameworkValetDriver.php` naming convention. For example, if you are writing a custom valet driver for WordPress, your filename should be `WordPressValetDriver.php`.

Let's take a look at a sample implementation of each method your custom Valet driver should implement.

<a name="the-serves-method"></a>
#### The `serves` Method

The `serves` method should return `true` if your driver should handle the incoming request. Otherwise, the method should return `false`. So, within this method, you should attempt to determine if the given `$sitePath` contains a project of the type you are trying to serve.

For example, let's imagine we are writing a `WordPressValetDriver`. Our `serves` method might look something like this:

```php
/**
 * Determine if the driver serves the request.
 */
public function serves(string $sitePath, string $siteName, string $uri): bool
{
    return is_dir($sitePath.'/wp-admin');
}
```

<a name="the-isstaticfile-method"></a>
#### The `isStaticFile` Method

The `isStaticFile` should determine if the incoming request is for a file that is "static", such as an image or a stylesheet. If the file is static, the method should return the fully qualified path to the static file on disk. If the incoming request is not for a static file, the method should return `false`:

```php
/**
 * Determine if the incoming request is for a static file.
 *
 * @return string|false
 */
public function isStaticFile(string $sitePath, string $siteName, string $uri)
{
    if (file_exists($staticFilePath = $sitePath.'/public/'.$uri)) {
        return $staticFilePath;
    }

    return false;
}
```

> [!WARNING]
> The `isStaticFile` method will only be called if the `serves` method returns `true` for the incoming request and the request URI is not `/`.

<a name="the-frontcontrollerpath-method"></a>
#### The `frontControllerPath` Method

The `frontControllerPath` method should return the fully qualified path to your application's "front controller", which is typically an "index.php" file or equivalent:

```php
/**
 * Get the fully resolved path to the application's front controller.
 */
public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
{
    return $sitePath.'/public/index.php';
}
```

<a name="local-drivers"></a>
### Local Drivers

If you would like to define a custom Valet driver for a single application, create a `LocalValetDriver.php` file in the application's root directory. Your custom driver may extend the base `ValetDriver` class or extend an existing application specific driver such as the `LaravelValetDriver`:

```php
use Valet\Drivers\LaravelValetDriver;

class LocalValetDriver extends LaravelValetDriver
{
    /**
     * Determine if the driver serves the request.
     */
    public function serves(string $sitePath, string $siteName, string $uri): bool
    {
        return true;
    }

    /**
     * Get the fully resolved path to the application's front controller.
     */
    public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
    {
        return $sitePath.'/public_html/index.php';
    }
}
```

<a name="other-valet-commands"></a>
## Other Valet Commands

<div class="overflow-auto">

| Command | Description |
| --- | --- |
| `valet list` | Display a list of all Valet commands. |
| `valet diagnose` | Output diagnostics to aid in debugging Valet. |
| `valet directory-listing` | Determine directory-listing behavior. Default is "off", which renders a 404 page for directories. |
| `valet forget` | Run this command from a "parked" directory to remove it from the parked directory list. |
| `valet log` | View a list of logs which are written by Valet's services. |
| `valet paths` | View all of your "parked" paths. |
| `valet restart` | Restart the Valet daemons. |
| `valet start` | Start the Valet daemons. |
| `valet stop` | Stop the Valet daemons. |
| `valet trust` | Add sudoers files for Brew and Valet to allow Valet commands to be run without prompting for your password. |
| `valet uninstall` | Uninstall Valet: shows instructions for manual uninstall. Pass the `--force` option to aggressively delete all of Valet's resources. |

</div>

<a name="valet-directories-and-files"></a>
## Valet Directories and Files

You may find the following directory and file information helpful while troubleshooting issues with your Valet environment:

#### `~/.config/valet`

Contains all of Valet's configuration. You may wish to maintain a backup of this directory.

#### `~/.config/valet/dnsmasq.d/`

This directory contains DNSMasq's configuration.

#### `~/.config/valet/Drivers/`

This directory contains Valet's drivers. Drivers determine how a particular framework / CMS is served.

#### `~/.config/valet/Nginx/`

This directory contains all of Valet's Nginx site configurations. These files are rebuilt when running the `install` and `secure` commands.

#### `~/.config/valet/Sites/`

This directory contains all of the symbolic links for your [linked projects](#the-link-command).

#### `~/.config/valet/config.json`

This file is Valet's master configuration file.

#### `~/.config/valet/valet.sock`

This file is the PHP-FPM socket used by Valet's Nginx installation. This will only exist if PHP is running properly.

#### `~/.config/valet/Log/fpm-php.www.log`

This file is the user log for PHP errors.

#### `~/.config/valet/Log/nginx-error.log`

This file is the user log for Nginx errors.

#### `/usr/local/var/log/php-fpm.log`

This file is the system log for PHP-FPM errors.

#### `/usr/local/var/log/nginx`

This directory contains the Nginx access and error logs.

#### `/usr/local/etc/php/X.X/conf.d`

This directory contains the `*.ini` files for various PHP configuration settings.

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

This file is the PHP-FPM pool configuration file.

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

This file is the default Nginx configuration used for building SSL certificates for your sites.

<a name="disk-access"></a>
### Disk Access

Since macOS 10.14, [access to some files and directories is restricted by default](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf). These restrictions include the Desktop, Documents, and Downloads directories. In addition, network volume and removable volume access is restricted. Therefore, Valet recommends your site folders are located outside of these protected locations.

However, if you wish to serve sites from within one of those locations, you will need to give Nginx "Full Disk Access". Otherwise, you may encounter server errors or other unpredictable behavior from Nginx, especially when serving static assets. Typically, macOS will automatically prompt you to grant Nginx full access to these locations. Or, you may do so manually via `System Preferences` > `Security & Privacy` > `Privacy` and selecting `Full Disk Access`. Next, enable any `nginx` entries in the main window pane.

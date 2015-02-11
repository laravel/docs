# Contribution Guide

- [Introduction](#introduction)
- [Core Development Discussion](#core-development-discussion)
- [New Features](#new-features)
- [Bugs](#bugs)
- [Creating Liferaft Applications](#creating-liferaft-applications)
- [Grabbing Liferaft Applications](#grabbing-liferaft-applications)
- [Which Branch?](#which-branch)
- [Security Vulnerabilities](#security-vulnerabilities)
- [Coding Style](#coding-style)

<a name="introduction"></a>
## Introduction

Laravel is an open-source project and anyone may contribute to Laravel for its improvement. We welcome contributors, regardless of skill level, gender, race, religion, or nationality. Having a diverse, vibrant community is one of the core values of the framework!

To encourage active collaboration, Laravel currently only accepts pull requests, not bug reports. "Bug reports" may be sent in the form of a pull request containing a failing unit test. Alternatively, a demonstration of the bug within a sandbox Laravel application may be sent as a pull request to the [main Laravel repository](https://github.com/laravel/laravel). A failing unit test or sandbox application provides the development team "proof" that the bug exists, and, after the development team addresses the bug, serves as a reliable indicator that the bug remains fixed.

The Laravel source code is managed on Github, and there are repositories for each of the Laravel projects:

- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Application](https://github.com/laravel/laravel)
- [Laravel Documentation](https://github.com/laravel/docs)
- [Laravel Cashier](https://github.com/laravel/cashier)
- [Laravel Envoy](https://github.com/laravel/envoy)
- [Laravel Homestead](https://github.com/laravel/homestead)
- [Laravel Homestead Build Scripts](https://github.com/laravel/settler)
- [Laravel Website](https://github.com/laravel/laravel.com)
- [Laravel Art](https://github.com/laravel/art)

<a name="core-development-discussion"></a>
## Core Development Discussion

Discussion regarding bugs, new features, and implementation of existing features takes place in the `#laravel-dev` IRC channel (Freenode). Taylor Otwell, the maintainer of Laravel, is typically present in the channel on weekdays from 8am-5pm (UTC-06:00 or America/Chicago), and sporadically present in the channel at other times.

The `#laravel-dev` IRC channel is open to all. All are welcome to join the channel either to participate or simply observe the discussions!

<a name="new-features"></a>
## New Features

Before sending pull requests for new features, please contact Taylor Otwell via the `#laravel-dev` IRC channel (Freenode). If the feature is found to be a good fit for the framework, you are free to make a pull request. If the feature is rejected, don't give up! You are still free to turn your feature into a package which can be released to the world via [Packagist](https://packagist.org/).

When adding new features, don't forget to add unit tests! Unit tests help ensure the stability and reliability of the framework as new features are added.

<a name="bugs"></a>
## Bugs

### Via Unit Test

Pull requests for bugs may be sent without prior discussion with the Laravel development team. When submitting a bug fix, try to include a unit test that ensures the bug never appears again!

If you believe you have found a bug in the framework, but are unsure how to fix it, please send a pull request containing a failing unit test. A failing unit test provides the development team "proof" that the bug exists, and, after the development team addresses the bug, serves as a reliable indicator that the bug remains fixed.

If are unsure how to write a failing unit test for a bug, review the other unit tests included with the framework. If you're still lost, you may ask for help in the `#laravel` IRC channel (Freenode).

### Via Laravel Liferaft

If you aren't able to write a unit test for your issue, Laravel Liferaft allows you to create a demo application that recreates the issue. Liferaft can even automate the forking and sending of pull requests to the Laravel repository. Once your Liferaft application is submitted, a Laravel maintainer can run your application on [Homestead](/docs/4.1/4.2/homestead) and review your issue.

<a name="creating-liferaft-applications"></a>
## Creating Liferaft Applications

Laravel Liferaft provides a fresh, innovative way to contribute to Laravel. First, you will need to install the Liferaft CLI tool via Composer:

### Installing Liferaft

	composer global require "laravel/liferaft=~1.0"

Make sure to place the `~/.composer/vendor/bin` directory in your PATH so the `liferaft` executable is found when you run the `liferaft` command in your terminal.

### Authenticating With GitHub

Before getting started with Liferaft, you need to register a GitHub personal access token. You can generate a personal access token from your [GitHub settings panel](https://github.com/settings/applications). The default scopes selected by GitHub will be sufficient; however, if you wish, you may grant the `delete_repo` scope so Liferaft can delete your old sandbox applications.

	liferaft auth my-github-token

### Create A New Liferaft Application

To create a new Liferaft application, just use the `new` command:

	liferaft new my-bug-fix

This command will do several things. First, it will fork the [Laravel GitHub repository](https://github.com/laravel/laravel) to your GitHub account. Next, it will clone the forked repository to your machine and install the Composer dependencies. Once the repository has been installed, you can begin recreating your issue within the Liferaft application!

### Recreating Your Issue

After creating a Liferaft application, simply recreate your issue. You are free to define routes, create Eloquent models, and even create database migrations! The only requirement is that your application is able to run on a fresh [Laravel Homestead](/docs/4.1/4.2/homestead) virtual machine. This allows Laravel maintainers to easily run your application on their own machines.

Once you have recreated your issue within the Liferaft application, you're ready to send it back to the Laravel repository for review!

### Send Your Application For Review

Once you have recreated your issue, it's almost time to send it for review! However, you should first complete the `liferaft.md` file that was generated in your Liferaft application. The first line of this file will be the title of your pull request. The remaining content will be included in the pull request body. Of course, GitHub Flavored Markdown is supported.

After completing the `liferaft.md` file, push all of your changes to your GitHub repository. Next, just run the Liferaft `throw` command from your application's directory:

	liferaft throw

This command will create a pull request against the Laravel GitHub repository. A Laravel maintainer can easily grab your application and run it in their own Homestead environment!

<a name="grabbing-liferaft-applications"></a>
## Grabbing Liferaft Applications

Intrested in contributing to Laravel? Liferaft makes it painless to install Liferaft applications and view them on your own [Homestead environment](/docs/4.1/4.2/homestead).

First, for convenience, clone the [laravel/laravel](https://github.com/laravel/laravel) into a `liferaft` directory on your machine:

	git clone https://github.com/laravel/laravel.git liferaft

Next, check out the `develop` branch so you will be able to install Liferaft applications that target both stable and upcoming Laravel releases:

	git checkout -b develop origin/develop

Next, you can run the Liferaft `grab` command from your repository directory. For example, if you want to install the Liferaft application associated with pull request #3000, you should run the following command:

	liferaft grab 3000

The `grab` command will create a new branch on your Liferaft directory, and pull in the changes for the specified pull request. Once the Liferaft application is installed, simply serve the directory through your [Homestead](/docs/4.1/4.2/homestead) virtual machine! Once you debug the issue, don't forget to send a pull request to the [laravel/framework](https://github.com/laravel/framework) repository with the proper fix!

Have an extra hour and want to solve a random issue? Just run `grab` without a pull request ID:

	liferaft grab

<a name="which-branch"></a>
## Which Branch?

> **Note:** This section primarly applies to those sending pull requests to the [laravel/framework](https://github.com/laravel/framework) repository, not Liferaft applications.

**All** bug fixes should be sent to the latest stable branch. Bug fixes should **never** be sent to the `master` branch unless they fix features that exist only in the upcoming release.

**Minor** features that are **fully backwards compatible** with the current Laravel release may be sent to the latest stable branch.

**Major** new features should always be sent to the `master` branch, which contains the upcoming Laravel release.

If you are unsure if your feature qualifies as a major or minor, please ask Taylor Otwell in the `#laravel-dev` IRC channel (Freenode).

<a name="security-vulnerabilities"></a>
## Security Vulnerabilities

If you discover a security vulnerability within Laravel, please send an e-mail to Taylor Otwell at <a href="mailto:taylorotwell@gmail.com">taylorotwell@gmail.com</a>. All security vulnerabilities will be promptly addressed.

<a name="coding-style"></a>
## Coding Style

Laravel follows the [PSR-0](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-0.md) and [PSR-1](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-1-basic-coding-standard.md) coding standards. In addition to these standards, the following coding standards should be followed:

- The class namespace declaration must be on the same line as `<?php`.
- A class' opening `{` must be on the same line as the class name.
- Functions and control structures must use Allman style braces.
- Indent with tabs, align with spaces.

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

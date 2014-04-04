# Artisan CLI

- [Introduction](#introduction)
- [Usage](#usage)

<a name="introduction"></a>
## Introduction

Artisan is the name of the command-line interface included with Laravel. It provides a number of helpful commands for your use while developing your application. It is driven by the powerful Symfony Console component.

<a name="usage"></a>
## Usage

To view a list of all available Artisan commands, you may use the `list` command:

#### Listing All Available Commands

	php artisan list

Every command also includes a "help" screen which displays and describes the command's available arguments and options. To view a help screen, simply precede the name of the command with `help`:

#### Viewing The Help Screen For A Command

	php artisan help migrate

You may specify the configuration environment that should be used while running a command using the `--env` switch:

#### Specifying The Configuration Environment

	php artisan migrate --env=local

You may also view the current version of your Laravel installation using the `--version` option:

#### Displaying Your Current Laravel Version

	php artisan --version

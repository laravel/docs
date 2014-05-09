# Artisan CLI

- [Introduction](#introduction)
- [Usage](#usage)

<a name="introduction"></a>
## Introduction

Artisan is the name of the command-line interface included with Laravel. It provides a number of helpful commands for your use while developing your application. It is driven by the powerful Symfony Console component.

<a name="usage"></a>
## Usage

#### Listing All Available Commands

To view a list of all available Artisan commands, you may use the `list` command:

	php artisan list

#### Viewing The Help Screen For A Command

Every command also includes a "help" screen which displays and describes the command's available arguments and options. To view a help screen, simply precede the name of the command with `help`:

	php artisan help migrate

#### Specifying The Configuration Environment

You may specify the configuration environment that should be used while running a command using the `--env` switch:

	php artisan migrate --env=local

#### Displaying Your Current Laravel Version

You may also view the current version of your Laravel installation using the `--version` option:

	php artisan --version

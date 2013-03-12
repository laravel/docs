# Artisan CLI

- [Introduction](#introduction)
- [Usage](#usage)

<a name="introduction"></a>
## Introduction

Artisan is the name of the command-line interface included with Laravel. It provides a number of helpful commands for your use while developing your application. It is driven by the powerful Symfony Console component.

<a name="usage"></a>
## Usage

To view a list of all available Artisan commands, you may use the `list` command:

**Listing All Available Commands**

	php artisan list

Every command also includes a "help" screen which displays and describes the command's available arguments and options. To view a help screen, simply precede the name of the command with `help`:

**Viewing The Help Screen For A Command**

	php artisan help migrate

You may specify the configuration environment that should be used while running a command using the `--env` switch:

**Specifying The Configuration Environment**

	php artisan migrate --env=local

You may also view the current version of your Laravel installation using the `--version` option:

**Displaying Your Current Laravel Version**

	php artisan --version

To create, and then register, a command-line Artisan command:

** Create the command in the app/commands folder, extending the Command class. **

	php artisan command:create MyNewCommand

You will now have a php skeleton file named MyNewCommand.php. Add your command code. The protected $name property determines how the command appears in Artisan's registered commands list.

	protected $name = 'mycommand:doit';

** Register the command in Artisan (so it appears in the command list, and can be executed):

Add your new class to the array map of loaded libraries in vendor/composer/autoload_classmap.php

	'MyNewCommand' => $baseDir . '/app/commands/MyNewCommand.php',

And then add an instance of the command object to the artisan start script, by editing app/start/artisan.php.

	Artisan::add(new MyNewCommand);

Your new command will now appear in the artisan list.

** Execute your custom command:

	php artisan mycommand:doit


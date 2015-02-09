# Filesystem / Cloud Storage

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
- [Custom Filesystems](#custom-filesystems)

<a name="introduction"></a>
## Introduction

Laravel provides a wonderful filesystem abstraction thanks to the [Flysystem](https://github.com/thephpleague/flysystem) PHP package by Frank de Jonge. The Laravel Flysystem integration provides simple to use drivers for working with local filesystems, Amazon S3, and Rackspace Cloud Storage. Even better, it's amazingly simple to switch between these storage options as the API remains the same for each system!

<a name="configuration"></a>
## Configuration

The filesystem configuration file is located at `config/filesystems.php`. Within this file you may configure all of your "disks". Each disk represents a particular storage driver and storage location. Example configurations for each supported driver is included in the configuration file. So, simply modify the configuration to reflect your storage preferences and credentials!

Before using the S3 or Rackspace drivers, you will need to install the appropriate package via Composer:

- Amazon S3: `league/flysystem-aws-s3-v2 ~1.0`
- Rackspace: `league/flysystem-rackspace ~1.0`

Of course, you may configure as many disks as you like, and may even have multiple disks that use the same driver.

When using the `local` driver, note that all file operations are relative to the `root` directory defined in your configuration file. By default, this value is set to the `storage/app` directory. Therefore, the following method would store a file in `storage/app/file.txt`:

	Storage::disk('local')->put('file.txt', 'Contents');

<a name="basic-usage"></a>
## Basic Usage

The `Storage` facade may be used to interact with any of your configured disks. Alternatively, you may type-hint the `Illuminate\Contracts\Filesystem\Factory` contract on any class that is resolved via the [IoC container](/docs/5.0/container).

#### Retrieving A Particular Disk

	$disk = Storage::disk('s3');

	$disk = Storage::disk('local');

#### Determining If A File Exists

	$exists = Storage::disk('s3')->exists('file.jpg');

#### Calling Methods On The Default Disk

	if (Storage::exists('file.jpg'))
	{
		//
	}

#### Retrieving A File's Contents

	$contents = Storage::get('file.jpg');

#### Setting A File's Contents

	Storage::put('file.jpg', $contents);

#### Prepend To A File

	Storage::prepend('file.log', 'Prepended Text');

#### Append To A File

	Storage::append('file.log', 'Appended Text');

#### Delete A File

	Storage::delete('file.jpg');

	Storage::delete(['file1.jpg', 'file2.jpg']);

#### Copy A File To A New Location

	Storage::copy('old/file1.jpg', 'new/file1.jpg');

#### Move A File To A New Location

	Storage::move('old/file1.jpg', 'new/file1.jpg');

#### Get File Size

	$size = Storage::size('file1.jpg');

#### Get The Last Modification Time (UNIX)

	$time = Storage::lastModified('file1.jpg');

#### Get All Files Within A Directory

	$files = Storage::files($directory);

	// Recursive...
	$files = Storage::allFiles($directory);

#### Get All Directories Within A Directory

	$directories = Storage::directories($directory);

	// Recursive...
	$directories = Storage::allDirectories($directory);

#### Create A Directory

	Storage::makeDirectory($directory);

#### Delete A Directory

	Storage::deleteDirectory($directory);

<a name="custom-filesystems"></a>
## Custom Filesystems
Laravel's Flysystem integration provides drivers for local filesystems, Amazon S3, and Rackspace Cloud Storage. Flysystem is not limited to these and has adapters for many additional storage systems. If you want to use one of these additional adapters in your Laravel application, you'll want to create a custom filesystem.

In order to set up your custom filesystem you'll need to create a Service Provider (for example, `DropboxFilesystemServiceProvider`). In its `boot` method, you'll want to inject an instance of the `Illuminate\Contracts\Filesystem\Factory` contract, and then call the `extend` method of the injected instance.

The first argument of the `extend` method is the name of the disk you will use, while the second argument is a closure that gets passed both the `$app` and `$config` variables.  

From this closure you must return an instance of `League\Flysystem\Filesystem`. Use the details provided with each filesystem to set this up.

> **Note:** The $config variable will already contain the proper values defined in `config/filesystems.php` for the provided disk.

Visit [Flysystem](https://github.com/thephpleague/flysystem#adapters) to view a list of available filesystems.

#### Dropbox Example

	<?php namespace App\Providers;

	use Illuminate\Contracts\Filesystem\Factory as FilesystemFactory;
	use League\Flysystem\Dropbox\DropboxAdapter;
	use League\Flysystem\Filesystem;
	use Dropbox\Client;

	class DropboxFilesystemServiceProvider {
		
		public function boot(FilesystemFactory $filesystem)
		{
			$filesystem->extend('dropbox', function($app, $config) 
			{
				$client = new Client($config['accessToken'], $config['clientIdentifier']);
				$adapter = new DropboxAdapter($client);
				
				return new Filesystem($adapter);
			});
		}

	}

# Filesystem / Cloud Storage

- [Introduction](#introduction)
- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
- [Custom Filesystems](#custom-filesystems)

<a name="introduction"></a>
## Introduction

Laravel provides a powerful filesystem abstraction thanks to the wonderful [Flysystem](https://github.com/thephpleague/flysystem) PHP package by Frank de Jonge. The Laravel Flysystem integration provides simple to use drivers for working with local filesystems, Amazon S3, and Rackspace Cloud Storage. Even better, it's amazingly simple to switch between these storage options as the API remains the same for each system.

<a name="configuration"></a>
## Configuration

The filesystem configuration file is located at `config/filesystems.php`. Within this file you may configure all of your "disks". Each disk represents a particular storage driver and storage location. Example configurations for each supported driver is included in the configuration file. So, simply modify the configuration to reflect your storage preferences and credentials!

Of course, you may configure as many disks as you like, and may even have multiple disks that use the same driver.

### The Local Driver

When using the `local` driver, note that all file operations are relative to the `root` directory defined in your configuration file. By default, this value is set to the `storage/app` directory. Therefore, the following method would store a file in `storage/app/file.txt`:

	Storage::disk('local')->put('file.txt', 'Contents');

### Other Driver Prerequisites

Before using the S3 or Rackspace drivers, you will need to install the appropriate package via Composer:

- Amazon S3: `league/flysystem-aws-s3-v2 ~1.0`
- Rackspace: `league/flysystem-rackspace ~1.0`

<a name="basic-usage"></a>
## Basic Usage

The `Storage` facade may be used to interact with any of your configured disks. For example, to store an avatar on the default "disk":

	<?php namespace App\Http\Controllers;

	use Storage;
	use Illuminate\Http\Request;
	use App\Http\Controllers\Controller;

	class UserController extends Controller
	{
		/**
		 * Update the avatar for the given user.
		 *
		 * @param  Request  $request
		 * @param  int  $id
		 * @return Response
		 */
		public function updateAvatar(Request $request, $id)
		{
			$user = User::findOrFail($id);

			Storage::put(
				'avatars/'.$user->id,
				file_get_contents($request->file('avatar')->getRealPath())
			);
		}
	}

#### Retrieving A Particular Disk

When using multiple disks, you may access a particular disk using the `disk` method on the `Storage` facade:

	$disk = Storage::disk('s3');

	$disk = Storage::disk('local');

#### Determining If A File Exists

	$exists = Storage::disk('s3')->exists('file.jpg');

#### Calling Methods On The Default Disk

If you call methods on the `Storage` facade without first calling the `disk` method, the method call will automatically be passed to the default disk:

	if (Storage::exists('file.jpg')) {
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

Laravel's Flysystem integration provides drivers for several "drivers" out of the box; however, Flysystem is not limited to these and has adapters for many other storage systems. You can create a custom driver if you want to use one of these additional adapters in your Laravel application.

In order to set up the custom filesystem you will need to create a [service provider](/docs/{{version}}/providers) such as `DropboxServiceProvider`. In the provider's `boot` method, you may use the `Storage` facade's `extend` method to define the custom driver:

	<?php namespace App\Providers;

	use Storage;
	use League\Flysystem\Filesystem;
	use Dropbox\Client as DropboxClient;
	use Illuminate\Support\ServiceProvider;
	use League\Flysystem\Dropbox\DropboxAdapter;

	class DropboxServiceProvider extends ServiceProvider
	{
		/**
		 * Perform post-registration booting of services.
		 *
		 * @return void
		 */
		public function boot()
		{
			Storage::extend('dropbox', function($app, $config) {
				$client = new DropboxClient(
					$config['accessToken'], $config['clientIdentifier']
				);

				return new Filesystem(new DropboxAdapter($client));
			});
		}

		/**
		 * Register bindings in the container.
		 *
		 * @return void
		 */
		public function register()
		{
			//
		}
	}

The first argument of the `extend` method is the name of the driver and the second is a Closure that receives the `$app` and `$config` variables. The resolver Closure must return an instance of `League\Flysystem\Filesystem`. The `$config` variable contains the values defined in `config/filesystems.php` for the specified disk.

Once you have created the service provider to register the extension, you may use the `dropbox` driver in your `config/filesystem.php` configuration file.

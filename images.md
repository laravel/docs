# Image Manipulation

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
- [Reading Images](#reading-images)
    - [Uploaded Files](#uploaded-files)
    - [Storage Files](#storage-files)
    - [Other Sources](#other-sources)
- [Manipulating Images](#manipulating-images)
    - [Resizing Images](#resizing-images)
    - [Other Transformations](#other-transformations)
- [Encoding Images](#encoding-images)
- [Storing Images](#storing-images)
- [Inspecting Images](#inspecting-images)
- [Image Drivers](#image-drivers)
    - [Custom Image Drivers](#custom-image-drivers)
    - [Custom Transformations](#custom-transformations)

<a name="introduction"></a>
## Introduction

Laravel provides a fluent image manipulation API that allows you to resize, crop, encode, and store images using the same expressive conventions found throughout the framework. Laravel's image features are powered by [Intervention Image](https://image.intervention.io/) and support the GD and Imagick PHP extensions.

The image API is useful when working with uploaded files, files stored on Laravel [filesystem disks](/docs/{{version}}/filesystem), local files, remote URLs, or raw image bytes:

```php
use Illuminate\Support\Facades\Image;

$path = Image::fromStorage('avatars/photo.jpg', 'public')
    ->cover(400, 400)
    ->toWebp()
    ->quality(80)
    ->storePublicly('avatars', 'public');
```

> [!WARNING]
> Image manipulation can be CPU and memory-intensive. Consider performing large image processing workloads on a [queued job](/docs/{{version}}/queues) instead of during the HTTP request that receives the upload.

<a name="installation"></a>
## Installation

Before using Laravel's image manipulation features, install the Intervention Image package via Composer:

```shell
composer require intervention/image:^4.0
```

You should also ensure your PHP installation has either the GD or Imagick extension installed, depending on which driver your application will use.

<a name="configuration"></a>
### Configuration

Laravel's image configuration file is located at `config/image.php`. If your application does not have an `image` configuration file, you may publish it using the `config:publish` Artisan command:

```shell
php artisan config:publish image
```

The image configuration file allows you to specify your application's default image driver. You may also specify the default driver using the `IMAGE_DRIVER` environment variable. The supported drivers are `gd` and `imagick`:

```ini
IMAGE_DRIVER=imagick
```

<a name="reading-images"></a>
## Reading Images

The `Image` facade provides several methods for reading images from common sources. Image contents are loaded lazily, so the source is typically not read until the image is processed or its bytes are requested.

<a name="uploaded-files"></a>
### Uploaded Files

You may retrieve an uploaded image from an incoming request using the `image` method. This method returns an `Illuminate\Image\Image` instance for the uploaded file, or `null` if the file is not present:

```php
use Illuminate\Http\Request;

Route::post('/avatar', function (Request $request) {
    $request->validate(['avatar' => ['required', 'image']]);

    $path = $request->image('avatar')
        ->cover(400, 400)
        ->toWebp()
        ->storePublicly('avatars', 'public');

    // ...
});
```

Alternatively, you may create an image instance from an `Illuminate\Http\UploadedFile` instance using the `fromUpload` method:

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromUpload($request->file('avatar'));
```

When an image is created from an uploaded file, you may retrieve the underlying uploaded file using the `file` method:

```php
$file = $image->file();
```

<a name="storage-files"></a>
### Storage Files

You may create an image instance from a file stored on one of your application's [filesystem disks](/docs/{{version}}/filesystem) using the `fromStorage` method. The first argument is the path to the file, while the second argument is the disk name:

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromStorage('avatars/photo.jpg', disk: 'public');
```

You may also create image instances directly from a filesystem disk instance using the `image` method:

```php
use Illuminate\Support\Facades\Storage;

$image = Storage::disk('public')->image('avatars/photo.jpg');
```

<a name="other-sources"></a>
### Other Sources

The `Image` facade also includes methods for creating image instances from raw bytes, local file paths, remote URLs, and Base64 encoded strings:

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromBytes($contents);
$image = Image::fromBase64($base64);
$image = Image::fromPath(storage_path('app/avatars/photo.jpg'));
$image = Image::fromUrl('https://example.com/photo.jpg');
```

<a name="manipulating-images"></a>
## Manipulating Images

Image instances are immutable. Each manipulation method returns a new image instance with the transformation appended to its processing pipeline, allowing methods to be chained fluently:

```php
$image = $request->image('avatar')
    ->orient()
    ->cover(400, 400)
    ->sharpen(10);
```

Transformations are processed in the order they are added to the image pipeline and the image is only encoded once at the end.

<a name="resizing-images"></a>
### Resizing Images

The `resize` method resizes an image to the given dimensions. You may provide both a width and height, or provide only one dimension using named arguments:

```php
$image = $image->resize(800, 600);
$image = $image->resize(width: 800);
$image = $image->resize(height: 600);
```

The `scale` method proportionally scales an image down so that it fits within the given dimensions. This method will never increase the size of an image:

```php
$image = $image->scale(800, 600);
$image = $image->scale(width: 800);
$image = $image->scale(height: 600);
```

The `cover` method resizes and crops an image to completely cover the given dimensions:

```php
$image = $image->cover(400, 400);
```

The `contain` method resizes an image to fit within the given dimensions while preserving the entire image. If necessary, empty space will be filled using the optional background color:

```php
$image = $image->contain(400, 400);
$image = $image->contain(400, 400, '#ffffff');
```

You may crop an image using the `crop` method. The first two arguments are the desired width and height, and the optional third and fourth arguments specify the crop's `x` and `y` coordinates:

```php
$image = $image->crop(300, 200);
$image = $image->crop(300, 200, x: 50, y: 25);
```

<a name="other-transformations"></a>
### Other Transformations

Laravel also provides a variety of additional image transformation methods:

```php
$image = $image->orient();
$image = $image->rotate(90);
$image = $image->rotate(90, '#ffffff');
$image = $image->blur(5);
$image = $image->grayscale();
$image = $image->sharpen(10);
$image = $image->flipVertically();
$image = $image->flipHorizontally();
```

The `orient` method rotates the image according to its EXIF orientation data. The `rotate` method rotates the image clockwise by the given angle and accepts an optional background color. The `blur` and `sharpen` methods accept values between `0` and `100`.

<a name="conditional-transformations"></a>
#### Conditional Transformations

Image instances support Laravel's `Conditionable` trait, allowing you to conditionally apply transformations using the `when` and `unless` methods:

```php
$image = $request->image('avatar')
    ->when($request->boolean('crop'), fn ($image) => $image->cover(400, 400))
    ->unless($request->boolean('preserve_format'), fn ($image) => $image->toWebp());
```

<a name="encoding-images"></a>
## Encoding Images

By default, processed images are encoded using their original format. However, you may convert the image to another supported format before retrieving or storing it:

```php
$image = $image->toWebp();
$image = $image->toJpg();
$image = $image->toJpeg();
```

You may use the `quality` method to set the output quality. The quality will be clamped between `1` and `100`:

```php
$image = $image->toWebp()->quality(80);
```

The `optimize` method is a convenient shortcut for converting the image to a given format and setting its quality. By default, images are optimized as WebP images with a quality of `70`:

```php
$image = $image->optimize();

$image = $image->optimize(format: 'jpg', quality: 85);
```

You may retrieve the processed image contents as a string of bytes, base64 encoded string, or data URI:

```php
$bytes = $image->toBytes();
$base64 = $image->toBase64();
$dataUri = $image->toDataUri();
```

An image instance may also be cast to a string to retrieve its processed bytes:

```php
$bytes = (string) $image;
```

<a name="storing-images"></a>
## Storing Images

The `store` method stores the processed image on one of your application's filesystem disks. Like uploaded files, Laravel will generate a unique filename and return the stored path. The second argument may be used to specify the disk:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->store(path: 'avatars');

$path = $request->image('avatar')
    ->cover(400, 400)
    ->store(path: 'avatars', disk: 's3');
```

You may use the `storeAs` method to specify the stored filename:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->storeAs(path: 'avatars', name: 'avatar.jpg', disk: 'public');
```

The `storePublicly` and `storePubliclyAs` methods store the image with `public` visibility:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->storePublicly(path: 'avatars', disk: 'public');

$path = $request->image('avatar')
    ->cover(400, 400)
    ->storePubliclyAs(path: 'avatars', name: 'avatar.webp', disk: 'public');
```

If the image could not be stored, the storage methods return `false`.

<a name="inspecting-images"></a>
## Inspecting Images

You may retrieve the image's MIME type, extension, dimensions, width, and height using the following methods:

```php
$mimeType = $image->mimeType();
$extension = $image->extension();

[$width, $height] = $image->dimensions();
$width = $image->width();
$height = $image->height();
```

These methods operate on the processed image. For example, calling `width` after `cover(400, 400)` will return `400`.

<a name="image-drivers"></a>
## Image Drivers

<a name="custom-image-drivers"></a>
### Custom Image Drivers

Laravel's image manager extends Laravel's base `Illuminate\Support\Manager` class. This means you may register custom image drivers using the `extend` method available on the image manager and `Image` facade.

Custom image drivers should implement the `Illuminate\Contracts\Image\Driver` interface. The `process` method receives the original image contents and the ordered `Illuminate\Image\ImagePipeline` that should be applied to the image, and should return the processed image bytes:

```php
<?php

namespace App\Images;

use Illuminate\Contracts\Image\Driver;
use Illuminate\Image\ImagePipeline;

class VipsDriver implements Driver
{
    /**
     * Process the given image contents with the specified pipeline.
     */
    public function process(string $contents, ImagePipeline $pipeline): string
    {
        // Apply the pipeline's transformations and output options...

        return $contents;
    }

    /**
     * Register a transformation handler.
     */
    public function transformUsing(string $transformation, callable $callback): static
    {
        // Store the handler so it may be applied while processing the pipeline...

        return $this;
    }
}
```

> [!NOTE]
> To better understand how to implement a custom image driver, you may review the framework's built-in `Illuminate\Image\Drivers\InterventionDriver` class.

Once you have implemented your custom driver, you may register it using the `Image` facade's `extend` method. Typically, this should be done in the `boot` method of a service provider:

```php
use App\Images\VipsDriver;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Image;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Image::extend('vips', function (Application $app) {
        return new VipsDriver;
    });
}
```

After registering the driver, you may use it for a specific image using the `using` method:

```php
$image = $request->image('avatar')
    ->using('vips')
    ->cover(400, 400);
```

You may also configure a custom driver as your application's default image driver using the `default` option in your application's `config/image.php` configuration file or the `IMAGE_DRIVER` environment variable:

```ini
IMAGE_DRIVER=vips
```

<a name="custom-transformations"></a>
### Custom Transformations

Applications and packages may define custom transformations by creating a class that implements the `Illuminate\Contracts\Image\Transformation` contract. Custom transformations can then be added to an image pipeline using the `transform` method:

```php
<?php

namespace App\Images\Transformations;

use Illuminate\Contracts\Image\Transformation;

class Pixelate implements Transformation
{
    public function __construct(
        public readonly int $size,
    ) {
        //
    }
}
```

Next, register a handler for the transformation and driver using the `Image` facade's `transformUsing` method. Typically, this should be done in the `boot` method of a service provider:

```php
use App\Images\Transformations\Pixelate;
use Illuminate\Support\Facades\Image;
use Intervention\Image\Interfaces\ImageInterface;

Image::transformUsing('gd', Pixelate::class, function (ImageInterface $image, Pixelate $transformation) {
    return $image->pixelate($transformation->size);
});
```

Once the transformation handler has been registered, you may apply the transformation to an image:

```php
use App\Images\Transformations\Pixelate;

$image = $request->image('avatar')
    ->transform(new Pixelate(12))
    ->store('avatars');
```

---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Обробка зображень

- [Вступ](#introduction)
- [Встановлення](#installation)
    - [Конфігурація](#configuration)
- [Читання зображень](#reading-images)
    - [Завантажені файли](#uploaded-files)
    - [Файли у сховищі](#storage-files)
    - [Інші джерела](#other-sources)
- [Обробка зображень](#manipulating-images)
    - [Зміна розміру зображень](#resizing-images)
    - [Інші перетворення](#other-transformations)
- [Кодування зображень](#encoding-images)
- [Збереження зображень](#storing-images)
- [Огляд зображень](#inspecting-images)
- [Драйвери зображень](#image-drivers)
    - [Власні драйвери зображень](#custom-image-drivers)
    - [Власні перетворення](#custom-transformations)

<a name="introduction"></a>
## Вступ

Laravel надає плавний API для обробки зображень, який дозволяє змінювати розмір, обрізати, кодувати й зберігати зображення за тими самими виразними домовленостями, що діють в усьому фреймворку. Можливості роботи із зображеннями в Laravel побудовані на [Intervention Image](https://image.intervention.io/) і підтримують PHP-розширення GD та Imagick.

API зображень стане в пригоді під час роботи із завантаженими файлами, файлами на [дисках файлової системи](/docs/{{version}}/filesystem) Laravel, локальними файлами, віддаленими URL чи сирими байтами зображення:

```php
use Illuminate\Support\Facades\Image;

$path = Image::fromStorage('avatars/photo.jpg', 'public')
    ->cover(400, 400)
    ->toWebp()
    ->quality(80)
    ->storePublicly('avatars', 'public');
```

> [!WARNING]
> Обробка зображень може бути вимогливою до процесора й пам'яті. Розгляньте можливість виконувати великі обсяги обробки зображень у [завданні в черзі](/docs/{{version}}/queues), а не під час HTTP-запиту, який приймає завантаження.

<a name="installation"></a>
## Встановлення

Перш ніж користуватися можливостями обробки зображень у Laravel, встановіть пакет Intervention Image через Composer:

```shell
composer require intervention/image:^4.0
```

Також переконайтеся, що у вашій інсталяції PHP встановлено розширення GD або Imagick - залежно від того, який драйвер використовуватиме ваш застосунок.

<a name="configuration"></a>
### Конфігурація

Файл конфігурації зображень Laravel лежить у `config/images.php`. Якщо у вашому застосунку немає файлу конфігурації `images`, опублікуйте його командою Artisan `config:publish`:

```shell
php artisan config:publish images
```

Файл конфігурації зображень дозволяє вказати драйвер зображень за замовчуванням для вашого застосунку. Ви також можете вказати драйвер за замовчуванням через змінну середовища `IMAGE_DRIVER`. Підтримувані драйвери - `gd` та `imagick`:

```ini
IMAGE_DRIVER=imagick
```

<a name="reading-images"></a>
## Читання зображень

Фасад `Image` надає кілька методів для читання зображень із поширених джерел. Вміст зображень завантажується ліниво, тож джерело зазвичай не читається, доки зображення не оброблено або доки не запитано його байти.

<a name="uploaded-files"></a>
### Завантажені файли

Ви можете дістати завантажене зображення з вхідного запиту методом `image`. Цей метод повертає екземпляр `Illuminate\Image\Image` для завантаженого файлу або `null`, якщо файлу немає:

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

Як варіант, ви можете створити екземпляр зображення з екземпляра `Illuminate\Http\UploadedFile` методом `fromUpload`:

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromUpload($request->file('avatar'));
```

Коли зображення створено із завантаженого файлу, ви можете дістати цей файл методом `file`:

```php
$file = $image->file();
```

<a name="storage-files"></a>
### Файли у сховищі

Ви можете створити екземпляр зображення з файлу, що зберігається на одному з [дисків файлової системи](/docs/{{version}}/filesystem) вашого застосунку, методом `fromStorage`. Перший аргумент - шлях до файлу, другий - назва диска:

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromStorage('avatars/photo.jpg', disk: 'public');
```

Ви також можете створювати екземпляри зображень безпосередньо з екземпляра диска методом `image`:

```php
use Illuminate\Support\Facades\Storage;

$image = Storage::disk('public')->image('avatars/photo.jpg');
```

<a name="other-sources"></a>
### Інші джерела

Фасад `Image` також містить методи для створення екземплярів зображень із сирих байтів, локальних шляхів, віддалених URL і рядків у Base64:

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromBytes($contents);
$image = Image::fromBase64($base64);
$image = Image::fromPath(storage_path('app/avatars/photo.jpg'));
$image = Image::fromUrl('https://example.com/photo.jpg');
```

<a name="manipulating-images"></a>
## Обробка зображень

Екземпляри зображень незмінні. Кожен метод обробки повертає новий екземпляр зображення з доданим до його конвеєра перетворенням, тож методи можна плавно поєднувати ланцюжком:

```php
$image = $request->image('avatar')
    ->orient()
    ->cover(400, 400)
    ->sharpen(10);
```

Перетворення обробляються в порядку, у якому їх додано до конвеєра зображення, а саме зображення кодується лише один раз, у кінці.

<a name="resizing-images"></a>
### Зміна розміру зображень

Метод `resize` змінює розмір зображення до заданих величин. Ви можете передати і ширину, і висоту або лише одну величину через іменовані аргументи:

```php
$image = $image->resize(800, 600);
$image = $image->resize(width: 800);
$image = $image->resize(height: 600);
```

Метод `scale` пропорційно зменшує зображення так, щоб воно вмістилося в задані величини. Цей метод ніколи не збільшує зображення:

```php
$image = $image->scale(800, 600);
$image = $image->scale(width: 800);
$image = $image->scale(height: 600);
```

Метод `cover` змінює розмір і обрізає зображення так, щоб воно повністю вкривало задані величини:

```php
$image = $image->cover(400, 400);
```

Метод `contain` змінює розмір зображення так, щоб воно вмістилося в задані величини, зберігши все зображення. За потреби порожній простір буде заповнено необов'язковим кольором тла:

```php
$image = $image->contain(400, 400);
$image = $image->contain(400, 400, '#ffffff');
```

Обрізати зображення можна методом `crop`. Перші два аргументи - потрібні ширина й висота, а необов'язкові третій і четвертий задають координати `x` та `y` обрізання:

```php
$image = $image->crop(300, 200);
$image = $image->crop(300, 200, x: 50, y: 25);
```

<a name="other-transformations"></a>
### Інші перетворення

Laravel також надає низку додаткових методів перетворення зображень:

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

Метод `orient` повертає зображення відповідно до даних орієнтації EXIF. Метод `rotate` повертає зображення за годинниковою стрілкою на заданий кут і приймає необов'язковий колір тла. Методи `blur` і `sharpen` приймають значення від `0` до `100`.

<a name="conditional-transformations"></a>
#### Умовні перетворення

Екземпляри зображень підтримують трейт `Conditionable` Laravel, тож ви можете застосовувати перетворення умовно, методами `when` та `unless`:

```php
$image = $request->image('avatar')
    ->when($request->boolean('crop'), fn ($image) => $image->cover(400, 400))
    ->unless($request->boolean('preserve_format'), fn ($image) => $image->toWebp());
```

<a name="encoding-images"></a>
## Кодування зображень

За замовчуванням оброблені зображення кодуються у своєму оригінальному форматі. Проте ви можете конвертувати зображення в інший підтримуваний формат перед отриманням чи збереженням:

```php
$image = $image->toWebp();
$image = $image->toJpg();
$image = $image->toJpeg();
$image = $image->toPng();
$image = $image->toGif();
$image = $image->toAvif();
$image = $image->toBmp();
```

Метод `quality` дозволяє задати якість на виході. Якість буде обмежено діапазоном від `1` до `100`:

```php
$image = $image->toWebp()->quality(80);
```

Метод `optimize` - зручне скорочення для конвертації зображення в заданий формат із заданням якості. За замовчуванням зображення оптимізуються як WebP з якістю `70`:

```php
$image = $image->optimize();

$image = $image->optimize(format: 'jpg', quality: 85);
```

Ви можете отримати вміст обробленого зображення як рядок байтів, рядок у Base64 чи data URI:

```php
$bytes = $image->toBytes();
$base64 = $image->toBase64();
$dataUri = $image->toDataUri();
```

Екземпляр зображення можна також привести до рядка, щоб отримати його оброблені байти:

```php
$bytes = (string) $image;
```

<a name="storing-images"></a>
## Збереження зображень

Метод `store` зберігає оброблене зображення на одному з дисків файлової системи вашого застосунку. Як і для завантажених файлів, Laravel згенерує унікальне ім'я файлу й поверне шлях збереження. Другим аргументом можна вказати диск:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->store(path: 'avatars');

$path = $request->image('avatar')
    ->cover(400, 400)
    ->store(path: 'avatars', disk: 's3');
```

Метод `storeAs` дозволяє вказати ім'я збереженого файлу:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->storeAs(path: 'avatars', name: 'avatar.jpg', disk: 'public');
```

Методи `storePublicly` та `storePubliclyAs` зберігають зображення з видимістю `public`:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->storePublicly(path: 'avatars', disk: 'public');

$path = $request->image('avatar')
    ->cover(400, 400)
    ->storePubliclyAs(path: 'avatars', name: 'avatar.webp', disk: 'public');
```

Якщо зображення не вдалося зберегти, методи збереження повертають `false`.

<a name="inspecting-images"></a>
## Огляд зображень

Отримати MIME-тип, розширення, розміри, ширину й висоту зображення можна такими методами:

```php
$mimeType = $image->mimeType();
$extension = $image->extension();

[$width, $height] = $image->dimensions();
$width = $image->width();
$height = $image->height();
```

Ці методи працюють з обробленим зображенням. Наприклад, виклик `width` після `cover(400, 400)` поверне `400`.

<a name="image-drivers"></a>
## Драйвери зображень

<a name="custom-image-drivers"></a>
### Власні драйвери зображень

Менеджер зображень Laravel розширює базовий клас `Illuminate\Support\Manager`. Це означає, що ви можете реєструвати власні драйвери зображень методом `extend`, доступним у менеджері зображень і фасаді `Image`.

Власні драйвери зображень мають реалізовувати інтерфейс `Illuminate\Contracts\Image\Driver`. Метод `process` отримує оригінальний вміст зображення та впорядкований `Illuminate\Image\ImagePipeline`, який слід застосувати до зображення, і має повернути оброблені байти:

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
> Щоб краще зрозуміти, як реалізувати власний драйвер зображень, перегляньте вбудований клас фреймворку `Illuminate\Image\Drivers\InterventionDriver`.

Щойно ви реалізували власний драйвер, зареєструйте його методом `extend` фасаду `Image`. Зазвичай це роблять у методі `boot` сервіс-провайдера:

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

Зареєструвавши драйвер, ви можете скористатися ним для конкретного зображення методом `using`:

```php
$image = $request->image('avatar')
    ->using('vips')
    ->cover(400, 400);
```

Ви також можете зробити власний драйвер драйвером зображень за замовчуванням для вашого застосунку через опцію `default` у файлі `config/images.php` або змінну середовища `IMAGE_DRIVER`:

```ini
IMAGE_DRIVER=vips
```

<a name="custom-transformations"></a>
### Власні перетворення

Застосунки й пакети можуть описувати власні перетворення, створивши клас, який реалізує контракт `Illuminate\Contracts\Image\Transformation`. Далі власні перетворення можна додавати до конвеєра зображення методом `transform`:

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

Далі зареєструйте обробник для перетворення й драйвера методом `transformUsing` фасаду `Image`. Зазвичай це роблять у методі `boot` сервіс-провайдера:

```php
use App\Images\Transformations\Pixelate;
use Illuminate\Support\Facades\Image;
use Intervention\Image\Interfaces\ImageInterface;

Image::transformUsing('gd', Pixelate::class, function (ImageInterface $image, Pixelate $transformation) {
    return $image->pixelate($transformation->size);
});
```

Щойно обробник перетворення зареєстровано, ви можете застосувати перетворення до зображення:

```php
use App\Images\Transformations\Pixelate;

$image = $request->image('avatar')
    ->transform(new Pixelate(12))
    ->store('avatars');
```

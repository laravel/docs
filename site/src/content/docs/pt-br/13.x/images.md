---
title: "Manipulação de Imagens"
---

- [Introdução](#introduction)
- [Instalação](#installation)
    - [Configuração](#configuration)
- [Lendo Imagens](#reading-images)
    - [Arquivos Enviados](#uploaded-files)
    - [Arquivos de Armazenamento](#storage-files)
    - [Outras Fontes](#other-sources)
- [Manipulando Imagens](#manipulating-images)
    - [Redimensionando Imagens](#resizing-images)
    - [Outras Transformações](#other-transformations)
- [Codificando Imagens](#encoding-images)
- [Armazenando Imagens](#storing-images)
- [Inspecionando Imagens](#inspecting-images)
- [Drivers de Imagem](#image-drivers)
    - [Drivers de Imagem Personalizados](#custom-image-drivers)
    - [Transformações Personalizadas](#custom-transformations)

<a id="introduction"></a>
## Introdução

O Laravel fornece uma API fluente de manipulação de imagens que permite redimensionar, recortar, codificar e armazenar imagens usando as mesmas convenções expressivas encontradas em todo o framework. Os recursos de imagem do Laravel são alimentados pelo [Intervention Image](https://image.intervention.io/) e suportam as extensões PHP GD e Imagick.

A API de imagem é útil ao trabalhar com arquivos enviados, arquivos armazenados em [discos do sistema de arquivos](../filesystem/) do Laravel, arquivos locais, URLs remotas ou bytes brutos de imagem:

```php
use Illuminate\Support\Facades\Image;

$path = Image::fromStorage('avatars/photo.jpg', 'public')
    ->cover(400, 400)
    ->toWebp()
    ->quality(80)
    ->storePublicly('avatars', 'public');
```

> **Aviso:**
> A manipulação de imagens pode consumir muita CPU e memória. Considere executar o processamento de imagens grandes em um [job na fila](../queues/) em vez de durante a requisição HTTP que recebe o upload.

<a id="installation"></a>
## Instalação

Antes de usar os recursos de manipulação de imagens do Laravel, instale o pacote Intervention Image via Composer:

```shell
composer require intervention/image:^4.0
```

Você também deve garantir que sua instalação do PHP tenha a extensão GD ou Imagick instalada, dependendo de qual driver sua aplicação vai usar.

<a id="configuration"></a>
### Configuração

O arquivo de configuração de imagens do Laravel está localizado em `config/images.php`. Se sua aplicação não possuir um arquivo de configuração `images`, você pode publicá-lo usando o comando Artisan `config:publish`:

```shell
php artisan config:publish images
```

O arquivo de configuração de imagens permite especificar o driver de imagem padrão da sua aplicação. Você também pode especificar o driver padrão usando a variável de ambiente `IMAGE_DRIVER`. Os drivers suportados são `gd` e `imagick`:

```ini
IMAGE_DRIVER=imagick
```

<a id="reading-images"></a>
## Lendo Imagens

A facade `Image` fornece vários métodos para ler imagens de fontes comuns. O conteúdo das imagens é carregado de forma preguiçosa (lazy), então a fonte normalmente não é lida até que a imagem seja processada ou seus bytes sejam solicitados.

<a id="uploaded-files"></a>
### Arquivos Enviados

Você pode recuperar uma imagem enviada de uma requisição recebida usando o método `image`. Este método retorna uma instância de `Illuminate\Image\Image` para o arquivo enviado, ou `null` se o arquivo não estiver presente:

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

Alternativamente, você pode criar uma instância de imagem a partir de uma instância de `Illuminate\Http\UploadedFile` usando o método `fromUpload`:

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromUpload($request->file('avatar'));
```

Quando uma imagem é criada a partir de um arquivo enviado, você pode recuperar o arquivo enviado subjacente usando o método `file`:

```php
$file = $image->file();
```

<a id="storage-files"></a>
### Arquivos de Armazenamento

Você pode criar uma instância de imagem a partir de um arquivo armazenado em um dos [discos do sistema de arquivos](../filesystem/) da sua aplicação usando o método `fromStorage`. O primeiro argumento é o caminho do arquivo, enquanto o segundo argumento é o nome do disco:

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromStorage('avatars/photo.jpg', disk: 'public');
```

Você também pode criar instâncias de imagem diretamente a partir de uma instância de disco do sistema de arquivos usando o método `image`:

```php
use Illuminate\Support\Facades\Storage;

$image = Storage::disk('public')->image('avatars/photo.jpg');
```

<a id="other-sources"></a>
### Outras Fontes

A facade `Image` também inclui métodos para criar instâncias de imagem a partir de bytes brutos, caminhos de arquivos locais, URLs remotas e strings codificadas em Base64:

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromBytes($contents);
$image = Image::fromBase64($base64);
$image = Image::fromPath(storage_path('app/avatars/photo.jpg'));
$image = Image::fromUrl('https://example.com/photo.jpg');
```

<a id="manipulating-images"></a>
## Manipulando Imagens

As instâncias de imagem são imutáveis. Cada método de manipulação retorna uma nova instância de imagem com a transformação adicionada ao seu pipeline de processamento, permitindo encadear os métodos de forma fluente:

```php
$image = $request->image('avatar')
    ->orient()
    ->cover(400, 400)
    ->sharpen(10);
```

As transformações são processadas na ordem em que são adicionadas ao pipeline da imagem, e a imagem só é codificada uma vez, no final.

<a id="resizing-images"></a>
### Redimensionando Imagens

O método `resize` redimensiona uma imagem para as dimensões fornecidas. Você pode informar largura e altura, ou informar apenas uma dimensão usando argumentos nomeados:

```php
$image = $image->resize(800, 600);
$image = $image->resize(width: 800);
$image = $image->resize(height: 600);
```

O método `scale` reduz proporcionalmente uma imagem para que ela caiba nas dimensões fornecidas. Este método nunca aumenta o tamanho de uma imagem:

```php
$image = $image->scale(800, 600);
$image = $image->scale(width: 800);
$image = $image->scale(height: 600);
```

O método `cover` redimensiona e recorta uma imagem para cobrir completamente as dimensões fornecidas:

```php
$image = $image->cover(400, 400);
```

O método `contain` redimensiona uma imagem para caber nas dimensões fornecidas preservando a imagem inteira. Se necessário, o espaço vazio será preenchido usando a cor de fundo opcional:

```php
$image = $image->contain(400, 400);
$image = $image->contain(400, 400, '#ffffff');
$image = $image->contain(400, 400, 'dominant');
```

Você pode especificar `dominant` como cor de fundo para preencher o espaço vazio usando a cor dominante da imagem.

Você pode recortar uma imagem usando o método `crop`. Os dois primeiros argumentos são a largura e a altura desejadas, e o terceiro e quarto argumentos opcionais especificam as coordenadas `x` e `y` do recorte:

```php
$image = $image->crop(300, 200);
$image = $image->crop(300, 200, x: 50, y: 25);
```

<a id="other-transformations"></a>
### Outras Transformações

O Laravel também fornece uma variedade de métodos adicionais de transformação de imagem:

```php
$image = $image->orient();
$image = $image->rotate(90);
$image = $image->rotate(90, '#ffffff');
$image = $image->rotate(90, 'dominant');
$image = $image->blur(5);
$image = $image->grayscale();
$image = $image->sharpen(10);
$image = $image->flipVertically();
$image = $image->flipHorizontally();
```

O método `orient` rotaciona a imagem de acordo com seus dados de orientação EXIF. O método `rotate` rotaciona a imagem no sentido horário pelo ângulo fornecido e aceita uma cor de fundo opcional. Os métodos `blur` e `sharpen` aceitam valores entre `0` e `100`.

<a id="conditional-transformations"></a>
#### Transformações Condicionais

As instâncias de imagem suportam a trait `Conditionable` do Laravel, permitindo aplicar transformações condicionalmente usando os métodos `when` e `unless`:

```php
$image = $request->image('avatar')
    ->when($request->boolean('crop'), fn ($image) => $image->cover(400, 400))
    ->unless($request->boolean('preserve_format'), fn ($image) => $image->toWebp());
```

<a id="encoding-images"></a>
## Codificando Imagens

Por padrão, as imagens processadas são codificadas usando seu formato original. No entanto, você pode converter a imagem para outro formato suportado antes de recuperá-la ou armazená-la:

```php
$image = $image->toWebp();
$image = $image->toJpg();
$image = $image->toJpeg();
$image = $image->toPng();
$image = $image->toGif();
$image = $image->toAvif();
$image = $image->toBmp();
```

Você pode usar o método `quality` para definir a qualidade de saída. A qualidade será limitada entre `1` e `100`:

```php
$image = $image->toWebp()->quality(80);
```

O método `optimize` é um atalho prático para converter a imagem para um determinado formato e definir sua qualidade. Por padrão, as imagens são otimizadas como imagens WebP com qualidade `70`:

```php
$image = $image->optimize();

$image = $image->optimize(format: 'jpg', quality: 85);
```

Você pode recuperar o conteúdo da imagem processada como uma string de bytes, uma string codificada em base64 ou um data URI:

```php
$bytes = $image->toBytes();
$base64 = $image->toBase64();
$dataUri = $image->toDataUri();
```

Uma instância de imagem também pode ser convertida para string para obter um data URI:

```php
$dataUri = (string) $image;
```

<a id="storing-images"></a>
## Armazenando Imagens

O método `store` armazena a imagem processada em um dos discos do sistema de arquivos da sua aplicação. Assim como nos arquivos enviados, o Laravel gerará um nome de arquivo único e retornará o caminho armazenado. O segundo argumento pode ser usado para especificar o disco:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->store(path: 'avatars');

$path = $request->image('avatar')
    ->cover(400, 400)
    ->store(path: 'avatars', disk: 's3');
```

Você pode usar o método `storeAs` para especificar o nome do arquivo armazenado:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->storeAs(path: 'avatars', name: 'avatar.jpg', disk: 'public');
```

Os métodos `storePublicly` e `storePubliclyAs` armazenam a imagem com visibilidade `public`:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->storePublicly(path: 'avatars', disk: 'public');

$path = $request->image('avatar')
    ->cover(400, 400)
    ->storePubliclyAs(path: 'avatars', name: 'avatar.webp', disk: 'public');
```

Se a imagem não puder ser armazenada, os métodos de armazenamento retornam `false`.

<a id="inspecting-images"></a>
## Inspecionando Imagens

Você pode recuperar o tipo MIME, a extensão, as dimensões, a largura, a altura e a cor dominante da imagem usando os seguintes métodos:

```php
$mimeType = $image->mimeType();
$extension = $image->extension();

[$width, $height] = $image->dimensions();
$width = $image->width();
$height = $image->height();

$dominantColor = $image->dominantColor();
```

Esses métodos operam sobre a imagem processada. Por exemplo, chamar `width` após `cover(400, 400)` retornará `400`.

<a id="image-drivers"></a>
## Drivers de Imagem

<a id="custom-image-drivers"></a>
### Drivers de Imagem Personalizados

O gerenciador de imagens do Laravel estende a classe base `Illuminate\Support\Manager` do Laravel. Isso significa que você pode registrar drivers de imagem personalizados usando o método `extend` disponível no gerenciador de imagens e na facade `Image`.

Drivers de imagem personalizados devem implementar a interface `Illuminate\Contracts\Image\Driver`. O método `process` recebe o conteúdo original da imagem e o `Illuminate\Image\ImagePipeline` ordenado que deve ser aplicado à imagem, e deve retornar os bytes da imagem processada. O método `dimensions` deve retornar a largura e a altura da imagem, enquanto o método `dominantColor` deve retornar a cor média da imagem como uma string hexadecimal:

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
     * Get the dimensions of the given image contents.
     */
    public function dimensions(string $contents): array
    {
        // Read the image's width and height...

        return [0, 0];
    }

    /**
     * Get the dominant (average) color of the image as a hex string.
     */
    public function dominantColor(string $contents): string
    {
        // Calculate the image's average color...

        return '#000000';
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

> **Nota:**
> Para entender melhor como implementar um driver de imagem personalizado, você pode revisar a classe nativa do framework `Illuminate\Image\Drivers\InterventionDriver`.

Depois de implementar seu driver personalizado, você pode registrá-lo usando o método `extend` da facade `Image`. Normalmente, isso deve ser feito no método `boot` de um service provider:

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

Após registrar o driver, você pode usá-lo para uma imagem específica usando o método `using`:

```php
$image = $request->image('avatar')
    ->using('vips')
    ->cover(400, 400);
```

Você também pode configurar um driver personalizado como driver de imagem padrão da sua aplicação usando a opção `default` no arquivo de configuração `config/images.php` da sua aplicação ou pela variável de ambiente `IMAGE_DRIVER`:

```ini
IMAGE_DRIVER=vips
```

<a id="custom-transformations"></a>
### Transformações Personalizadas

Aplicações e pacotes podem definir transformações personalizadas criando uma classe que implementa o contrato `Illuminate\Contracts\Image\Transformation`. Transformações personalizadas podem então ser adicionadas a um pipeline de imagem usando o método `transform`:

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

Em seguida, registre um handler para a transformação e o driver usando o método `transformUsing` da facade `Image`. Normalmente, isso deve ser feito no método `boot` de um service provider:

```php
use App\Images\Transformations\Pixelate;
use Illuminate\Support\Facades\Image;
use Intervention\Image\Interfaces\ImageInterface;

Image::transformUsing('gd', Pixelate::class, function (ImageInterface $image, Pixelate $transformation) {
    return $image->pixelate($transformation->size);
});
```

Depois que o handler de transformação for registrado, você pode aplicar a transformação a uma imagem:

```php
use App\Images\Transformations\Pixelate;

$image = $request->image('avatar')
    ->transform(new Pixelate(12))
    ->store('avatars');
```

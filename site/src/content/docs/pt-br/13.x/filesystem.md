---
title: "Armazenamento de Arquivos"
---

- [Introdução](#introduction)
- [Configuração](#configuration)
    - [O Driver Local](#the-local-driver)
    - [O Disco Público](#the-public-disk)
    - [Pré-requisitos do Driver](#driver-prerequisites)
    - [Sistemas de Arquivos com Escopo, Somente Leitura e Read-Through](#scoped-and-read-only-filesystems)
    - [Sistemas de Arquivos Compatíveis com Amazon S3](#amazon-s3-compatible-filesystems)
- [Obtendo Instâncias de Disco](#obtaining-disk-instances)
    - [Discos Sob Demanda](#on-demand-disks)
- [Recuperando Arquivos](#retrieving-files)
    - [Baixando Arquivos](#downloading-files)
    - [URLs de Arquivos](#file-urls)
    - [URLs Temporárias](#temporary-urls)
    - [Metadados de Arquivos](#file-metadata)
- [Armazenando Arquivos](#storing-files)
    - [Prefixando e Sufixando Arquivos](#prepending-appending-to-files)
    - [Copiando e Movendo Arquivos](#copying-moving-files)
    - [Streaming Automático](#automatic-streaming)
    - [Uploads de Arquivos](#file-uploads)
    - [Visibilidade de Arquivos](#file-visibility)
    - [Manipulação de Imagens](#image-manipulation)
- [Deletando Arquivos](#deleting-files)
- [Diretórios](#directories)
- [Testes](#testing)
- [Sistemas de Arquivos Personalizados](#custom-filesystems)

<a id="introduction"></a>
## Introdução

O Laravel fornece uma poderosa abstração de sistema de arquivos graças ao maravilhoso pacote PHP [Flysystem](https://github.com/thephpleague/flysystem) de Frank de Jonge. A integração Flysystem do Laravel fornece drivers simples para trabalhar com sistemas de arquivos locais, SFTP e Amazon S3. Melhor ainda, é surpreendentemente simples alternar entre essas opções de armazenamento entre sua máquina de desenvolvimento local e servidor de produção, pois a API permanece a mesma para cada sistema.

<a id="configuration"></a>
## Configuração

O arquivo de configuração do sistema de arquivos do Laravel está localizado em `config/filesystems.php`. Dentro deste arquivo, você pode configurar todos os seus "discos" de sistema de arquivos. Cada disco representa um driver de armazenamento e local de armazenamento específicos. Configurações de exemplo para cada driver suportado estão incluídas no arquivo de configuração para que você possa modificar a configuração para refletir suas preferências e credenciais de armazenamento.

O driver `local` interage com arquivos armazenados localmente no servidor que executa a aplicação Laravel, enquanto o driver de armazenamento `sftp` é usado para FTP baseado em chave SSH. O driver `s3` é usado para escrever no serviço de armazenamento em nuvem S3 da Amazon.

> **Nota:**
> Você pode configurar quantos discos quiser e pode até ter múltiplos discos que usam o mesmo driver.

<a id="the-local-driver"></a>
### O Driver Local

Ao usar o driver `local`, todas as operações de arquivo são relativas ao diretório `root` definido no seu arquivo de configuração `filesystems`. Por padrão, este valor é definido como o diretório `storage/app/private`. Portanto, o seguinte método escreveria em `storage/app/private/example.txt`:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```

<a id="the-public-disk"></a>
### O Disco Público

O disco `public` incluído no arquivo de configuração `filesystems` da sua aplicação é destinado para arquivos que serão publicamente acessíveis. Por padrão, o disco `public` usa o driver `local` e armazena seus arquivos em `storage/app/public`.

Se seu disco `public` usa o driver `local` e você deseja tornar esses arquivos acessíveis pela web, você deve criar um link simbólico do diretório de origem `storage/app/public` para o diretório de destino `public/storage`:

Para criar o link simbólico, você pode usar o comando Artisan `storage:link`:

```shell
php artisan storage:link
```

Uma vez que um arquivo tenha sido armazenado e o link simbólico tenha sido criado, você pode criar uma URL para os arquivos usando o helper `asset`:

```php
echo asset('storage/file.txt');
```

Você pode configurar links simbólicos adicionais no seu arquivo de configuração `filesystems`. Cada um dos links configurados será criado quando você executar o comando `storage:link`:

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```

O comando `storage:unlink` pode ser usado para destruir seus links simbólicos configurados:

```shell
php artisan storage:unlink
```

<a id="driver-prerequisites"></a>
### Pré-requisitos do Driver

<a id="s3-driver-configuration"></a>
#### Configuração do Driver S3

Antes de usar o driver S3, você precisará instalar o pacote Flysystem S3 via o gerenciador de pacotes Composer:

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```

Um array de configuração do disco S3 está localizado no seu arquivo de configuração `config/filesystems.php`. Tipicamente, você deve configurar suas informações e credenciais do S3 usando as seguintes variáveis de ambiente que são referenciadas pelo arquivo de configuração `config/filesystems.php`:

```ini
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```

Para conveniência, essas variáveis de ambiente correspondem à convenção de nomenclatura usada pelo AWS CLI.

<a id="ftp-driver-configuration"></a>
#### Configuração do Driver FTP

Antes de usar o driver FTP, você precisará instalar o pacote Flysystem FTP via o gerenciador de pacotes Composer:

```shell
composer require league/flysystem-ftp "^3.0"
```

As integrações Flysystem do Laravel funcionam muito bem com FTP; no entanto, uma configuração de exemplo não está incluída no arquivo de configuração padrão `config/filesystems.php` do framework. Se você precisar configurar um sistema de arquivos FTP, você pode usar o exemplo de configuração abaixo:

```php
'ftp' => [
    'driver' => 'ftp',
    'host' => env('FTP_HOST'),
    'username' => env('FTP_USERNAME'),
    'password' => env('FTP_PASSWORD'),

    // Optional FTP Settings...
    // 'port' => env('FTP_PORT', 21),
    // 'root' => env('FTP_ROOT'),
    // 'passive' => true,
    // 'ssl' => true,
    // 'timeout' => 30,
],
```

<a id="sftp-driver-configuration"></a>
#### Configuração do Driver SFTP

Antes de usar o driver SFTP, você precisará instalar o pacote Flysystem SFTP via o gerenciador de pacotes Composer:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```

As integrações Flysystem do Laravel funcionam muito bem com SFTP; no entanto, uma configuração de exemplo não está incluída no arquivo de configuração padrão `config/filesystems.php` do framework. Se você precisar configurar um sistema de arquivos SFTP, você pode usar o exemplo de configuração abaixo:

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // Settings for basic authentication...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // Settings for SSH key-based authentication with encryption password...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'passphrase' => env('SFTP_PASSPHRASE'),

    // Settings for file / directory permissions...
    'visibility' => 'private', // `private` = 0600, `public` = 0644
    'directory_visibility' => 'private', // `private` = 0700, `public` = 0755

    // Optional SFTP Settings...
    // 'hostFingerprint' => env('SFTP_HOST_FINGERPRINT'),
    // 'maxTries' => 4,
    // 'passphrase' => env('SFTP_PASSPHRASE'),
    // 'port' => env('SFTP_PORT', 22),
    // 'root' => env('SFTP_ROOT', ''),
    // 'timeout' => 30,
    // 'useAgent' => true,
],
```

<a id="scoped-and-read-only-filesystems"></a>
### Sistemas de Arquivos com Escopo, Somente Leitura e Read-Through

Discos com escopo permitem que você defina um sistema de arquivos onde todos os caminhos são automaticamente prefixados com um determinado prefixo de caminho. Antes de criar um disco de sistema de arquivos com escopo, você precisará instalar um pacote Flysystem adicional via o gerenciador de pacotes Composer:

```shell
composer require league/flysystem-path-prefixing "^3.0"
```

Você pode criar uma instância com escopo de caminho de qualquer disco de sistema de arquivos existente definindo um disco que utiliza o driver `scoped`. Por exemplo, você pode criar um disco que define o escopo do seu disco `s3` existente para um prefixo de caminho específico, e então cada operação de arquivo usando seu disco com escopo utilizará o prefixo especificado:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```

Discos "somente leitura" permitem que você crie discos de sistema de arquivos que não permitem operações de escrita. Antes de usar a opção de configuração `read-only`, você precisará instalar um pacote Flysystem adicional via o gerenciador de pacotes Composer:

```shell
composer require league/flysystem-read-only "^3.0"
```

Em seguida, você pode incluir a opção de configuração `read-only` em um ou mais arrays de configuração do seu disco:

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```

Discos read-through permitem que você migre arquivos entre discos sem tempo de inatividade. Ao ler um arquivo, o Laravel verifica o disco principal primeiro. Se o arquivo existir apenas no disco de fallback, o Laravel lê o arquivo do disco de fallback e o copia para o disco principal para requisições futuras:

```php
'assets' => [
    'driver' => 'read-through',
    'primary' => 's3',
    'fallback' => 'legacy-s3',
],
```

Escritas e listagens de diretórios visam o disco principal. Verificações de existência de arquivo e metadados usam qualquer disco sem copiar arquivos para o disco principal. Se a cópia de um arquivo de fallback para o disco principal falhar, a leitura ainda terá sucesso por padrão. Para lançar uma exceção em vez disso, defina a opção de configuração `throw_on_promotion_failure` como `true`.

<a id="amazon-s3-compatible-filesystems"></a>
### Sistemas de Arquivos Compatíveis com Amazon S3

Por padrão, o arquivo de configuração `filesystems` da sua aplicação contém uma configuração de disco para o disco `s3`. Além de usar este disco para interagir com o [Amazon S3](https://aws.amazon.com/s3/), você pode usá-lo para interagir com qualquer serviço de armazenamento de arquivos compatível com S3 como [RustFS](https://github.com/rustfs/rustfs), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/) ou [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/).

Tipicamente, após atualizar as credenciais do disco para corresponder às credenciais do serviço que você planeja usar, você só precisa atualizar o valor da opção de configuração `endpoint`. O valor desta opção é tipicamente definido via a variável de ambiente `AWS_ENDPOINT`:

```php
'endpoint' => env('AWS_ENDPOINT', 'https://rustfs:9000'),
```

<a id="obtaining-disk-instances"></a>
## Obtendo Instâncias de Disco

A facade `Storage` pode ser usada para interagir com qualquer um dos seus discos configurados. Por exemplo, você pode usar o método `put` na facade para armazenar um avatar no disco padrão. Se você chamar métodos na facade `Storage` sem primeiro chamar o método `disk`, o método será automaticamente passado para o disco padrão:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```

Se sua aplicação interage com múltiplos discos, você pode usar o método `disk` na facade `Storage` para trabalhar com arquivos em um disco particular:

```php
Storage::disk('s3')->put('avatars/1', $content);
```

<a id="on-demand-disks"></a>
### Discos Sob Demanda

Às vezes, você pode desejar criar um disco em tempo de execução usando uma determinada configuração sem que essa configuração esteja realmente presente no arquivo de configuração `filesystems` da sua aplicação. Para conseguir isso, você pode passar um array de configuração ao método `build` da facade `Storage`:

```php
use Illuminate\Support\Facades\Storage;

$disk = Storage::build([
    'driver' => 'local',
    'root' => '/path/to/root',
]);

$disk->put('image.jpg', $content);
```

<a id="retrieving-files"></a>
## Recuperando Arquivos

O método `get` pode ser usado para recuperar o conteúdo de um arquivo. O conteúdo bruto em string do arquivo será retornado pelo método. Lembre-se, todos os caminhos de arquivo devem ser especificados relativos à localização "root" do disco:

```php
$contents = Storage::get('file.jpg');
```

Se o arquivo que você está recuperando contém JSON, você pode usar o método `json` para recuperar o arquivo e decodificar seu conteúdo:

```php
$orders = Storage::json('orders.json');
```

O método `exists` pode ser usado para determinar se um arquivo existe no disco:

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```

O método `missing` pode ser usado para determinar se um arquivo está faltando no disco:

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```

<a id="downloading-files"></a>
### Baixando Arquivos

O método `download` pode ser usado para gerar uma resposta que força o navegador do usuário a baixar o arquivo no caminho fornecido. O método `download` aceita um nome de arquivo como segundo argumento do método, que determinará o nome do arquivo que é visto pelo usuário que baixa o arquivo. Finalmente, você pode passar um array de headers HTTP como terceiro argumento ao método:

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```

<a id="file-urls"></a>
### URLs de Arquivos

Você pode usar o método `url` para obter a URL de um determinado arquivo. Se você estiver usando o driver `local`, isso normalmente apenas prefixará `/storage` ao caminho fornecido e retornará uma URL relativa para o arquivo. Se você estiver usando o driver `s3`, a URL remota totalmente qualificada será retornada:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```

Ao usar o driver `local`, todos os arquivos que devem ser publicamente acessíveis devem ser colocados no diretório `storage/app/public`. Além disso, você deve [criar um link simbólico](#the-public-disk) em `public/storage` que aponta para o diretório `storage/app/public`.

> **Aviso:**
> Ao usar o driver `local`, o valor de retorno de `url` não é codificado em URL. Por esta razão, recomendamos sempre armazenar seus arquivos usando nomes que criarão URLs válidas.

<a id="url-host-customization"></a>
#### Personalização do Host da URL

Se você gostaria de modificar o host para URLs geradas usando a facade `Storage`, você pode adicionar ou alterar a opção `url` no array de configuração do disco:

```php
'public' => [
    'driver' => 'local',
    'root' => storage_path('app/public'),
    'url' => env('APP_URL').'/storage',
    'visibility' => 'public',
    'throw' => false,
],
```

<a id="temporary-urls"></a>
### URLs Temporárias

Usando o método `temporaryUrl`, você pode criar URLs temporárias para arquivos armazenados usando os drivers `local` e `s3`. Este método aceita um caminho e uma instância `DateTime` especificando quando a URL deve expirar:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->plus(minutes: 5)
);
```

<a id="enabling-local-temporary-urls"></a>
#### Habilitando URLs Temporárias Locais

Se você começou a desenvolver sua aplicação antes do suporte a URLs temporárias ser introduzido ao driver `local`, você pode precisar habilitar URLs temporárias locais. Para fazer isso, adicione a opção `serve` ao array de configuração do seu disco `local` dentro do arquivo de configuração `config/filesystems.php`:

```php
'local' => [
    'driver' => 'local',
    'root' => storage_path('app/private'),
    'serve' => true, // [tl! add]
    'throw' => false,
],
```

<a id="s3-request-parameters"></a>
#### Parâmetros de Requisição S3

Se você precisar especificar [parâmetros de requisição S3](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests) adicionais, você pode passar o array de parâmetros de requisição como terceiro argumento ao método `temporaryUrl`:

```php
$url = Storage::temporaryUrl(
    'file.jpg',
    now()->plus(minutes: 5),
    [
        'ResponseContentType' => 'application/octet-stream',
        'ResponseContentDisposition' => 'attachment; filename=file2.jpg',
    ]
);
```

<a id="customizing-temporary-urls"></a>
#### Personalizando URLs Temporárias

Se você precisar personalizar como URLs temporárias são criadas para um disco de armazenamento específico, você pode usar o método `buildTemporaryUrlsUsing`. Por exemplo, isso pode ser útil se você tem um controller que permite baixar arquivos armazenados via um disco que normalmente não suporta URLs temporárias. Normalmente, este método deve ser chamado do método `boot` de um provedor de serviço:

```php
<?php

namespace App\Providers;

use DateTime;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\URL;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Storage::disk('local')->buildTemporaryUrlsUsing(
            function (string $path, DateTime $expiration, array $options) {
                return URL::temporarySignedRoute(
                    'files.download',
                    $expiration,
                    array_merge($options, ['path' => $path])
                );
            }
        );
    }
}
```

<a id="temporary-upload-urls"></a>
#### URLs de Upload Temporárias

> **Aviso:**
> A capacidade de gerar URLs de upload temporárias é suportada apenas pelos drivers `s3` e `local`.

Se você precisar gerar uma URL temporária que pode ser usada para enviar um arquivo diretamente da sua aplicação do lado do cliente, você pode usar o método `temporaryUploadUrl`. Este método aceita um caminho e uma instância `DateTime` especificando quando a URL deve expirar. O método `temporaryUploadUrl` retorna um array associativo que pode ser desestruturado na URL de upload e os headers que devem ser incluídos com a requisição de upload:

```php
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->plus(minutes: 5)
);
```

Este método é primariamente útil em ambientes serverless que requerem que a aplicação do lado do cliente envie arquivos diretamente para um sistema de armazenamento em nuvem como Amazon S3.

<a id="file-metadata"></a>
### Metadados de Arquivos

Além de ler e escrever arquivos, o Laravel também pode fornecer informações sobre os próprios arquivos. Por exemplo, o método `size` pode ser usado para obter o tamanho de um arquivo em bytes:

```php
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```

O método `lastModified` retorna o timestamp UNIX da última vez que o arquivo foi modificado:

```php
$time = Storage::lastModified('file.jpg');
```

O tipo MIME de um determinado arquivo pode ser obtido via o método `mimeType`:

```php
$mime = Storage::mimeType('file.jpg');
```

<a id="file-paths"></a>
#### Caminhos de Arquivos

Você pode usar o método `path` para obter o caminho de um determinado arquivo. Se você estiver usando o driver `local`, isso retornará o caminho absoluto para o arquivo. Se você estiver usando o driver `s3`, este método retornará o caminho relativo para o arquivo no bucket S3:

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```

<a id="storing-files"></a>
## Armazenando Arquivos

O método `put` pode ser usado para armazenar conteúdo de arquivos em um disco. Você também pode passar um `resource` PHP ao método `put`, que usará o suporte de stream subjacente do Flysystem. Lembre-se, todos os caminhos de arquivo devem ser especificados relativos à localização "root" configurada para o disco:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```

<a id="failed-writes"></a>
#### Escritas com Falha

Se o método `put` (ou outras operações de "escrita") não conseguir escrever o arquivo no disco, `false` será retornado:

```php
if (! Storage::put('file.jpg', $contents)) {
    // The file could not be written to disk...
}
```

Se você desejar, pode definir a opção `throw` dentro do array de configuração do disco do sistema de arquivos. Quando esta opção é definida como `true`, métodos de "escrita" como `put` lançarão uma instância de `League\Flysystem\UnableToWriteFile` quando as operações de escrita falharem:

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```

Alternativamente, você pode definir a opção `report` dentro do array de configuração do disco do sistema de arquivos. Quando esta opção é definida como `true`, o Laravel registrará a exceção subjacente usando o handler de exceções da sua aplicação quando uma operação de "escrita" falhar, sem lançar a exceção ou interromper o valor de retorno da operação de escrita:

```php
'public' => [
    'driver' => 'local',
    // ...
    'report' => true,
],
```

Se nem as opções `throw` nem `report` forem definidas, o disco retornará silenciosamente `false` em caso de falha e a exceção subjacente não será lançada ou registrada.

<a id="prepending-appending-to-files"></a>
### Prefixando e Sufixando Arquivos

Os métodos `prepend` e `append` permitem que você escreva no início ou final de um arquivo:

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```

<a id="copying-moving-files"></a>
### Copiando e Movendo Arquivos

O método `copy` pode ser usado para copiar um arquivo existente para uma nova localização no disco, enquanto o método `move` pode ser usado para renomear ou mover um arquivo existente para uma nova localização:

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```

Você pode usar os métodos `copyToDisk` e `moveToDisk` para copiar ou mover um arquivo para outro disco. O caminho do arquivo de origem será usado no disco de destino a menos que você forneça um terceiro argumento:

```php
Storage::disk('local')->copyToDisk('s3', 'reports/report.csv');

Storage::disk('local')->moveToDisk(
    's3', 'reports/report.csv', 'archive/report.csv'
);
```

<a id="automatic-streaming"></a>
### Streaming Automático

Streaming de arquivos para armazenamento oferece uso de memória significativamente reduzido. Se você gostaria que o Laravel gerenciasse automaticamente o streaming de um determinado arquivo para sua localização de armazenamento, você pode usar o método `putFile` ou `putFileAs`. Este método aceita uma instância `Illuminate\Http\File` ou `Illuminate\Http\UploadedFile` e fará streaming automaticamente do arquivo para sua localização desejada:

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// Automatically generate a unique ID for filename...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// Manually specify a filename...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```

Há algumas coisas importantes a notar sobre o método `putFile`. Note que nós especificamos apenas um nome de diretório e não um nome de arquivo. Por padrão, o método `putFile` gerará um ID único para servir como nome do arquivo. A extensão do arquivo será determinada examinando o tipo MIME do arquivo. O caminho para o arquivo será retornado pelo método `putFile` para que você possa armazenar o caminho, incluindo o nome de arquivo gerado, no seu banco de dados.

Os métodos `putFile` e `putFileAs` também aceitam um argumento para especificar a "visibilidade" do arquivo armazenado. Isso é particularmente útil se você estiver armazenando o arquivo em um disco na nuvem como Amazon S3 e gostaria que o arquivo fosse publicamente acessível via URLs geradas:

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```

<a id="file-uploads"></a>
### Uploads de Arquivos

Em aplicações web, um dos casos de uso mais comuns para armazenar arquivos é armazenar arquivos enviados pelo usuário como fotos e documentos. O Laravel torna muito fácil armazenar arquivos enviados usando o método `store` em uma instância de arquivo enviado. Chame o método `store` com o caminho no qual você deseja armazenar o arquivo enviado:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserAvatarController extends Controller
{
    /**
     * Update the avatar for the user.
     */
    public function update(Request $request): string
    {
        $path = $request->file('avatar')->store('avatars');

        return $path;
    }
}
```

Há algumas coisas importantes a notar sobre este exemplo. Note que nós especificamos apenas um nome de diretório, não um nome de arquivo. Por padrão, o método `store` gerará um ID único para servir como nome do arquivo. A extensão do arquivo será determinada examinando o tipo MIME do arquivo. O caminho para o arquivo será retornado pelo método `store` para que você possa armazenar o caminho, incluindo o nome de arquivo gerado, no seu banco de dados.

Você também pode chamar o método `putFile` na facade `Storage` para realizar a mesma operação de armazenamento de arquivo que o exemplo acima:

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```

<a id="specifying-a-file-name"></a>
#### Especificando um Nome de Arquivo

Se você não deseja que um nome de arquivo seja automaticamente atribuído ao seu arquivo armazenado, você pode usar o método `storeAs`, que recebe o caminho, o nome do arquivo e o (opcional) disco como seus argumentos:

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```

Você também pode usar o método `putFileAs` na facade `Storage`, que realizará a mesma operação de armazenamento de arquivo que o exemplo acima:

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```

> **Aviso:**
> Caracteres unicode não imprimíveis e inválidos serão automaticamente removidos dos caminhos de arquivo. Portanto, você pode desejar sanitizar seus caminhos de arquivo antes de passá-los aos métodos de armazenamento de arquivos do Laravel. Os caminhos de arquivo são normalizados usando o método `League\Flysystem\WhitespacePathNormalizer::normalizePath`.

<a id="specifying-a-disk"></a>
#### Especificando um Disco

Por padrão, o método `store` deste arquivo enviado usará seu disco padrão. Se você gostaria de especificar outro disco, passe o nome do disco como segundo argumento ao método `store`:

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```

Se você estiver usando o método `storeAs`, você pode passar o nome do disco como terceiro argumento ao método:

```php
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a id="other-uploaded-file-information"></a>
#### Outras Informações do Arquivo Enviado

Se você gostaria de obter o nome original e a extensão do arquivo enviado, você pode fazer isso usando os métodos `getClientOriginalName` e `getClientOriginalExtension`:

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```

No entanto, tenha em mente que os métodos `getClientOriginalName` e `getClientOriginalExtension` são considerados inseguros, pois o nome do arquivo e a extensão podem ser adulterados por um usuário malicioso. Por esta razão, você deve normalmente preferir os métodos `hashName` e `extension` para obter um nome e uma extensão para o upload de arquivo fornecido:

```php
$file = $request->file('avatar');

$name = $file->hashName(); // Generate a unique, random name...
$extension = $file->extension(); // Determine the file's extension based on the file's MIME type...
```

<a id="file-visibility"></a>
### Visibilidade de Arquivos

Na integração Flysystem do Laravel, "visibilidade" é uma abstração de permissões de arquivo em múltiplas plataformas. Arquivos podem ser declarados `public` ou `private`. Quando um arquivo é declarado `public`, você está indicando que o arquivo deve geralmente ser acessível a outros. Por exemplo, ao usar o driver S3, você pode recuperar URLs para arquivos `public`.

Você pode definir a visibilidade ao escrever o arquivo via o método `put`:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```

Se o arquivo já tiver sido armazenado, sua visibilidade pode ser recuperada e definida via os métodos `getVisibility` e `setVisibility`:

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```

Ao interagir com arquivos enviados, você pode usar os métodos `storePublicly` e `storePubliclyAs` para armazenar o arquivo enviado com visibilidade `public`:

```php
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```

<a id="image-manipulation"></a>
### Manipulação de Imagens

Se você precisar redimensionar, cortar ou converter uma imagem enviada antes de armazená-la, você pode usar os [recursos de manipulação de imagens](../images/) do Laravel:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->toWebp()
    ->storePublicly('avatars', 'public');
```

Você também pode criar uma instância de imagem a partir de um arquivo já armazenado em um dos seus discos de sistema de arquivos:

```php
$image = Storage::disk('public')->image('avatars/photo.jpg');
```

<a id="local-files-and-visibility"></a>
#### Arquivos Locais e Visibilidade

Ao usar o driver `local`, a [visibilidade](#file-visibility) `public` se traduz em permissões `0755` para diretórios e permissões `0644` para arquivos. Você pode modificar os mapeamentos de permissões no arquivo de configuração `filesystems` da sua aplicação:

```php
'local' => [
    'driver' => 'local',
    'root' => storage_path('app'),
    'permissions' => [
        'file' => [
            'public' => 0644,
            'private' => 0600,
        ],
        'dir' => [
            'public' => 0755,
            'private' => 0700,
        ],
    ],
    'throw' => false,
],
```

<a id="deleting-files"></a>
## Deletando Arquivos

O método `delete` aceita um único nome de arquivo ou um array de arquivos para deletar:

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```

Se necessário, você pode especificar o disco do qual o arquivo deve ser deletado:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```

<a id="directories"></a>
## Diretórios

<a id="get-all-files-within-a-directory"></a>
#### Obter Todos os Arquivos Dentro de um Diretório

O método `files` retorna um array de todos os arquivos dentro de um determinado diretório. Se você gostaria de recuperar uma lista de todos os arquivos dentro de um determinado diretório incluindo subdiretórios, você pode usar o método `allFiles`:

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```

<a id="get-all-directories-within-a-directory"></a>
#### Obter Todos os Diretórios Dentro de um Diretório

O método `directories` retorna um array de todos os diretórios dentro de um determinado diretório. Se você gostaria de recuperar uma lista de todos os diretórios dentro de um determinado diretório incluindo subdiretórios, você pode usar o método `allDirectories`:

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```

<a id="create-a-directory"></a>
#### Criar um Diretório

O método `makeDirectory` criará o diretório fornecido, incluindo quaisquer subdiretórios necessários:

```php
Storage::makeDirectory($directory);
```

<a id="delete-a-directory"></a>
#### Deletar um Diretório

Finalmente, o método `deleteDirectory` pode ser usado para remover um diretório e todos os seus arquivos:

```php
Storage::deleteDirectory($directory);
```

<a id="testing"></a>
## Testes

O método `fake` da facade `Storage` permite que você gere facilmente um disco falso que, combinado com as utilidades de geração de arquivo da classe `Illuminate\Http\UploadedFile`, simplifica muito os testes de uploads de arquivos. Por exemplo:

```php tab=Pest
<?php

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

test('albums can be uploaded', function () {
    Storage::fake('photos');

    $response = $this->json('POST', '/photos', [
        UploadedFile::fake()->image('photo1.jpg'),
        UploadedFile::fake()->image('photo2.jpg')
    ]);

    // Assert one or more files were stored...
    Storage::disk('photos')->assertExists('photo1.jpg');
    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

    // Assert one or more files were not stored...
    Storage::disk('photos')->assertMissing('missing.jpg');
    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

    // Assert that the number of files in a given directory matches the expected count...
    Storage::disk('photos')->assertCount('/wallpapers', 2);

    // Assert that a given directory is empty...
    Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');

    // Assert that the disk contains no files...
    Storage::disk('photos')->assertEmpty();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_albums_can_be_uploaded(): void
    {
        Storage::fake('photos');

        $response = $this->json('POST', '/photos', [
            UploadedFile::fake()->image('photo1.jpg'),
            UploadedFile::fake()->image('photo2.jpg')
        ]);

        // Assert one or more files were stored...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // Assert one or more files were not stored...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // Assert that the number of files in a given directory matches the expected count...
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // Assert that a given directory is empty...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');

        // Assert that the disk contains no files...
        Storage::disk('photos')->assertEmpty();
    }
}
```

Por padrão, o método `fake` deletará todos os arquivos em seu diretório temporário. Se você gostaria de manter esses arquivos, você pode usar o método "persistentFake" em vez disso. Para mais informações sobre testes de uploads de arquivos, você pode consultar as [informações de documentação de testes HTTP sobre uploads de arquivos](../http-tests/#testing-file-uploads).

> **Aviso:**
> O método `image` requer a [extensão GD](https://www.php.net/manual/en/book.image.php).

<a id="custom-filesystems"></a>
## Sistemas de Arquivos Personalizados

A integração Flysystem do Laravel fornece suporte para vários "drivers" nativamente; no entanto, o Flysystem não está limitado a estes e tem adaptadores para muitos outros sistemas de armazenamento. Você pode criar um driver personalizado se quiser usar um desses adaptadores adicionais na sua aplicação Laravel.

Para definir um sistema de arquivos personalizado você precisará de um adaptador Flysystem. Vamos adicionar um adaptador Dropbox mantido pela comunidade ao nosso projeto:

```shell
composer require spatie/flysystem-dropbox
```

Em seguida, você pode registrar o driver dentro do método `boot` de um dos [provedores de serviço](../providers/) da sua aplicação. Para conseguir isso, você deve usar o método `extend` da facade `Storage`:

```php
<?php

namespace App\Providers;

use Illuminate\Contracts\Foundation\Application;
use Illuminate\Filesystem\FilesystemAdapter;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\ServiceProvider;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Storage::extend('dropbox', function (Application $app, array $config) {
            $adapter = new DropboxAdapter(new DropboxClient(
                $config['authorization_token']
            ));

            return new FilesystemAdapter(
                new Filesystem($adapter, $config),
                $adapter,
                $config
            );
        });
    }
}
```

O primeiro argumento do método `extend` é o nome do driver e o segundo é um closure que recebe as variáveis `$app` e `$config`. O closure deve retornar uma instância de `Illuminate\Filesystem\FilesystemAdapter`. A variável `$config` contém os valores definidos em `config/filesystems.php` para o disco especificado.

Uma vez que você tenha criado e registrado o provedor de serviço da extensão, você pode usar o driver `dropbox` no seu arquivo de configuração `config/filesystems.php`.
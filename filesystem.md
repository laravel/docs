# Sistema de arquivos / Armazenamento na nuvem

- [Introdução](#introduction)
- [Configuração](#configuration)
- [Utilização básica](#basic-usage)
- [Custom Filesystems](#custom-filesystems)

<a name="introduction"></a>
## Introdução

O Laravel provê uma maravilhosa abstração do sistema de arquivos graças ao pacote PHP [Flysystem](https://github.com/thephpleague/flysystem), do Frank de Jonge. A integração "Laravel Flysystem" possibilita uma forma simples para utilizar drivers para trabalhar com sistemas de arquivos locais, Amazon S3, a Rackspace Cloud Storage. Melhor do que isso, é extremamente simples alternar entre essas opções de armazenamento. A API trata cada sistema de armazenamento da mesma forma!

<a name="configuration"></a>
## Configuração

O arquivo de configuração dos sistema de arquivos está localizado em `config/filesystems.php`. Neste arquivo você pode configurar todos os seus "discos". Cada disco representa um driver de armazenamento particular e o local de armazenamento. No arquivo de configuração você encontra exemplos para cada driver suportado. Então, simplesmente modifique a configuração para refletir as suas preferências e credenciais do seu armazenamento!

Antes de tilizar os drivers S3 or Rackspace, voCê precisará instalar os devidos pacotes através do Composer:

- Amazon S3: `league/flysystem-aws-s3-v2 ~1.0`
- Rackspace: `league/flysystem-rackspace ~1.0`

A propósito, você pode configurar quantos discos você quiser, e pode ter múltiplos discos que usem o mesmo driver.

Quando utilizando o driver `local`, observe que todas as operações com arquivos são relativas ao diretório `root` definido em seu arquivo de configuração. Por padrão, este valor é configurado no doretório `storage/app`. Portanto, o seguinte método iria armazenar um arquivo em `storage/app/file.txt`:

	Storage::disk('local')->put('file.txt', 'Contents');

<a name="basic-usage"></a>
## Utilização básica

A facade `Storage` pode ser utilizada para interagir com qualquer um de seus discos configurados. Alternativamente, você pode usar o contrato `Illuminate\Contracts\Filesystem\Factory` em qualquer classe que ela é resolvida via [IoC container](/docs/5.0/container).

#### Obtendo um disco específico

	$disk = Storage::disk('s3');

	$disk = Storage::disk('local');

#### Verificando se um arquivo existe

	$exists = Storage::disk('s3')->exists('file.jpg');

#### Executando métodos no disco padrão

	if (Storage::exists('file.jpg'))
	{
		//
	}

#### Obtendo o conteúdo de um arquivo

	$contents = Storage::get('file.jpg');

#### Atribuindo o conteúdo a um arquivo

	Storage::put('file.jpg', $contents);

#### Colocando conteúdo no início de um arquivo (prepend)

	Storage::prepend('file.log', 'Prepended Text');

#### Colocando conteúdo no fim de um arquivo (append)

	Storage::append('file.log', 'Appended Text');

#### Excluindo um arquivo

	Storage::delete('file.jpg');

	Storage::delete(['file1.jpg', 'file2.jpg']);

#### Copiando um arquivo para um novo local

	Storage::copy('old/file1.jpg', 'new/file1.jpg');

#### Movendo um arquivo para um novo local

	Storage::move('old/file1.jpg', 'new/file1.jpg');

#### Obtendo o tamanho de um arquivo

	$size = Storage::size('file1.jpg');

#### Obtendo a data da última nodificação (UNIX)

	$time = Storage::lastModified('file1.jpg');

#### Obtendo todos os arquivos de um diretório

	$files = Storage::files($directory);

	// Recursivo...
	$files = Storage::allFiles($directory);

#### Obtendo todos os diretórios de um diretório

	$directories = Storage::directories($directory);

	// Recursivo...
	$directories = Storage::allDirectories($directory);

#### Cria um diretório

	Storage::makeDirectory($directory);

#### Apaga um diretório

	Storage::deleteDirectory($directory);

<a name="custom-filesystems"></a>
## Custom Filesystems

Laravel's Flysystem integration provides drivers for several "drivers" out of the box; however, Flysystem is not limited to these and has adapters for many other storage systems. You can create a custom driver if you want to use one of these additional adapters in your Laravel application. Don't worry, it's not too hard!

In order to set up the custom filesystem you will need to create a service provider such as `DropboxFilesystemServiceProvider`. In the provider's `boot` method, you can inject an instance of the `Illuminate\Contracts\Filesystem\Factory` contract and call the `extend` method of the injected instance. Alternatively, you may use the `Disk` facade's `extend` method.

The first argument of the `extend` method is the name of the driver and the second is a Closure that receives the `$app` and `$config` variables. The resolver Closure must return an instance of `League\Flysystem\Filesystem`.

> **Note:** The $config variable will already contain the values defined in `config/filesystems.php` for the specified disk.

#### Dropbox Example

	<?php namespace App\Providers;

	use Storage;
	use League\Flysystem\Filesystem;
	use Dropbox\Client as DropboxClient;
	use League\Flysystem\Dropbox\DropboxAdapter;
	use Illuminate\Support\ServiceProvider;

	class DropboxFilesystemServiceProvider extends ServiceProvider {

		public function boot()
		{
			Storage::extend('dropbox', function($app, $config)
			{
				$client = new DropboxClient($config['accessToken'], $config['clientIdentifier']);

				return new Filesystem(new DropboxAdapter($client));
			});
		}

		public function register()
		{
			//
		}

	}

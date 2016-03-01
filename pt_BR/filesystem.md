# Filesystem / Cloud Storage

- [Introdução](#introduction)
- [Configuração](#configuration)
- [O Básico](#basic-usage)
	- [Obtendo Instâncias de Disco](#obtaining-disk-instances)
	- [Recuperando Arquivos](#retrieving-files)
	- [Armazenando Arquivos](#storing-files)
	- [Deletando Arquivos](#deleting-files)
	- [Diretórios](#directories)
- [Sistemas de Arquivo Personalizados](#custom-filesystems)

<a name="introduction"></a>
## Introdução

O Laravel provê uma poderosa abstração de sistemas de arquivos (filesystems) graças ao incrível pacote PHP [Flysystem](https://github.com/thephpleague/flysystem), criado por Frank de Jonge. A integração feita pelo Laravel Flysystem contém drivers simples para trabalhar com sistemas de arquivos locais, Amazon S3 e armazenamento em nuvem da Rackspace. Mais do que isso, é absurdamente simples realizar a troca entre essas opções de armazenamento, já que a API continua a mesma, independente do tipo de sistema implementado.

<a name="configuration"></a>
## Configuração

A configuração do sistema de armazenamento está localizada em `config/filesystems.php`. Dentro desse arquivo você deve configurar todos seus "discos". Cada disco representa um único driver de armazenamento e a sua localização. Para cada driver suportado, existe uma configuração de exemplo nesse arquivo. Então, para utilizá-lo, simplesmente modifique a configuração para refletir as suas preferências de armazenamento e suas credenciais.

E, obviamente, você pode configurar quantos discos você desejar, e talvez até utilizar múltiplos discos com o mesmo driver.

#### O Driver Local

Quando você utiliza o driver `local`, note que todas as operações com os arquivos são relativas ao diretório `root` definido em seu arquivo de configuração. Por padrão, esse arquivo é definido com o diretório `storage/app`. Portanto, o exemplo a seguir deverá armazenar um arquivo em `storage/app/file.txt`.

	Storage::disk('local')->put('file.txt', 'Contents');

#### Outros Pré Requisitos para os Drivers

Antes de utilizar os drivers para o Amazon S3 ou Rackspace, você precisa instalar o pacote apropriado via Composer:

- Amazon S3: `league/flysystem-aws-s3-v3 ~1.0`
- Rackspace: `league/flysystem-rackspace ~1.0`

<a name="basic-usage"></a>
## O Básico

<a name="obtaining-disk-instances"></a>
### Obtendo Instâncias de Disco

O Facada `Storage` pode ser utilizado para interagir com qualquer um de seus discos configurados. Por exemplo, você pode utilizar o método `put` no facade para armazenar uma imagem de perfil no disco padrão. Se você realizar a chamada de métodos com o facade `Storage` sem chamar previamente o método `disk`, o Laravel utilizará automaticamente seu disco padrão.

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

Ao utilizar múltiplos discos, você pode acessar um disco específico usando o método `disk` no facade `Storage`. E, obviamente, você deve continuar encadeando os métodos que você deseja executar nesse disco:

	$disk = Storage::disk('s3');

	$contents = Storage::disk('local')->get('file.jpg')

<a name="retrieving-files"></a>
### Recuperando Arquivos

O método `get` pode ser utilizado para recuperar o conteúdo de um arquivo. Com o método a seguir, o conteúdo será retornado em formato de strings simples:

	$contents = Storage::get('file.jpg');

O método `exists` deve ser utilizado para determinar se um determinado arquivo existe no disco:

	$exists = Storage::disk('s3')->exists('file.jpg');

#### Informações de Metadados

O método `size` deve ser utilizado para buscar o tamanho do arquivo em bytes:

	$size = Storage::size('file1.jpg');

O método `lastModified`  retorna um timestamp no formato UNIX da última vez que o arquivo foi modificado:

	$time = Storage::lastModified('file1.jpg');

<a name="storing-files"></a>
### Armazenando Arquivos

O método `put` deve ser utilizado para armazenar um arquivo no disco. Você também pode passar um `resource` PHP para o método `put`, que utilizará o Flysystem's como um apoio adjascente. A utilização de streams é altamente recomendada quando você estiver lidando com arquivos grandes:

	Storage::put('file.jpg', $contents);

	Storage::put('file.jpg', $resource);

O método `copy` deve ser utilizado para copiar um arquivo existente para uma nova localização no disco:

	Storage::copy('old/file1.jpg', 'new/file1.jpg');

O método `move` pode ser utilizado para mover um arquivo existente para uma nova localização.:

	Storage::move('old/file1.jpg', 'new/file1.jpg');

#### Inserindo conteúdo no Início e no Fim dos arquivos

Os métodos `prepend` e `append` lhe permitem adicionar conteúdo facilmente ao começo (prepend) ou ao fim (append) do arquivo:

	Storage::prepend('file.log', 'Esse texto vem no início');

	Storage::append('file.log', 'Texto no fim do arquivo');

<a name="deleting-files"></a>
### Deletando Arquivos

O método `delete` aceita um único nome de arquivo ou um array de arquivos para serem removidos do disco:

	Storage::delete('file.jpg');

	Storage::delete(['file1.jpg', 'file2.jpg']);

<a name="directories"></a>
### Diretórios

#### Buscar todos os arquivos que estão em um diretório

O método `files` retorna um array com todos os arquivos de determinado diretório. Caso você queira retornar uma lista com todos os arquivos do diretório incluindo os seus subdiretórios, você deve usar o método `allFiles`:

	$files = Storage::files($directory);

	$files = Storage::allFiles($directory);

#### Buscando Todos os Subdiretórios de um Diretório

O método `directories` retorna um array com todos os diretórios que estão dentro do diretório passado como parâmetro. Adicionalmente, você pode usar o método `allDirectories` para obter uma lista com os diretórios e subdiretórios do diretório passado como parâmetro:

	$directories = Storage::directories($directory);

	// Recursive...
	$directories = Storage::allDirectories($directory);

#### Criando um Diretório

O método `makeDirectory` vai cria um diretório, incluindo qualquer subdiretório adicional:

	Storage::makeDirectory($directory);

#### Deletando um diretório

Finalmente, o método `deleteDirectory` deve ser utilizado para remover um diretório, incluindo todo seu conteúdo, do disco:

	Storage::deleteDirectory($directory);

<a name="custom-filesystems"></a>
## Sistemas de Arquivo Personalizados

A integração do Laravel Flysystem disponibiliza vários "drivers" por padrão; entretando, o Flysystem não está limitado à somente esses drivers, e possui integrações para muitos outros sistemas de armazenamento. Você pode criar um driver customizado se você quiser utilizar alguma dessas integrações adicionais com sua aplicação Laravel.

Para configurar um sistema de arquivos customizado você precisará criar um [service provider](/docs/{{version}}/providers), como um `DropboxServiceProvider`. No método `boot` do provider você deve utilizar o Facade `Storage` e o método `extend` para definir esse driver:

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

O primeiro parâmetro do método `extend` é o nome do driver e o segundo é a Closure que recebe as variáveis `$app` e `$config`. A Closure deve retornar uma instância de `League\Flysystem\Filesystem`. A variável `$config` contém os valores definidos em `config/filesystems.php` para o disco especificado.

Assim, a partir do momento que você criou um service provider para registrar a extensão, você pode usar o seu `dropbox` driver em seu arquivo de configuração que está em `config/filesystem.php`.

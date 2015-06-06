# Desenvolvimento de Pacotes

- [Introdução](#introduction)
- [Service Providers](#service-providers)
- [Rotas](#routing)
- [Recursos](#resources)
	- [Views](#views)
	- [Traduções](#translations)
	- [Configurações](#configuration)
- [Assets públicos](#public-assets)
- [Publicando Grupos de Arquivos](#publishing-file-groups)

<a name="introduction"></a>
## Introdução

Pacotes são um modo primário de adicionar funcionalidades ao Laravel. Eles podem fazer coisas excelentes, como o [Carbon](https://github.com/briannesbitt/Carbon), ou o framework de testes BDD [Behat](https://github.com/Behat/Behat).

E é claro, existem diferentes tipos de pacotes. Alguns deles são agnósticos, isso significa que funcionam em qualquer framework, não somente Laravel. Carbon e Behat são exemplos de pacotes agnósticos. Qualquer um desses pacotes podem ser usados com o Laravel simplemente requerindo-os no arquivo `composer.json`.

Por outro lado, existem pacotes que são para uso específico no Laravel. Esses pacotes podem ter rotas, controllers, views e configurações específicas para melhor entrosamento com a aplicação Laravel. Esse artigo lhe instruirá a construir pacotes que serão específicos para Laravel.

<a name="service-providers"></a>
## Service Providers

[Service providers](/docs/{{version}}/providers) são o ponto de conexão entre seu pacote e o Laravel. Um service provider é responsável por atrelar coisas no [service container](/docs/{{version}}/container) do Laravel e informá-lo onde estão os recursos como views, configurações, e arquivos de localização.

Um service provider deve estender a classe `Illuminate\Support\ServiceProvider` e conter dois métodos: `register` e `boot`. A classe base `ServiceProvider` está localizada no pacote Composer `illuminate/support`, que você deve adicionar nas dependências do seu pacote.

Para aprender mais sobre a estrutura do service provider, leia [sua documentação](/docs/{{version}}/providers).

<a name="routing"></a>
## Rotas

Para definir rotas para seu pacote, simplesmente `require` o arquivo de rotas dentro do método `boot` do service provider. Dentro do seu arquivo de rotas você pode usar o facade `Route` para [registrar rotas](/docs/{{version}}/routing) como você quiser dentro de uma aplicação Laravel típica:

	/**
	 * Perform post-registration booting of services.
	 *
	 * @return void
	 */
	public function boot()
	{
		if (! $this->app->routesAreCached()) {
			require __DIR__.'/../../routes.php';
		}
	}

<a name="resources"></a>
## Recursos

<a name="views"></a>
### Views

Para registrar [views](/docs/{{version}}/views)  do seu pacote com Laravel, você precisa dizer ao Laravel onde as views estão localizadas. Você pode fazer isso usando o método do service provider `loadViewsFrom`. Esse método aceita dois argumentos: o caminho para o diretório das suas views e o nome do seu pacote. Por exemplo, se o nome do seu pacote é `courier`, adicione o seguinte trecho ao método `boot` do service provider:

	/**
	 * Perform post-registration booting of services.
	 *
	 * @return void
	 */
	public function boot()
	{
		$this->loadViewsFrom(__DIR__.'/path/to/views', 'courier');
	}


As views do pacote serão referenciadas usando a sintaxe dois-pontos-duplos `package::view`. Então, você pode carregar uma view `admin` do seu pacote `courier` da seguinte maneira:

	Route::get('admin', function () {
		return view('courier::admin');
	});

#### Sobrescrevendo as Views do Pacote

Quando você usa o método `loadViewsFrom`, o Laravel na realidade registra **duas** localizações para suas views: Uma no diretório da sua aplicação `resources/views/vendor` e outra no diretório que você especificou. Então, usando o exemplo `courier`: Quando você requerer uma view do pacote, o Laravel irá primeiro checar se existe uma versão dessa view gerada pelo desenvolvedor que está usando seu pacote em `resources/views/vendor/courier`. Então, se não há uma versão dessa view, o Laravel irá procurar a view no diretório que você especificou na chamada ao método `loadViewsFrom`. Isso torna fácil para o usuário final (desenvolvedor que está usando seu pacote) customizar ou sobrescrevê-las.

#### Publicando Views

Se você gostaria de disponibilizar suas views para o diretório da aplicação `resources/views/vendor`, você pode usar o método `publishes` do service provider. Esse método aceita um array cujos índices são caminho principal de cada diretório de views do seu pacote e valor é o local de sua publicação, neste caso `resources/views/vendor/courier`:

	/**
	 * Perform post-registration booting of services.
	 *
	 * @return void
	 */
	public function boot()
	{
		$this->loadViewsFrom(__DIR__.'/path/to/views', 'courier');

		$this->publishes([
			__DIR__.'/path/to/views' => base_path('resources/views/vendor/courier'),
		]);
	}

Agora, quando os desenvolvedores que usam seu pacote executarem o comando Artisan `vendor:publish`, as views do seu pacote serão copiadas para o local que você especificou.

<a name="translations"></a>
### Traduções

Se seu pacote contiver [arquivos de tradução](/docs/{{version}}/localization), você pode usar o método `loadTranslationsFrom` para informar ao Laravel como carregá-las. Por exemplo, se o nome do seu pacote é "courier", você pode adicionar o seguinte trecho ao método `boot` do service provider:

	/**
	 * Perform post-registration booting of services.
	 *
	 * @return void
	 */
	public function boot()
	{
		$this->loadTranslationsFrom(__DIR__.'/path/to/translations', 'courier');
	}

As traduções de pacotes são referenciadas usando a sintaxe dois-pontos-duplos. Então, se você quiser carregar a linha `welcome` do arquivo `messages` do pacote `courier`, seria assim:

	echo trans('courier::messages.welcome');

<a name="configuration"></a>
### Configuração

Usualmente, você pode querer publicar os arquivos de configuração do seu pacote para o diretório `config` da aplicação. Isso permitirá que desenvolvedores que usam seu pacote possam facilmente sobrescrever suas configurações padrão. Para publicar um arquivo de configuração, use o método `publishes` do service provider dentro do método `boot`:

	/**
	 * Perform post-registration booting of services.
	 *
	 * @return void
	 */
	public function boot()
	{
		$this->publishes([
			__DIR__.'/path/to/config/courier.php' => config_path('courier.php'),
		]);
	}

Agora, quando o desenvolvedor que usa seu pacote executar o comando Artisan `vendor:publish`, seu arquivo de configuração será copiado para o diretório que você especificou. E é claro, uma vez que seu arquivo foi publicado, ele pode ser acessado como qualquer outro arquivo de configuração:

	$value = config('courier.option');

#### Configuração Padrão do Pacote

Você pode escolher fundir as configurações do seu pacote com a cópia das configurações da aplicação. Isso permitira que os desenvolvedores incluam somente as opções que eles querem sobrescrever na cópia do seu arquivo de configuração. Para fundir as configurações, no método `register` do seu service provider use  `mergeConfigFrom`:

	/**
	 * Register bindings in the container.
	 *
	 * @return void
	 */
	public function register()
	{
		$this->mergeConfigFrom(
			__DIR__.'/path/to/config/courier.php', 'courier'
		);
	}

<a name="public-assets"></a>
## Assets Públicos

Você pode ter assets como JavaScript, CSS e imagens. Para publicar esses assets no diretório `public` da aplicação, use o método `publishes` do service provider. No exemplo a seguir, nós vamos também adicionar uma tag de grupo `public`, que pode ser usada para publicar grupos de assets:

	/**
	 * Perform post-registration booting of services.
	 *
	 * @return void
	 */
	public function boot()
	{
		$this->publishes([
			__DIR__.'/path/to/assets' => public_path('vendor/courier'),
		], 'public');
	}

Agora, quando o desenvolvedor que usa seu pacote executar o comando Artisan `vendor:publish`, seus assets serão copiados para o local especificado. Se você precisar sobrescrever os assets toda vez que seu pacote for atualizado, você pode usar a flag `--force`.

	php artisan vendor:publish --tag=public --force

Caso queira se certificar que os assets serão sempre atualizados, você pode adicionar esse comando na lista de comandos `post-update-cmd` no seu arquivo `composer.json`.

<a name="publishing-file-groups"></a>
## Publicando Grupos de Arquivos

Você pode publicar grupos de assets e recursos separadamente. Por exemplo, se quiser que seus usuários possam publicar os arquivos configuração do seu pacote sem forçá-lo a publicar também os assets ao mesmo tempo. Para evitar isso, use tags quando chamar o método `publishes`. Por exemplo, vamos definir dois grupos de publicação no método `boot` do service provider do pacote.

	/**
	 * Perform post-registration booting of services.
	 *
	 * @return void
	 */
	public function boot()
	{
		$this->publishes([
			__DIR__.'/../config/package.php' => config_path('package.php')
		], 'config');

		$this->publishes([
			__DIR__.'/../database/migrations/' => database_path('/migrations')
		], 'migrations');
	}

Agora os usuários poderão publicar esses grupos separadamente, referenciado o nome da tag quando usar o comando Artisan `vendor:publish`:

	php artisan vendor:publish --provider="Vendor\Providers\PackageServiceProvider" --tag="config"


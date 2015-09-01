# Laravel Elixir

- [Introdução](#introduction)
- [Instalação & Configuração](#installation)
- [Executando o Elixir](#running-elixir)
- [Trabalhando com folhas de estilo (Stylesheets)](#working-with-stylesheets)
	- [Less](#less)
	- [Sass](#sass)
	- [CSS puro](#plain-css)
	- [Mapas de código](#css-source-maps)
- [Trabahando com scripts](#working-with-scripts)
	- [CoffeeScript](#coffeescript)
	- [Browserify](#browserify)
	- [Babel](#babel)
	- [Scripts](#javascript)
- [Versionando / Cache Busting](#versioning-and-cache-busting)
- [Gulp - Chamando tarefas existentes](#calling-existing-gulp-tasks)
- [Escrevendo extensões Elixir](#writing-elixir-extensions)
- [Extras](#elixir-extras)

<a name="introduction"></a>
## Introdução

Laravel Elixir provê uma limpa e fluente API para definir tarefas Gulp básicas para sua aplicação. Elixir suporta os mais comuns pré-processadores CSS, Javasript e também as ferramentas de teste. Usando métodos encadeados, elixir permite que você defina fluentemente o pipeline dos seus assets. Por exemplo:

```javascript
elixir(function(mix) {
	mix.sass('app.scss')
	   .coffee('app.coffee');
});
```

Se você já esteve confuso antes sobre como começar com Gulp e compilações de assets, você irá amar o Laravel Elixir. Entretanto, você não é obrigado a usá-lo enquanto desenvolve sua aplicação. Você é livre para usar qualquer outra ferramenta de assets pipeline, ou nenhuma delas.

<a name="installation"></a>
## Instalação & Configuração

### Instalando o NodeJS

Antes de executar o elixir, você deve se certificar que o NodeJS está instalado na sua máquina.

    node -v

Por padrão, Laravel Homestead inclue tudo que você precisa para começar; Entretanto, se você não usa o Vagrant, então você pode facilmente instalar o NodeJS visitando [a página de download](http://nodejs.org/download/).

### Gulp

O próximo passo, você precisará instalar o [Gulp](http://gulpjs.com) como um pacote NPM(gerenciador de pacotes do NodeJS) global:

    npm install --global gulp

### Laravel Elixir

Por último, você deve instalar o Elixir. Dentro da sua instalação do Laravel você encontrará o arquivo `package.json` na pasta principal. Pense nesse arquivo como o `composer.json`, exceto que ele define as dependências do Node, ao invés do PHP. Você deve instalar todas as dependências que ele referencia executando o seguinte comando:

	npm install

<a name="running-elixir"></a>
## Executando o Elixir

Elixir foi construído a partir da última versão do [Gulp](http://gulpjs.com), então, para executar as tarefas do Elixir você só precisa executar o comando `gulp` no seu terminal. Se você adicionar o parâmetro `--production` ao comando, isso indicará ao Elixir que deve minificar seu arquivos CSS e Javascript gerados:

	// Executa todas as tarefas...
	gulp

	// Executa todas as tarefas e minifica todos os CSS e Javascript gerados...
	gulp --production

#### Verificando por modificações nos Assets

É muito inconveniente ficar executando o comando `gulp` no terminal a cada alteração nos seus assets, você pode usar o comando `gulp watch`. Esse comando vai continar rodando no seu terminal e verificando alterações nos seus assets. Quando uma alteração acontecer, os assets serão compilados automaticamente.

    // Executa as tarefas a cada alteração nos assets
    gulp watch

	// Executa as tarefas a cada alteração nos assets e minifica os arquivos css e javascript gerados
	gulp watch --production

<a name="working-with-stylesheets"></a>
## Trabalhando com Folhas de Estilo

O arquivo `gulpfile.js` no diretório principal da sua aplicação contem todas as tarefas do Elixir. Essas tarefas podem ser aninhadas para definir como seus assets serão compilados.

<a name="less"></a>
### Less

Para compilar [Less](http://lesscss.org/) em CSS você precisa usar o método `less`. Esse método assume que seus arquivos Less estão armazenados em `resources/assets/less`. Por padrão, essa tarefa criará o arquivo CSS compilado em, por exemplo, `public/css/app.css`:

```javascript
elixir(function(mix) {
	mix.less("app.less");
});
```

Você pode também combinar multiplos arquivos Less em um único arquivo CSS. Novamente, o arquivo resultante será `public/css/app.css`. Se você desejar alterar o local de armazenamento do arquivo compilado, você pode passar o segundo argumento do método `less`:

```javascript
elixir(function(mix) {
	mix.less([
		"app.less",
		"controllers.less"
	], "public/assets/css");
});
```

<a name="sass"></a>
### Sass

O método `sass` permite que você compile [Sass](http://sass-lang.com/) em CSS. Assumindo que seus arquivos Sass estão armazenados em `resources/assets/sass`, você pode usar o método assim:

```javascript
elixir(function(mix) {
	mix.sass("app.scss");
});
```

Novamente, como no método `less`, você pode compilar multiplos arquivos em um único arquivo CSS, e até mesmo customizar o caminho do arquivo de resultado:

```javascript
elixir(function(mix) {
	mix.sass([
		"app.scss",
		"controllers.scss"
	], "public/assets/css");
});
```

#### Ruby Sass

Elixir usa a biblioteca LibSass para compilar. Em alguns casos ela pode ser vantajosa que a versão Ruby, embora mais lenta, porém mais rica em recursos. Assumindo que você tem tanto o Ruby quando a gem Sass instalados (`gem install sass`), você pode usar o compilador Ruby Sass da seguinte maneira:

```javascript
elixir(function(mix) {
	mix.rubySass("app.scss");
});
```

<a name="plain-css"></a>
### CSS Puro

Se você gostaria de combinar alguns arquivos em CSS puro em um único arquivo, você pode fazer isso através do método `styles`. Os caminhos passados para esse método são relativos ao diretório `resources/assets/css` e o arquivo css resultante será `public/css/all.css`:

```javascript
elixir(function(mix) {
	mix.styles([
		"normalize.css",
		"main.css"
	]);
});
```

Claro, você pode também modificar o caminho do arquivo de saída passando o segundo argumento do método `style`:

```javascript
elixir(function(mix) {
	mix.styles([
		"normalize.css",
		"main.css"
	], "public/assets/css");
});
```

<a name="css-source-maps"></a>
### Mapas de Código

Mapas de código são ativados automaticamente. Então, para cada arquivo compilado você verá um acompanhado `*.css.map` no mesmo diretório. Esse arquivo permitira rastrear seu código compilado de volta aos seus seletores originais em Sass ou Less quando for debugar no navegador.

Se você não quiser que os arquivos de mapa de código sejam gerados para seu CSS, você pode desabilitar essa funcionalidade com a opção:

```javascript
elixir.config.sourcemaps = false;

elixir(function(mix) {
	mix.sass("app.scss");
});
```

<a name="working-with-scripts"></a>
## Trabalhando com Scripts

O Elixir também provê algumas funções para ajudá-lo a trabalhar com arquivos JavaScript, compilar ECMAScript 6, CoffeeScript, Browserify, minificação ou simplesmente concatenar arquivos javascript plano.

<a name="coffeescript"></a>
### CoffeeScript

O método  `coffee` pode ser usado para compilar [CoffeeScript](http://coffeescript.org/) em javascript plano. O método `coffee` aceita um array de arquivos CoffeeScript relativos ao diretório `resources/assets/coffee` e são gerados em um único arquivo `app.js` no diretório `public/js`:

```javascript
elixir(function(mix) {
	mix.coffee(['app.coffee', 'controllers.coffee']);
});
```

<a name="browserify"></a>
### Browserify

Elixir também tem o método `browserify`, que lhe dá todos os benefícios de requerer módulos no navegador usando EcmaScript 6.

Essa tarefa assume que seus scripts estejão no diretório `resources/assets/js` e o resultado será o arquivo `public/js/bundle.js`:

```javascript
elixir(function(mix) {
	mix.browserify('index.js');
});
```

<a name="babel"></a>
### Babel

O método `babel` pode ser usado para compilar [EcmaScript 6 e 7](https://babeljs.io/docs/learn-es2015/) JavaScript. Esta função aceita um array de arquivos relativos ao diretório `resources/assets/js`, e gera um único arquivo `all.js` no diretório `public/js`:

```javascript
elixir(function(mix) {
	mix.babel([
                "order.js",
                "product.js"
        ]);
});
```

Para escolher um local de saída diferente, basta especificar seu caminho desejado como o segundo argumento. A assinatura e funcionalidade deste método são idênticos aos mix.scripts (), excluindo a compilação Babel.

<a name="javascript"></a>
### Scripts

Se você tem multiplos arquivos JavaScript que gostaria de combinar em um único arquivo, você pode usar o método `scripts`.

O método `scripts` assume que todos os arquivos são relativos ao diretório `resources/assets/js`, e o arquivo javascript resultante será `public/js/all.js` por padrão:

```javascript
elixir(function(mix) {
	mix.scripts([
		"jquery.js",
		"app.js"
	]);
});
```
Se você precisar combinar mais de um grupo de script em diferentes arquivos, você pode fazer múltiplas chamadas ao método `scripts`. O segundo argumento determina o nome do arquivo resultante para cada concatenação:

```javascript
elixir(function(mix) {
    mix.scripts(['app.js', 'controllers.js'], 'public/js/app.js')
       .scripts(['forum.js', 'threads.js'], 'public/js/forum.js');
});
```

Se você precisa combinar todos os arquivos em um diretório, você pode user o método `scriptsIn`. O arquivo resultate será `public/js/all.js`:

```javascript
elixir(function(mix) {
	mix.scriptsIn("public/js/some/directory");
});
```

<a name="versioning-and-cache-busting"></a>
## Versionamento / Evitando o Cache

Muitos desenvolvedores sufixam seus assets compilados com uma marca de tempo ou um token único para forçar o navegador a ler os novos assets ao invés das suas cópias locais em cache. O Elixir pode lidar com isso usando o método `version`.

O método `version` aceita o nome do arquivo relativo ao diretório `public` e adicionará um hash único ao nome desse arquivo, permitindo que o navegador renove seu cache. Por exemplo, o nome do arquivo gerado se parecerá com `all-16d570a7.css`:

```javascript
elixir(function(mix) {
	mix.version("css/all.css");
});
```

Após gerar o arquivo versionado, você deve usar a função global do Laravel `elixir` nas suas [views](/docs/{{version}}/views) para carregar o arquivo versionado propriamente com seu hash. A função `elixir` irá automaticamente determinar o nome do arquivo com hash:

	<link rel="stylesheet" href="{{ elixir('css/all.css') }}">

#### Versionando Múltiplos Arquivos

Você pode passar um array de arquivos para o método `version` para versioná-los:

```javascript
elixir(function(mix) {
	mix.version(["css/all.css", "js/app.js"]);
});
```

Após esses arquivos terem sido versionados, você pode usar a função `elixir` para gerar os links para os arquivos com seus próprios hashs. Lembre-se, você só precisa passar o nome do arquivo sem hash para a função `elixir`. A função irá usar o nome sem hash para determinar a versão do hash atual desse arquivo:

	<link rel="stylesheet" href="{{ elixir('css/all.css') }}">

	<script src="{{ elixir('js/app.js') }}"></script>

<a name="calling-existing-gulp-tasks"></a>
## Executando Tarefas Existentes do Gulp

Se você precisa executar tarefas existentes do gulp pelo Elixir, você pode usar o método `task`. Como exemplo, imagine que você tem uma tarefa Gulp que simplesmente fala o texto quando invocada:
```javascript
gulp.task("speak", function() {
	var message = "Tea...Earl Grey...Hot";

	gulp.src("").pipe(shell("say " + message));
});
```

Se você quiser chamá-la pelo Elixir, use o método `mix.task` e passe o nome da tarefa como único argumento:

```javascript
elixir(function(mix) {
    mix.task('speak');
});
```

#### Observador de Modificações de Arquivos

Se precisa registrar um observador para executar sua tarefa cada vez que alguns arquivos sejam modificados, passe uma expressão regular no segundo argumento do método `task`:

```javascript
elixir(function(mix) {
    mix.task('speak', 'app/**/*.php');
});
```

<a name="writing-elixir-extensions"></a>
## Escrevendo Extensões Elixir

Se você precisa de mais flexibilidade que a `task` do Elixir provê, você pode criar suas próprias extensões. Extensões Elixir permitem que você passe argumentos customizados para as tarefas. Por exemplo, pode poderia escrever uma extenção assim:

```javascript
// Arquivo: elixir-extensions.js

var gulp = require("gulp");
var shell = require("gulp-shell");
var elixir = require("laravel-elixir");

elixir.extend("speak", function(message) {

	gulp.task("speak", function() {
		gulp.src("").pipe(shell("say " + message));
	});

	return this.queueTask("speak");

 });
```

E é só isso! Você pode criar suas tarefas no início do Gulpfile, ou extrair em arquivos de tarefas customizadas. Por exemplo, se você colocar suas extençoes em `elixir-extensions.js`, você pode requerer esse arquivo a partir do seu `Gulpfile` dessa forma:

```javascript
// Arquivo: Gulpfile.js

var elixir = require("laravel-elixir");

require("./elixir-tasks")

elixir(function(mix) {
	mix.speak("Tea, Earl Grey, Hot");
});
```

#### Observador de Modificações de Arquivos

Se você quiser que suas tarefas sejam re-executadas enquanto executa o comando `gulp watch`, você pode registrar um observador:

```javascript
this.registerWatcher("speak", "app/**/*.php");

return this.queueTask("speak");
```

<a name="elixir-extras"></a>
# Extras

instale o bower e crie o arquivo .bowerrc:

```javascript
{
  "directory": "vendor/bower_components"
}
```
em `projeto\node_modules\laravel-elixir\Config.js` ja vem alguns paths configurado para usar:

```javascript
//Diretorio padrão do bower
var bowerDir  = elixir.config.bowerDir + '/';
```
Se você usa **angular** pode instalar tambem [laravel-elixir-angular](https://www.npmjs.com/package/laravel-elixir-angular):

    npm i laravel-elixir-angular

Exemplo:

```javascript
var elixir = require('laravel-elixir');

require('laravel-elixir-angular');

elixir(function(mix) {
   mix.angular();
});
```

ou, se quiser usar **typescript**, instale  [laravel-elixir-typescript](https://www.npmjs.com/package/laravel-elixir-typescript):

    npm i laravel-elixir-typescript

Exemplo:

```javascript
var elixir = require('laravel-elixir');

require('laravel-elixir-typescript');

elixir(function(mix) {
  mix.typescript('app.js');
});
```


---
title: "MongoDB"
---

- [Introdução](#introduction)
- [Instalação](#installation)
    - [Driver do MongoDB](#mongodb-driver)
    - [Iniciando um Servidor MongoDB](#starting-a-mongodb-server)
    - [Instalando o Pacote Laravel MongoDB](#install-the-laravel-mongodb-package)
- [Configuração](#configuration)
- [Recursos](#features)

<a id="introduction"></a>
## Introdução

O [MongoDB](https://www.mongodb.com/resources/products/fundamentals/why-use-mongodb) é um dos bancos de dados NoSQL orientados a documentos mais populares, utilizado por sua alta carga de escrita (útil para analytics ou IoT) e alta disponibilidade (fácil configuração de replica sets com failover automático). Ele também pode fazer sharding do banco de dados facilmente para escalabilidade horizontal e possui uma linguagem de consulta poderosa para realizar agregações, buscas de texto ou consultas geoespaciais.

Em vez de armazenar dados em tabelas de linhas ou colunas como bancos SQL, cada registro em um banco MongoDB é um documento descrito em BSON, uma representação binária dos dados. As aplicações podem então recuperar essas informações em formato JSON. Ele suporta uma grande variedade de tipos de dados, incluindo documentos, arrays, documentos embutidos e dados binários.

Antes de usar o MongoDB com o Laravel, recomendamos instalar e usar o pacote `mongodb/laravel-mongodb` via Composer. O pacote `laravel-mongodb` é mantido oficialmente pelo MongoDB. Embora o MongoDB seja nativamente suportado pelo PHP através do driver MongoDB, o pacote [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) oferece uma integração mais completa com o Eloquent e outros recursos do Laravel:

```shell
composer require mongodb/laravel-mongodb
```

<a id="installation"></a>
## Instalação

<a id="mongodb-driver"></a>
### Driver do MongoDB

Para se conectar a um banco de dados MongoDB, é necessária a extensão PHP `mongodb`. Se você está desenvolvendo localmente usando o [Laravel Herd](https://herd.laravel.com) ou instalou o PHP via `php.new`, você já tem essa extensão instalada no seu sistema. No entanto, se precisar instalar a extensão manualmente, você pode fazê-lo via PECL:

```shell
pecl install mongodb
```

Alternativamente, você pode instalar a extensão usando o [PIE](https://github.com/php/pie), o instalador oficial de extensões do PHP:

```shell
pie install mongodb/mongodb-extension
```

Para mais informações sobre a instalação da extensão MongoDB para PHP, consulte as [instruções de instalação da extensão MongoDB para PHP](https://www.php.net/manual/en/mongodb.installation.php).

<a id="starting-a-mongodb-server"></a>
### Iniciando um Servidor MongoDB

O MongoDB Community Server pode ser usado para executar o MongoDB localmente e está disponível para instalação no Windows, macOS, Linux ou como um container Docker. Para aprender a instalar o MongoDB, consulte o [guia oficial de instalação do MongoDB Community](https://docs.mongodb.com/manual/administration/install-community/).

A string de conexão para o servidor MongoDB pode ser definida no seu arquivo `.env`:

```ini
MONGODB_URI="mongodb://localhost:27017"
MONGODB_DATABASE="laravel_app"
```

Para hospedar o MongoDB na nuvem, considere usar o [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
Para acessar localmente um cluster do MongoDB Atlas a partir da sua aplicação, você precisará [adicionar seu próprio endereço IP nas configurações de rede do cluster](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/) à IP Access List do projeto.

A string de conexão para o MongoDB Atlas também pode ser definida no seu arquivo `.env`:

```ini
MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority"
MONGODB_DATABASE="laravel_app"
```

<a id="install-the-laravel-mongodb-package"></a>
### Instalando o Pacote Laravel MongoDB

Por fim, use o Composer para instalar o pacote Laravel MongoDB:

```shell
composer require mongodb/laravel-mongodb
```

> **Nota:**
> Esta instalação do pacote falhará se a extensão PHP `mongodb` não estiver instalada. A configuração do PHP pode ser diferente entre o CLI e o servidor web, então certifique-se de que a extensão esteja habilitada nas duas configurações.

<a id="configuration"></a>
## Configuração

Você pode configurar sua conexão com o MongoDB através do arquivo de configuração `config/database.php` da sua aplicação. Neste arquivo, adicione uma conexão `mongodb` que utilize o driver `mongodb`:

```php
'connections' => [
    'mongodb' => [
        'driver' => 'mongodb',
        'dsn' => env('MONGODB_URI', 'mongodb://localhost:27017'),
        'database' => env('MONGODB_DATABASE', 'laravel_app'),
    ],
],
```

<a id="features"></a>
## Recursos

Após concluir a configuração, você pode usar o pacote `mongodb` e a conexão com o banco de dados na sua aplicação para aproveitar uma variedade de recursos poderosos:

- [Usando o Eloquent](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/eloquent-models/): os models podem ser armazenados em coleções do MongoDB. Além dos recursos padrão do Eloquent, o pacote Laravel MongoDB oferece recursos adicionais, como relacionamentos embutidos. O pacote também fornece acesso direto ao driver do MongoDB, que pode ser usado para executar operações como consultas brutas e pipelines de agregação.
- [Escreva consultas complexas](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/query-builder/) usando o query builder.
- [Busca por similaridade / vetorial](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/fundamentals/vector-search/) usando embeddings vetoriais e o método Eloquent `vectorSearch`.
- O [driver de cache](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/) `mongodb` é otimizado para usar recursos do MongoDB, como índices TTL, para limpar automaticamente entradas de cache expiradas.
- [Despache e processe jobs enfileirados](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/) com o driver de fila `mongodb`.
- [Armazenamento de arquivos no GridFS](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/filesystems/), via o [GridFS Adapter para Flysystem](https://flysystem.thephpleague.com/docs/adapter/gridfs/).
- [Busca de texto completo](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/scout/) usando o engine `mongodb` do Scout.
- A maioria dos pacotes de terceiros que usam uma conexão de banco de dados ou o Eloquent pode ser utilizada com o MongoDB.

Para continuar aprendendo a usar o MongoDB e o Laravel, consulte o [Guia de Início Rápido](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/) do MongoDB.

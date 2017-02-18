# Database: Seeding

- [Introdução](#introduction)
- [Criando Seeders](#writing-seeders)
	- [Usando Model Factories](#using-model-factories)
	- [Chamando Seeders Adicionais](#calling-additional-seeders)
- [Executando Seeders](#running-seeders)

<a name="introduction"></a>
## Introdução

Laravel inclui um método simples para popular (semear) seu banco de dados com dados de teste usando as classes Seed. Todas as Seeders são armazenadas em `database/seeds`. Uma classe Seed podem ter o nome que você desejar, mas provavelmente deve seguir alguma mínima convenção, como por exemplo `UserTableSeeder`, etc. Por padrão, uma classe `DatabaseSeeder` é definida para você. A partir desta classe, você pode usar o método `call` para executar outras seeders, o que lhe permite controlar a ordem na qual o banco de dados será semeado.

<a name="writing-seeders"></a>
## Criando Seeders

Para gerar uma seeder, você pode usar o comando `make:seeder` [Artisan command](/docs/{{version}}/artisan). Todas as seeders geradas pelo framework serão armazenadas no diretório `database/seeders`:

	php artisan make:seeder UserTableSeeder

Uma classe seeder contém somente um método por padrão: `run`. Este método é chamado quando o comando `db:seed` [Artisan command](/docs/{{version}}/artisan) é executado. Dentro do método `run` você pode inserir os dados para seu banco de dados da forma como desejar. Pode usar [query builder](/docs/{{version}}/queries) para inserir os dados manualmente ou usar [Eloquent model factories](/docs/{{version}}/testing#model-factories).

Como exemplo, vamos modificar a classe `DatabaseSeeder` que vem como padrão em uma nova instalação do Laravel. Vamos adicionar a instrução insert do banco de dados para o método `run`:

	<?php

	use DB;
	use Illuminate\Database\Seeder;
	use Illuminate\Database\Eloquent\Model;

	class DatabaseSeeder extends Seeder
	{
	    /**
	     * Run the database seeds.
	     *
	     * @return void
	     */
	    public function run()
	    {
	        DB::table('users')->insert([
	        	'name' => str_random(10),
	        	'email' => str_random(10).'@gmail.com',
	        	'password' => bcrypt('secret'),
	        ]);
	    }
	}

<a name="using-model-factories"></a>
### Usando Model Factories

Claro, especificar manualmente os atributos para cada seed é complicado. Ao invés, você pode usar [model factories](/docs/{{version}}/testing#model-factories) para convenientemente gerar uma grande quantidade de registros para o banco de dados. Primeiro, veja a [documentação da model factory](/docs/{{version}}/testing#model-factories) para aprender como definir suas factories. Uma vez definidas as factories, pode usar a função helper `factory` para inserir registros em seu banco de dados.

Por exemplo, vamos criar 50 usuários e adicionar um relacionamento para cada usuário:

    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        factory('App\User', 50)->create()->each(function($u) {
        	$u->posts()->save(factory('App\Post')->make());
        });
    }

<a name="calling-additional-seeders"></a>
### Chamando Seeders Adicionais

Dentro da classe `DatabaseSeeder`, você pode usar o método `call` para executar classes seed adicionais. Usando o método `call` permite dividir seu database seeding em vários arquivos, para que um único arquivo seeder não se torne grande demais. Simplesmente informe o nome da classe seeder que você deseja executar:

    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        Model::unguard();

        $this->call('UserTableSeeder');
        $this->call('PostsTableSeeder');
        $this->call('CommentsTableSeeder');
    }

<a name="running-seeders"></a>
## Executando Seeders

Uma vez que escreveu sua classe seeder, você pode usar o comando `db:seed` do Artisan para popular seu banco de dados. Por padrão, o comando `db:seed` executa a classe `DatabaseSeeder`, que pode ser usada para chamar todas as outras classes seed. Entretanto, você pode usar a opção `--class` e especificar uma classe seeder para ser executada individualmente:

	php artisan db:seed

	php artisan db:seed --class=UserTableSeeder

Você pode também popular seu banco de dados com o comando `migrate:refresh`, que vai realizar o rollback e executar novamente todas suas migrations. Este comando é útil para reconstruir totalmente seu banco de dados:

	php artisan migrate:refresh --seed

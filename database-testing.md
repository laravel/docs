# Database Testing

- [Introduction](#introduction)
- [Resetting The Database After Each Test](#resetting-the-database-after-each-test)
    - [Using Migrations](#using-migrations)
    - [Using Transactions](#using-transactions)
- [Writing Factories](#writing-factories)
    - [Factory Types](#factory-types)
- [Using Factories](#using-factories)
    - [Creating Models](#creating-models)
    - [Persisting Models](#persisting-models)
    - [Relationships](#relationships)

<a name="introduction"></a>
## Introduction

Laravel provides a variety of helpful tools to make it easier to test your database driven applications. First, you may use the `seeInDatabase` helper to assert that data exists in the database matching a given set of criteria. For example, if you would like to verify that there is a record in the `users` table with the `email` value of `sally@example.com`, you can do the following:

    public function testDatabase()
    {
        // Make call to application...

        $this->seeInDatabase('users', [
            'email' => 'sally@example.com'
        ]);
    }

Of course, the `seeInDatabase` method and other helpers like it are for convenience. You are free to use any of PHPUnit's built-in assertion methods to supplement your tests.

<a name="resetting-the-database-after-each-test"></a>
## Resetting The Database After Each Test

It is often useful to reset your database after each test so that data from a previous test does not interfere with subsequent tests.

<a name="using-migrations"></a>
### Using Migrations

One approach to resetting the database state is to rollback the database after each test and migrate it before the next test. Laravel provides a simple `DatabaseMigrations` trait that will automatically handle this for you. Simply use the trait on your test class and everything will be handled for you:

    <?php

    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Illuminate\Foundation\Testing\DatabaseTransactions;

    class ExampleTest extends TestCase
    {
        use DatabaseMigrations;

        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->visit('/')
                 ->see('Laravel 5');
        }
    }

<a name="using-transactions"></a>
### Using Transactions

Another approach to resetting the database state is to wrap each test case in a database transaction. Again, Laravel provides a convenient `DatabaseTransactions` trait that will automatically handle this for you:

    <?php

    use Illuminate\Foundation\Testing\WithoutMiddleware;
    use Illuminate\Foundation\Testing\DatabaseMigrations;
    use Illuminate\Foundation\Testing\DatabaseTransactions;

    class ExampleTest extends TestCase
    {
        use DatabaseTransactions;

        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $this->visit('/')
                 ->see('Laravel 5');
        }
    }

> {note} This trait will only wrap the default database connection in a transaction. If your application is using multiple database connections, you will need to manually handle the transaction logic for those connections.

<a name="writing-factories"></a>
## Writing Factories

When testing, it is common to need to insert a few records into your database before executing your test. Instead of manually specifying the value of each column when you create this test data, Laravel allows you to define a default set of attributes for each of your [Eloquent models](/docs/{{version}}/eloquent) using model factories. To get started, take a look at the `database/factories/ModelFactory.php` file in your application. Out of the box, this file contains one factory definition:

    $factory->define(App\User::class, function (Faker\Generator $faker) {
        return [
            'name' => $faker->name,
            'email' => $faker->email,
            'password' => bcrypt(str_random(10)),
            'remember_token' => str_random(10),
        ];
    });

Within the Closure, which serves as the factory definition, you may return the default test values of all attributes on the model. The Closure will receive an instance of the [Faker](https://github.com/fzaninotto/Faker) PHP library, which allows you to conveniently generate various kinds of random data for testing.

Of course, you are free to add your own additional factories to the `ModelFactory.php` file. You may also create additional factory files for each model for better organization. For example, you could create `UserFactory.php` and `CommentFactory.php` files within your `database/factories` directory. All of the files within the `factories` directory will automatically be loaded by Laravel.

<a name="factory-types"></a>
### Factory Types

Sometimes you may wish to have multiple factories for the same Eloquent model class. For example, perhaps you would like to have a factory for "Administrator" users in addition to normal users. You may define these factories using the `defineAs` method:

    $factory->defineAs(App\User::class, 'admin', function ($faker) {
        return [
            'name' => $faker->name,
            'email' => $faker->email,
            'password' => str_random(10),
            'remember_token' => str_random(10),
            'admin' => true,
        ];
    });

Instead of duplicating all of the attributes from your base user factory, you may use the `raw` method to retrieve the base attributes. Once you have the attributes, simply supplement them with any additional values you require:

    $factory->defineAs(App\User::class, 'admin', function ($faker) use ($factory) {
        $user = $factory->raw(App\User::class);

        return array_merge($user, ['admin' => true]);
    });

<a name="using-factories"></a>
## Using Factories

<a name="creating-models"></a>
### Creating Models

Once you have defined your factories, you may use the global `factory` function in your tests or seed files to generate model instances. So, let's take a look at a few examples of creating models. First, we'll use the `make` method to create models but not save them to the database:

    public function testDatabase()
    {
        $user = factory(App\User::class)->make();

        // Use model in tests...
    }

You may also create a Collection of many models or create models of a given type:

    // Create three App\User instances...
    $users = factory(App\User::class, 3)->make();

    // Create an "admin" App\User instance...
    $user = factory(App\User::class, 'admin')->make();

    // Create three "admin" App\User instances...
    $users = factory(App\User::class, 'admin', 3)->make();

#### Overriding Attributes

If you would like to override some of the default values of your models, you may pass an array of values to the `make` method. Only the specified values will be replaced while the rest of the values remain set to their default values as specified by the factory:

    $user = factory(App\User::class)->make([
        'name' => 'Abigail',
    ]);

<a name="persisting-models"></a>
### Persisting Models

The `create` method not only creates the model instances but also saves them to the database using Eloquent's `save` method:

    public function testDatabase()
    {
        // Create a single App\User instance...
        $user = factory(App\User::class)->create();

        // Create three App\User instances...
        $users = factory(App\User::class, 3)->create();

        // Use model in tests...
    }

You may override attributes on the model by passing an array to the `create` method:

    $user = factory(App\User::class)->create([
        'name' => 'Abigail',
    ]);

<a name="relationships"></a>
### Relationships

In this example, we'll attach a relation to some created models. When using the `create` method to create multiple models, an Eloquent [collection instance](/docs/{{version}}/eloquent-collections) is returned, allowing you to use any of the convenient functions provided by the collection, such as `each`:

    $users = factory(App\User::class, 3)
               ->create()
               ->each(function ($u) {
                    $u->posts()->save(factory(App\Post::class)->make());
                });

#### Relations & Attribute Closures

You may also attach relationships to models using Closure attributes in your factory definitions. For example, if you would like to create a new `User` instance when creating a `Post`, you may do the following:

    $factory->define(App\Post::class, function ($faker) {
        return [
            'title' => $faker->title,
            'content' => $faker->paragraph,
            'user_id' => function () {
                return factory(App\User::class)->create()->id;
            }
        ];
    });

These Closures also receive the evaluated attribute array of the factory that contains them:

    $factory->define(App\Post::class, function ($faker) {
        return [
            'title' => $faker->title,
            'content' => $faker->paragraph,
            'user_id' => function () {
                return factory(App\User::class)->create()->id;
            },
            'user_type' => function (array $post) {
                return App\User::find($post['user_id'])->type;
            }
        ];
    });

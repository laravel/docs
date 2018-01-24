# Database Testing

- [Introduction](#introduction)
- [Generating Factories](#generating-factories)
- [Resetting The Database After Each Test](#resetting-the-database-after-each-test)
- [Writing Factories](#writing-factories)
    - [Factory States](#factory-states)
- [Using Factories](#using-factories)
    - [Creating Models](#creating-models)
    - [Persisting Models](#persisting-models)
    - [Relationships](#relationships)
- [Available Assertions](#available-assertions)

<a name="introduction"></a>
## Introduction

Laravel provides a variety of helpful tools to make it easier to test your database driven applications. First, you may use the `assertDatabaseHas` helper to assert that data exists in the database matching a given set of criteria. For example, if you would like to verify that there is a record in the `users` table with the `email` value of `sally@example.com`, you can do the following:

    public function testDatabase()
    {
        // Make call to application...

        $this->assertDatabaseHas('users', [
            'email' => 'sally@example.com'
        ]);
    }

You can also use the `assertDatabaseMissing` helper to assert that data does not exist in the database.

Of course, the `assertDatabaseHas` method and other helpers like it are for convenience. You are free to use any of PHPUnit's built-in assertion methods to supplement your tests.

<a name="generating-factories"></a>
## Generating Factories

To create a factory, use the `make:factory` [Artisan command](/docs/{{version}}/artisan):

    php artisan make:factory PostFactory

The new factory will be placed in your `database/factories` directory.

The `--model` option may be used to indicate the name of the model created by the factory. This option will pre-fill the generated factory file with the given model:

    php artisan make:factory PostFactory --model=Post

<a name="resetting-the-database-after-each-test"></a>
## Resetting The Database After Each Test

It is often useful to reset your database after each test so that data from a previous test does not interfere with subsequent tests. The `RefreshDatabase` trait takes the most optimal approach to migrating your test database depending on if you are using an in-memory database or a traditional database. Use the trait on your test class and everything will be handled for you:

    <?php

    namespace Tests\Feature;

    use Tests\TestCase;
    use Illuminate\Foundation\Testing\RefreshDatabase;
    use Illuminate\Foundation\Testing\WithoutMiddleware;

    class ExampleTest extends TestCase
    {
        use RefreshDatabase;

        /**
         * A basic functional test example.
         *
         * @return void
         */
        public function testBasicExample()
        {
            $response = $this->get('/');

            // ...
        }
    }

<a name="writing-factories"></a>
## Writing Factories

When testing, you may need to insert a few records into your database before executing your test. Instead of manually specifying the value of each column when you create this test data, Laravel allows you to define a default set of attributes for each of your [Eloquent models](/docs/{{version}}/eloquent) using model factories. To get started, take a look at the `database/factories/UserFactory.php` file in your application. Out of the box, this file contains one factory definition:

    use Faker\Generator as Faker;

    $factory->define(App\User::class, function (Faker $faker) {
        return [
            'name' => $faker->name,
            'email' => $faker->unique()->safeEmail,
            'password' => '$2y$10$TKh8H1.PfQx37YgCzwiKb.KjNyWgaHb9cbcoQgdIVFlYg7B77UdFm', // secret
            'remember_token' => str_random(10),
        ];
    });

Within the Closure, which serves as the factory definition, you may return the default test values of all attributes on the model. The Closure will receive an instance of the [Faker](https://github.com/fzaninotto/Faker) PHP library, which allows you to conveniently generate various kinds of random data for testing.

You may also create additional factory files for each model for better organization. For example, you could create `UserFactory.php` and `CommentFactory.php` files within your `database/factories` directory. All of the files within the `factories` directory will automatically be loaded by Laravel.

<a name="factory-states"></a>
### Factory States

States allow you to define discrete modifications that can be applied to your model factories in any combination. For example, your `User` model might have a `delinquent` state that modifies one of its default attribute values. You may define your state transformations using the `state` method. For simple states, you may pass an array of attribute modifications:

    $factory->state(App\User::class, 'delinquent', [
        'account_status' => 'delinquent',
    ]);

If your state requires calculation or a `$faker` instance, you may use a Closure to calculate the state's attribute modifications:

    $factory->state(App\User::class, 'address', function ($faker) {
        return [
            'address' => $faker->address,
        ];
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

#### Applying States

You may also apply any of your [states](#factory-states) to the models. If you would like to apply multiple state transformations to the models, you should specify the name of each state you would like to apply:

    $users = factory(App\User::class, 5)->states('delinquent')->make();

    $users = factory(App\User::class, 5)->states('premium', 'delinquent')->make();

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

These Closures also receive the evaluated attribute array of the factory that defines them:

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

<a name="available-assertions"></a>
## Available Assertions

Laravel provides several database assertions for your [PHPUnit](https://phpunit.de/) tests:

Method  | Description
------------- | -------------
`$this->assertDatabaseHas($table, array $data);`  |  Assert that a table in the database contains the given data.
`$this->assertDatabaseMissing($table, array $data);`  |  Assert that a table in the database does not contain the given data.
`$this->assertSoftDeleted($table, array $data);`  |  Assert that the given record has been soft deleted.

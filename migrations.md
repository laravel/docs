# Migrations & Seeding

- [Introduction](#introduction)
- [Creating Migrations](#creating-migrations)
- [Running Migrations](#running-migrations)
- [Rolling Back Migrations](#rolling-back-migrations)
- [Database Seeding](#database-seeding)

<a name="introduction"></a>
## Introduction

Migrations are a type of version control for your database. They allow a team to modify the database schema and stay up to date on the current schema state. Migrations are typically paired with the [Schema Builder](/docs/{{version}}/schema) to easily manage your application's schema.

<a name="creating-migrations"></a>
## Creating Migrations

To create a migration, you may use the `make:migration` command on the Artisan CLI:

	php artisan make:migration create_users_table

The migration will be placed in your `database/migrations` folder, and will contain a timestamp which allows the framework to determine the order of the migrations.

The `--table` and `--create` options may also be used to indicate the name of the table, and whether the migration will be creating a new table:

	php artisan make:migration add_votes_to_users_table --table=users

	php artisan make:migration create_users_table --create=users

<a name="running-migrations"></a>
## Running Migrations

#### Running All Outstanding Migrations

	php artisan migrate

> **Note:** If you receive a "class not found" error when running migrations, try running the `composer dump-autoload` command.

### Forcing Migrations In Production

Some migration operations are destructive, meaning they may cause you to lose data. In order to protect you from running these commands against your production database, you will be prompted for confirmation before these commands are executed. To force the commands to run without a prompt, use the `--force` flag:

	php artisan migrate --force

<a name="rolling-back-migrations"></a>
## Rolling Back Migrations

#### Rollback The Last Migration Operation

	php artisan migrate:rollback

#### Rollback all migrations

	php artisan migrate:reset

#### Rollback all migrations and run them all again

	php artisan migrate:refresh

	php artisan migrate:refresh --seed

<a name="database-seeding"></a>
## Database Seeding

Laravel also includes a simple way to seed your database with test data using seed classes. All seed classes are stored in `database/seeds`. Seed classes may have any name you wish, but probably should follow some sensible convention, such as `UserTableSeeder`, etc. By default, a `DatabaseSeeder` class is defined for you. From this class, you may use the `call` method to run other seed classes, allowing you to control the seeding order.

#### Example Database Seed Class

	class DatabaseSeeder extends Seeder {

		public function run()
		{
			$this->call('UserTableSeeder');

			$this->command->info('User table seeded!');
		}

	}

	class UserTableSeeder extends Seeder {

		public function run()
		{
			DB::table('users')->delete();

			User::create(['email' => 'foo@bar.com']);
		}

	}

To seed your database, you may use the `db:seed` command on the Artisan CLI:

	php artisan db:seed

By default, the `db:seed` command runs the `DatabaseSeeder` class, which may be used to call other seed classes. However, you may use the `--class` option to specify a specific seeder class to run individually:

	php artisan db:seed --class=UserTableSeeder

You may also seed your database using the `migrate:refresh` command, which will also rollback and re-run all of your migrations:

	php artisan migrate:refresh --seed

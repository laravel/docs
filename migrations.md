# Migration & Seeding

- [Introduzione](#Introduzione)
- [Creare una Migration](#creare-migration)
- [Eseguire le Migration](#eseguire-migration)
- [Rollback delle Migration](#rollback-migration)
- [Database Seeding](#database-seeding)

<a name="Introduzione"></a>
## Introduzione

Le Migration possono essere definite come una sorta di version control per il tuo database. Permettono agevolmente ad un team di modificare lo schema del database e permettere a tutti di essere aggiornati sugli ultimi cambiamenti. Di solito, il sistema di Migration va a braccetto con lo [Schema Builder](/docs/master/schema).

<a name="creare-migration"></a>
## Creare una Migration

Per creare una migration, usa il comando `make:migration` di Artisan:

	php artisan make:migration create_users_table

La migration verrà messa nella cartella `database/migrations`, e conterrà nel nome un timestamp da usare come riferimento per la classificazione, a livello cronologico, delle migration stesse.

Se preferisci, specifica anche l'opzione `--path` per decidere dove mettere la migration. Il percorso in questione dovrebbe essere relativo alla root della tua installazione.

	php artisan make:migration foo --path=app/migrations

Le opzioni `--table` e `--create`, inoltre, possono essere usate per indicare il nome della tabella ed eventualmente anche se tale tabella verrà creata in tale migration:

	php artisan make:migration add_votes_to_user_table --table=users

	php artisan make:migration create_users_table --create=users

<a name="eseguire-migration"></a>
## Eseguire le Migration

#### Eseguire tutte le Migration

	php artisan migrate

> **Nota:** se dovessi ricevere un errore di tipo "class not found" prova ad eseguire il comando `composer dump-autoload` e ritentare.

### Forzare le Migration in Produzione

Alcune operazioni effettuate dalle migration possono essere distuttive, con la logica conseguenza di perdita di dati preziosi. Per proteggerti da problemi di questo genere, Artisan ti chiederà conferma prima di eseguire una o più migration in produzione. Se vuoi evitare il prompt in questione, invece, ti basterà usare il flag `--force`:

	php artisan migrate --force

Fallo, però, a tuo rischio e pericolo.

<a name="rollback-migration"></a>
## Rollback delle Migration

#### Effettuare il Rollback delle ultime Migration

	php artisan migrate:rollback

#### Rollback di Tutte le Migration

	php artisan migrate:reset

#### Rollback e Successiva Esecuzione di Tutte le Migration

	php artisan migrate:refresh

	php artisan migrate:refresh --seed

<a name="database-seeding"></a>
## Database Seeding

Laravel, oltre al sistema di Migration, include anche un comodo sistema di Seeding che permette di inserire agevolmente, in caso di bisogno, dei dati dummy nel database per effettuare dei test. Le classi "seed" possono essere chiamate come meglio si crede, ma è bene comunque seguire una certa nomenclatura (ad esempio `UserTableSeeder` e così via). Di default, Laravel possiede già una classe _DatabaseSeeder_ definita per lo scopo, che puoi usare per richiamare gli altri seeder.

#### Seeding di Esempio

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

			User::create(array('email' => 'foo@bar.com'));
		}

	}

Usa il comando `db:seed` per avviare la procedura:

	php artisan db:seed

Di default, il comando `db:seed` "esegue" la classe `DatabaseSeeder` che può essere, come abbiamo visto, usata per richiamare le altre. Nulla però ti vieta di usare il flag _--class_ per sceglierne una in particolare.

	php artisan db:seed --class=UserTableSeeder

Puoi anche eseguire le operazioni di seeding tramite _migrate:refresh_, aggiungendo l'opzione _--seed_.

	php artisan migrate:refresh --seed

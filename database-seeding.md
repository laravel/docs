# Database: Seeding

- [Introduzione](#introduzione)
- [Scrivere un Seeder](#scrivere-seeder)
	- [Usare le Model Factory](#usare-model-factory)
	- [Richiamare altri Seeder](#richiamare-altri-seeder)
- [Eseguire un Seeder](#eseguire-seeder)

<a name="introduzione"></a>
## Introduzione

Laravel, tramite il seeding, ti offre un semplice metodo per popolare velocemente il tuo database con dei dati di prova, magari da usare per i test. Tali classi, dette "Seeder", vengono generalmente piazzate in _database/seeds_. Puoi dare a queste classi il nome che preferisci, anche se è buona norma assegnare loro dei nomi significativi, come _UserTableSeeder_.

Da queste classi, inoltre, è possibile usare un metodo _call_ che permette di richiamare altre classi Seeder, permettendoti quindi di definire l'ordine e le modalità di seeding del tuo database in modo più strutturato.

<a name="scrivere-seeder"></a>
## Scrivere un Seeder

Vediamo come creare un seeder. Per prima cosa, usa il [comando Artisan](/docs/5.1/artisan) _make:seeder_ per generare un nuovo file usando questa sintassi.

	php artisan make:seeder UserTableSeeder

La classe seeder generata conterrà un metodo _run_, che verrà poi richiamato nel momento in cui l'utente eseguirà il comando Artisan _db:seed_. In questo metodo _run_ quindi dovrai inserire tutte le istruzioni di popolamento delle tabelle con i dati appropriati. Qui puoi usare quello che vuoi, dal [query builder](/docs/5.1/database-query-builder) alle [factory di model Eloquent](/docs/5.1/testing#model-factory).

Facciamo un esempio. Modifichiamo come segue la classe _DatabaseSeeder_ già inclusa in Laravel di default.

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

Fatto: adesso, quando eseguiremo le operazioni di seeding, nel database inseriremo un nuovo utente di prova.

<a name="usare-model-factory"></a>
### Usare le Model Factory

Specificare i singoli attributi per ogni record da inserire, a volte, può essere davvero scomodo. Immagina di dover popolare una tabella _posts_ con dei dati di esempio... anche un 50 post di prova, per iniziare. Immagina che lavoraccio!

Per fortuna, le [model factory](/docs/5.1/testing#model-factory) arrivano in tuo aiuto! Dopo averle definite adeguatamente, infatti, usarle nelle tue classi Seeder è davvero molto semplice.

Guarda questo esempio, in cui creiamo cinquanta utenti a cui associamo un post.

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

<a name="richiamare-altri-seeder"></a>
### Richiamare altri Seeder

Nella classe _DatabaseSeeder_, come già menzionato in precedenza, nulla ti vieta di richiamare il metodo _call_ per eseguire altri seeder. In questo modo puoi organizzare meglio tutto il tuo lavoro di seeding, specie se hai a che fare con procedure più complesse del solito.

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

<a name="eseguire-seeder"></a>
## Eseguire un Seeder

Una volta scritta la tua classe Seeder, eseguirla è davvero semplice. Tutto quello che devi fare è avviare il comando Artisan

	php artisan db:seed

che, di default, avvierà il seeder _DatabaseSeeder_. Nel caso in cui tu voglia richiamarne uno in particolare non devi fare altro che usare l'opzione _--class_, così:

	php artisan db:seed --class=UserTableSeeder

Puoi anche usare il flag _--seed_ del comando _migrate:refresh_ se vuoi effettuare il seeding subito dopo l'esecuzione delle migration. La scelta è tua!

	php artisan migrate:refresh --seed

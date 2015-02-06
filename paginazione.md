# Paginazione

- [Configurazione](#configurazione)
- [Uso](#uso)
- [Aggiungere I Link Di Paginazione](#aggiungere-link-paginazione)
- [Convertire In JSON](#convertire-in-json)

<a name="configurazione"></a>
## Configurazione

In altri framework, la paginazione può essere piuttosto noiosa. Laravel, invece, la rende “frizzante”! Laravel può generare un "range" intelligente di link basati sulla pagina corrente. L'HTML generato è compatibile con il framework CSS Bootstrap.

<a name="uso"></a>
## Uso

Ci sono una serie di modi per paginare degli elementi. Il più semplice è usare il metodo `paginate` sulla query builder o su un modello Eloquent.

#### Paginare I Risultati Del Database

	$users = DB::table('users')->paginate(15);

> **Nota:** Attualmente, l'operazione di paginazione che usano lo statement `groupBy` non possono essere eseguite efficientemente da Laravel. Se hai bisogno di usare `groupBy` con i risultati della paginazione, è raccomandato eseguire una query al database manualmente usando il metodo `Paginator::make`.

#### Paginare Un Model Eloquent

Puoi anche paginare i model [Eloquent](/eloquent):

	$allUsers = User::paginate(15);

	$someUsers = User::where('votes', '>', 100)->paginate(15);

Il parametro passato al metodo `paginate` è il numero di elementi da visualizzare per pagina. Una volta recuperati i risultati, puoi visualizzarli nella tua view, creando i link di paginazione con il metodo `render`:

	<div class="container">
		<?php foreach ($users as $user): ?>
			<?php echo $user->name; ?>
		<?php endforeach; ?>
	</div>

	<?php echo $users->render(); ?>

Questo è tutto quello da fare per creare un sistema di paginazione! Nota che non abbiamo bisogno di informare il framework sulla pagina corrente. Laravel lo determinerà per te, automaticamente. 

Puoi anche accedere ad alcune informazioni aggiuntive di paginazione usando i seguenti metodi:

- `currentPage`
- `lastPage`
- `perPage`
- `total`
- `count`

#### Paginazione Semplice

Se vuoi mostrare solo i link "Successivo" e "Precedente" nella tua view, hai a disposizione il metodo `simplePaginate` per eseguire una query più efficiente. Questo è utile in caso di numero considerevole di elementi da visualizzare e non si richiede di visualizzare l'esatto numero di pagine nella view:

	$someUsers = User::where('votes', '>', 100)->simplePaginate(15);

#### Creare Un Paginatore Manualemente

In alcuni casi puoi creare un istanza pagination manualmente, passando a tale istanza un array di elementi. Puoi farlo utilizzando un istanza di `Illuminate\Pagination\Paginator` oppure `Illuminate\Pagination\LengthAwarePaginator`, dipende dalle tue necessità.

#### Personalizzare Gli URL Paginator

Puoi anche personalizzare gli URL usando il paginator tramite il metodo `setPath`:

	$users = User::paginate();

	$users->setPath('custom/url');

Nell'esempio sopra verrano creati degli URL come il seguente: http://example.com/custom/url?page=2

<a name="aggiungere-link-paginazione"></a>
## Aggiungere I Link Di Paginazione

Puoi aggiungere query string ai tuoi link di paginazione usando il medoto `appends` di Paginator:

	<?php echo $users->appends(['sort' => 'votes'])->render(); ?>

Questo genererà URL di questo tipo:

	http://example.com/something?page=2&sort=votes

Se desideri aggiungere un “hash fragment” alle URL, puoi usare il metodo `fragment`:

	<?php echo $users->fragment('foo')->render(); ?>

Questo metodo genererà URL di questo tipo:

	http://example.com/something?page=2#foo

<a name="convertire-in-json"></a>
## Convertire In JSON

La classe `Paginator` implementa il contract `Illuminate\Contracts\Support\JsonableInterface` che contiene il metodo `toJson`. Puoi convertire un istanza `Paginator` in JSON ritornando il valore da una route. I dati JSON dell'istanza includeranno alcune "meta" informazioni come `total`, `current_page`, e `last_page`. I dati dell'istanza saranno accessibili nell'array JSON tramite la chiave `data`.

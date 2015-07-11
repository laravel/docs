# Laravel Cashier

- [Introduzione](#introduzione)
- [Abbonamenti](#abbonamenti)
	- [Creare Un Abbonamento](#creare-abbonamento)
	- [Controllare Lo Stato Di Un Abbonamento](#controllare-stato-abbonamento)
	- [Cambiare Abbonamento](#cambiare-abbonamento)
	- [Abbonamento Per Quantità](#abbonamento-per-quantita)
	- [Tasse Abbonamento](#tasse-abbonamento)
	- [Cancellare Un Abbonamento](#cancellare-abbonamento)
	- [Riattivare Un Abbonamento](#riattivare-abbonamento)
- [Gestire Webhook di Stripe](#gestire-webhook-stripe)
	- [Gestire I Pagamenti Falliti](#gestire-pagamenti-falliti)
	- [Gestire Altri Webhook](#gestire-altri-webhook)
- [Ricarica Singola](#ricarica-singola)
- [Fatture](#fatture)
	- [Generare Fatture In PDF](#generare-fatture-pdf)

<a name="introduzione"></a>
## Introduzione

Laravel Cashier fornisce una espressiva e fluente interfaccia per utilizzare il servizio di sottoscrizione e pagamento di [Stripe's](https://stripe.com) . Gestisce quasi tutto il codice necessario per la sottoscrizione di pagamenti. Oltre alla gestione base degli abbonamenti, Cashier può gestire facilmente coupon, cambi di piano, abbonamenti di "quantità", cancellazione, periodi di grazia e persino generare fatture in PDF.

<a name="configurazione"></a>
### Configurazione

#### Composer

Per prima cosa, aggiungi il package Cashier al tuo file `composer.json` ed esegui il comando `composer update`:

	"laravel/cashier": "~5.0" (For Stripe SDK ~2.0, and Stripe APIs on 2015-02-18 version and later)
	"laravel/cashier": "~4.0" (For Stripe APIs on 2015-02-18 version and later)
	"laravel/cashier": "~3.0" (For Stripe APIs up to and including 2015-02-16 version)

#### Service Provider

Successivamente, registra il [service provider](/docs/{{version}}/providers) `Laravel\Cashier\CashierServiceProvider`  nel tuo file di configurazione `app`.

#### Migration

Prima di usare Cashier, è necessario aggiungere alcune colonne al database. Non ti preoccupare, puoi usare il comando Artisan `cashier:table` che si occuperà di creare una migration per l'aggiunta delle colonne necessarie. Per esempio, per aggiungere la colonna alla tabella degli utenti puoi usare: `php artisan cashier:table users`.

Una volta creata la migration, puoi eseguire semplicemente il comando `migrate`.

#### Setup Del Model

Adesso, aggiungi il trait `Billable` e i necessari mutator per le date all'interno del tuo model:

	use Laravel\Cashier\Billable;
	use Laravel\Cashier\Contracts\Billable as BillableContract;

	class User extends Model implements BillableContract {

		use Billable;

		protected $dates = ['trial_ends_at', 'subscription_ends_at'];

	}

Aggiungendo le colonne nella proprietà `$dates` del model, indichiamo ad Eloquent di ritornare quelle colonne come istanze di Carbon / DateTime invece di stringhe grezze.

#### Stripe Key

Per finire, imposta la tua Stripe key nel file di configurazione `services.php`:

	'stripe' => [
		'model'  => 'User',
		'secret' => env('STRIPE_API_SECRET'),
	],

<a name="abbonamenti"></a>
## Abbonamenti

<a name="creare-abbonamento"></a>
### Creare Un Abbonamento

Per creaare un abbonamento, per prima cosa recupera l'istanza del tuo model, che tipicamente sarà un istanza di `App\User`. Una volta recuperata, puoi usare il metodo `subscription`per gestire l'abbonamento di un utente:

	$user = User::find(1);

	$user->subscription('monthly')->create($creditCardToken);

Il metodo `create`creera automaticamente l'abbonamento utilizzando Stripe, e si occuperà di aggiornare le informazioni nel database salvando l'ID cliente e altre informazioni utili per i pagamenti. Se il tuo piano di abbonamento ha un periodo di prova gratuita configurato nel tuo account Stripe verrà associata la data di scadenza della prova all'utente che hai registrato.

Se il tuo abbonamento ha un periodo di prova che non è configurato nel tuo account Stripe, allora dovrai assicurarti di creare e salvare la data di fine subito dopo la sottoscrizione dell'abbonamento:

	$user->trial_ends_at = Carbon::now()->addDays(14);

	$user->save();

#### Specificare Dettagli Aggiuntivi Per L'Utente

Se vuoi specificare dei dettagli aggiuntivi per gli utenti, puoi farlo passando questi dati come secondo parametro del metodo `create`:

	$user->subscription('monthly')->create($creditCardToken, [
		'email' => $email, 'description' => 'Our First Customer'
	]);

Per sapere di più sui campi addizionali supportati da Stripe dai una occhiata alla loro  [documentazione sulla creazione dei clienti](https://stripe.com/docs/api#create_customer).

#### Coupon

Se vuoi applicare un coupon quando viene creato un abbonamento, puoi usare il metodo `withCoupon`:

	$user->subscription('monthly')
	     ->withCoupon('code')
	     ->create($creditCardToken);

<a name="controllare-stato-abbonamento"></a>
### Controllare Lo Stato Di Un Abbonamento

Una volta che l'utente si è abbonato alla tua applicazione, puoi facilmente controllarne lo stato usando alcuni metodi convenienti. Per primo, il metodo `subscribed` ritorna `true` se l'utente ha un abbonamento attivo, anche se l'abbonamento è attualmente in un periodo di prova:

	if ($user->subscribed()) {
		//
	}

Il metodo `subscribed` è un ottimo candidato per le [middleware](/docs/{{version}}/middleware), permettendoti di filtrare l'accesso a route o controller basati sullo stato dell'abbonamento:

	public function handle($request, Closure $next)
	{
		if ($request->user() && ! $request->user()->subscribed()) {
			// This user is not a paying customer...
			return redirect('billing');
		}

		return $next($request);
	}

Se vuoi determinare se un utente è ancora in periodo di prova, puoi usare il metodo `onTrial`. Questo metodo può essere utile per visualizzare un messaggio che avvisa l'utente che si trova ancora nel periodo di prova:

	if ($user->onTrial()) {
		//
	}

Il metodo `onPlan` può essere utilizzato per determinare se un utente è abbonato ad un dato piano:

	if ($user->onPlan('monthly')) {
		//
	}

#### Stato di Cancellazione Abbonamento

Per verificare se un utente una volta era abbonato ma adesso ha cancellato la sua iscrizione puoi usare il metodo `cancelled`:

	if ($user->cancelled()) {
		//
	}

Puoi anche determinare se un utente ha cancellato il suo abbonamento, ma si trova ancora nel  "periodo di grazia" prima che l'abbonamento scada completamente. Per esempio, se un utente cancella il suo abbonamento il 5 Marzo ma la scadenza dell'abbonamento è prevista per il 10 Marzo, l'utente fino a quella data sarà in un "periodo di grazia" durante il quale potrà ancora accedere alla tua applicazione. Nota che il metodo `subscribed` ritorna sempre `true` durante questo periodo.

	if ($user->onGracePeriod()) {
		//
	}

Il metodo `everSubscribed` può essere usato per determinare se un utente è mai stato abbonato ad un piano della tua applicazione:

	if ($user->everSubscribed()) {
		//
	}

<a name="cambiare-abbonamento"></a>
### Cambiare Abbonamento

Dopo che un utente si è abbonato alla tua applicazione, potrebbero volere occasionalmente cambiare il loro abbonamento. Per cambiare l'abbonamento di utente, usa il metodo `swap`. Per sempio, puoi facilmente cambiare l'abbonamento in un abbonamento premium:

	$user = App\User::find(1);

	$user->subscription('premium')->swap();

Se l'utente è in un periodo di prova, questa verrà mantenuta fino alla scadenza. Se l'abbonamento è una "quantità" anche in questo caso verrà mantenuta. Quando si cambia piano, puoi usare il metodo `prorate` per indicare che la ricarica dovrà essere ripartita proporzionalmente . In aggiunta, puoi usare il metodo `swapAndInvoice` per fatturare immediatamente l'utente per il cambio di piano:

	$user->subscription('premium')
				->prorate()
				->swapAndInvoice();

<a name="abbonamento-per-quantita"></a>
### Abbonamento Per Quantità

Qualche volta gli abbonamenti sono affette da una "quantità". Per esempio, la tua applicazione potrebbe addebitare $10 al mese **per utente** ad account. Per icrementare e decrementare facilmetne queste quantità puoi usare i metodi `increment` e `decrement`:

	$user = User::find(1);

	$user->subscription()->increment();

	// Add five to the subscription's current quantity...
	$user->subscription()->increment(5);

	$user->subscription()->decrement();

	// Subtract five to the subscription's current quantity...
	$user->subscription()->decrement(5);

Per maggiori informazioni su abbonamenti per quantità, consulta la [documentazione Stripe](https://stripe.com/docs/guides/subscriptions#setting-quantities).

<a name="tasse-abbonamento"></a>
### Tasse Abbonamento

Con Cashier, è facile offrire un valore di `tax_percent` da inviare a Stripe. Per specificare la percentuale delle tasse che un untente paga su un abbonamento, implementa il metodo `getTaxPercent` nel tuo model, e ritorna un valore numerico tra 0 e 100, con non più di 2i cifre decimali.

	public function getTaxPercent() {
		return 20;
	}

Questo ti consente di applicare una tassa, che può essere utile per un bacino di utenza che si estende su più stati. 

<a name="cancellare-abbonamento"></a>
### Cancellare Un Abbonamento

Per cancellare un abbonamento, chiama semplicmente il metodo `cancel` sull'abbonamento dell'utente:

	$user->subscription()->cancel();

Quando un abbonamento è cancellato, Cashier imposterà automaticamente la colonna `subscription_ends_at` nel tuo database. Questa colonna è usata per sapere quando il metodo `subscribed` deve ritornare `false`. Per esempio, se un cliente cancella un abbonamento l'1 di Marzo, ma l'For example, if a customer cancels a subscription on March 1st, ma il suo abbonamento sarebbe dovuto finire il 5 Marzo, il metodo `subscribed` continuerà a ritornare `true` fino al 5 Marzo.

Per determinare se un utente ha cancellato il suo abbonamento ma si trova ancora nel suo "periodo di grazia" usa il metodo `onGracePeriod`:

	if ($user->onGracePeriod()) {
		//
	}

<a name="riattivare-abbonamento"></a>
### Riattivare Un Abbonamento

Se un utente ha cancellato il suo abbonamento e vuoi ri-attivarlo, usa il metodo `resume`:

	$user->subscription('monthly')->resume($creditCardToken);

Se un cliente ha cancellato il suo abbonamento, ma ha fatto richiesta di riattivarlo prima che l'abobnamento orginale scadesse non gli sarà addebitato subito il costo del nuovo abbonamento. Il suo abbonamento sarà semplicemente riattivato e il pagamento sarà automaticamente effettuato alla normale scadenza.

<a name="gestire-webhook-stripe"></a>
## Gestire Webhook di Stripe

<a name="gestire-pagamenti-falliti"></a>
### Gestire I Pagamenti Falliti

E se la carta di credito di un cliente scade? Nessun problema - Cashier include un Webhook controller che si occuperà automaticamente di cancellare l'abbonamento al tuo posto. Non devi far altro che far puntare una route al controller:

	Route::post('stripe/webhook', 'Laravel\Cashier\WebhookController@handleWebhook');

Tutto qui! Tutti i pagamenti che falliranno saranno catturati e gestiti dal controller. Il controller cancellerà l'abbonamento dopo 3 tentativi di pagamento falliti. Non dimenticarti: avrai bisogno di configurare l'URI di webhook nel pannello di controllo di Stripe.

Visto che lo webhook di Stripe ha bisogno di bypassare la  [verifica CSRF](/docs/{{version}}/routing#csrf-protection) di Laravel, assicurati di includere l'URI come eccezione nel middleware `VerifyCsrfToken`:

	protected $except = [
		'stripe/*',
	];

<a name="gestire-altri-webhook"></a>
### Gestire Altri Webhook

Se ci sono altri eventi Stripe che vuoi gestire, puoi estendere il Webhook controller. I nomi dei tuoi metodi dovranno rispettare le convenzioni di Cashier, in particolare, i metodi dovranno essere preceduti dalla parola `handle` e il nome del webhook Stripe in formato "camel case"che vuoi gestire. Per esempio, se vuoi gestire il webhook `invoice.payment_succeeded`, dovrai aggiungere al tuo controller il metodo `handleInvoicePaymentSucceeded`.

	<?php namespace App\Http\Controller;

	use Laravel\Cashier\WebhookController as BaseController;

	class WebhookController extends BaseController
	{
		/**
		 * Handle a stripe webhook.
		 *
		 * @param  array  $payload
		 * @return Response
		 */
		public function handleInvoicePaymentSucceeded($payload)
		{
			// Handle The Event
		}
	}

<a name="ricarica-singola"></a>
## Ricarica Singola

Se vuoi effettuare una ricarica "una tantum" sulla carta di credito del cliente abbonato, puoi usare il metodo `charge` sull'istanza dell'utente. Il metodo `charge` riceve come parametro l'ammontare che desideri caricare nel **minimo denominatore della valuta usata dalla tua applicazione**. Così, per esempio, nell'esempio sotto caricheremo 100 centesimi, o un euro, sulla carta di credito del cliente:

	$user->charge(100);

Il metodo `charge` accetta un arrai come suo secondo parametro, dandoti l'opportunità di passare qualsiasi opzione tu desideri sulla creazione della ricarica di Stripe:

	$user->charge(100, [
		'source' => $token,
		'receipt_email' => $user->email,
	]);

Il metodo `charge` ritornerà `false` se la ricarica fallisce. Questo solitamente indica che la ricarica non è permssa:

	if ( ! $user->charge(100)) {
		// The charge was denied...
	}

Se la ricarica avviene correttamente, verrà ritornata dal metodo la risposta completa di Stripe.

<a name="fatture"></a>
## Fatture
Puoi facilmente recuperare un array di tutte le fatture di un utente utilizzando il metodo `invoices`:

	$invoices = $user->invoices();

Quando mostri un elenco di fatture al cliente puoi utilizzare questi metodi per mostrare informazioni rilevanti. Per esempio, puoi mostrare le fatture in una tabella, permettendo all'utente di scaricarle facilmente:

	<table>
		@foreach ($invoices as $invoice)
			<tr>
				<td>{{ $invoice->dateString() }}</td>
				<td>{{ $invoice->dollars() }}</td>
				<td><a href="/user/invoice/{{ $invoice->id }}">Download</a></td>
			</tr>
		@endforeach
	</table>

<a name="generare-fatture-pdf"></a>
#### Generare Fatture In PDF

Da una route o controller, usa il metodo `downloadInvoice` per generare una fattura in formato PDF. Questo metodo genererà automaticamente un'appropriata risposta HTTP per eseguire il download del file:

	Route::get('user/invoice/{invoice}', function ($invoiceId) {
		return Auth::user()->downloadInvoice($invoiceId, [
			'vendor'  => 'Your Company',
			'product' => 'Your Product',
		]);
	});

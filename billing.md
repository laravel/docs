# Laravel Cashier

- [Introduzione](#introduzione)
- [Configurazione](#configurazione)
- [Abbonamento Ad Un Piano](#abbonamento-ad-un-piano)
- [Nessuna Carta Richiesta](#nessuna-carta-richiesta)
- [Cambiare Abbonamento](#cambiare-abbonamento)
- [Abbonamento Per Quantità](#abbonamento-per-quantita)
- [Cancellare Un Abbonamento](#cancellare-un-abbonamento)
- [Riattivare Un Abbonamento](#riattivare-un-abbonamento)
- [Controllare Lo Stato Di Un Abbonamento](#controllare-lo-stato-di-un-abbonamento)
- [Gestire I Pagamenti Falliti](#gestire-i-pagamenti-falliti)
- [Gestire Altri Webhook Di Pagamento](#gestire-altri-webhook-di-pagamento)
- [Fatture](#fatture)

<a name="introduzione"></a>
## Introduzione

Laravel Cashier fornisce una espressiva e fluente interfaccia per utilizzare il servizio di sottoscrizione e pagamento di [Stripe's](https://stripe.com). Gestisce quasi tutto il codice necessario per la sottoscrizione di pagamenti. Oltre alla gestione base degli abbonamenti, Cashier può gestire facilmente  coupon, cambi di piano, abbonamenti di "quantità", cancellazione, periodi di grazia e persino generare fatture in PDF.

<a name="configurazione"></a>
## Configurazione

#### Composer

Per prima cosa devi aggiungere il package Cashier al tuo file `composer.json`:

	"laravel/cashier": "~3.0"

#### Service Provider

Devi poi registrare il provider `Laravel\Cashier\CashierServiceProvider` nel file di configurazione `app`

#### Migration

Prima di utilizzare Cashier è necessario aggiungere alcune colonne al database. Non ti preoccupare, puoi usare il comando Artisan `cashier:table` che si occuperà di creare una migration per l'aggiunta delle colonne necessarie. Per esempio, per aggiungere la colonna alla tabella degli utenti puoi usare `php artisan cashier:table users`. Una volta che la migration è stata creata non devi far altro che eseguire il comando `migrate`.

#### Setup Del Model

Adesso, aggiungi il trait `Billable` e i necessari mutator per le date all'interno del tuo model:

	use Laravel\Cashier\Billable;
	use Laravel\Cashier\Contracts\Billable as BillableContract;

	class User extends Eloquent implements BillableContract {

		use Billable;

		protected $dates = ['trial_ends_at', 'subscription_ends_at'];

	}

#### Stripe Key

Per finire, imposta la tua Stripe key in uno dei file di bootstrap o in un service providers, come ad esempio il file `AppServiceProvider`:

	User::setStripeKey('stripe-key');

<a name="abbonamento-ad-un-piano"></a>
## Abbonamento Ad Un Piano

Una volta che hai una istanza del model, puoi facilmente abbonare l'utente al piano di pagamento scelto:

	$user = User::find(1);

	$user->subscription('monthly')->create($creditCardToken);

Se vuoi applicare un coupon quando crei una abbonamento lo puoi fare utilizzando il metodo `withCoupon`:

	$user->subscription('monthly')
	     ->withCoupon('code')
	     ->create($creditCardToken);

Il metodo `subscription` creerà in automatico un abbonamento utilizzando Stripe e si occuperà di aggiornare le informazioni nel database salvando l'ID cliente e altre informazioni utili per i pagamenti. Se il tuo piano di abbonamento ha un periodo di prova gratuita configurato nel tuo account Stripe verrà associata la data di scadenza della prova all'utente che hai registrato.

Se il tuo abbonamento ha un periodo di prova che **non** è configurato nel tuo account Stripe, allora dovrai assicurarti di creare e salvare la data di fine subito dopo la sottoscrizione dell'abbonamento.:

	$user->trial_ends_at = Carbon::now()->addDays(14);

	$user->save();

### Specificare Dettagli Aggiuntivi Per L'Utente

Se vuoi specificare alcuni dettagli aggiuntivi sul tuo cliente lo puoi fare passandoli come secondo parametro del metodo `create`:

	$user->subscription('monthly')->create($creditCardToken, [
		'email' => $email, 'description' => 'Our First Customer'
	]);

Per sapere di più sui campi addizionali supportati da Stripe dai una occhiata alla loro [documentazione sulla creazione dei clienti](https://stripe.com/docs/api#create_customer).

<a name="nessuna-carta-richiesta"></a>
## Nessuna Carta Richiesta

Se la tua applicazione offre un periodo di proa gratuito senza la richiesta iniziale dei dati della carta di credito, devi impostare la proprietà `cardUpFront` su `false` all'interno del tuo model:

	protected $cardUpFront = false;

Quando crei l'abbonamento, assicurati di impostare una data di scadenza:

	$user->trial_ends_at = Carbon::now()->addDays(14);

	$user->save();

<a name="cambiare-abbonamento"></a>
## Cambiare Abbonamento

Per cambiare l'abbonamento di un utente devi usare il metodo `swap`:

	$user->subscription('premium')->swap();

Se l'utente è in un periodo di prova, questa verrà mantenuta fino alla scadenza. Se l'abbonamento è una "quantità" anche in questo caso verrà mantenuta.

<a name="abbonamento-per-quantita"></a>
## Abbonamento Per Quantità

Qualche volta gli abbonamenti sono affette da una "quantità". Per esempio, la tua applicazione potrebbe addebitare $10 al mese per utente ad account. Per icrementare e decrementare facilmetne queste quantità puoi usare i metodi `increment` e `decrement`:

	$user = User::find(1);

	$user->subscription()->increment();

	// Aggiungi 5 alla quantità attuale dell'abbonamento
	$user->subscription()->increment(5);

	$user->subscription->decrement();

	// Sottrai 5 dalla quantità attuale dell'abbonamento
	$user->subscription()->decrement(5);

<a name="cancellare-un-abbonamento"></a>
## Cancellare Un Abbonamento

Cancellare un abbonamento è facile come fare una passeggiata al parco:

	$user->subscription()->cancel();

Quando un abbonamento viene cancellato, Cashier imposterà automaticamente una nuova data nella colonna `subscription_ends_at` del tuo database. Questa colonna viene usata per decidere se il metodo `subscribed` deve restituire `false`. Per esempio, se un cliente cancella il suo abbonamento il 2 Marzo, ma il suo abbonamento sarebbe dovuto finire il 5 Marzo, il metodo `subscribed` continuerà a restituire `true` fino al 5 Marzo.

<a name="riattivare-un-abbonamento"></a>
## Riattivare Un Abbonamento

Se un cliente ha cancellato il suo abbonamento e adesso devi riattivarlo puoi farlo usando il metodo `resume`:

	$user->subscription('monthly')->resume($creditCardToken);

Se un cliente ha cancellato il suo abbonamento, ma ha fatto richiesta di riattivarlo prima che l'abobnamento orginale scadesse non gli sarà addebitato subito il costo del nuovo abbonamento. Il suo abbonamento sarà semplicemente riattivato e il pagamento sarà automaticamente effettuato alla normale scadenza.

<a name="controllare-lo-stato-di-un-abbonamento"></a>
## Controllare Lo Stato Di Un Abbonamento

Per verificare se un utente è abbonato alla tua applicazione, utilizza il metodo `subscribed`:

	if ($user->subscribed())
	{
		//
	}

Il metodo `subscribed` è un ottimo candidato per le [route middleware](/docs/master/middleware):

	public function handle($request, Closure $next)
	{
		if ($request->user() && ! $request->user()->subscribed())
		{
			return redirect('billing');
		}

		return $next($request);
	}

Puoi anche controllare se un utente è ancora nel periodo trial (se lo hai previsto) utilizzando il metodo `onTrial`:

	if ($user->onTrial())
	{
		//
	}

Per verificare se un utente una volta era abbonato ma adesso ha cancellato la sua iscrizione puoi usare il metodo `cancelled`:

	if ($user->cancelled())
	{
		//
	}

Puoi anche controllare quali utenti hanno cancellato l'abbonamento ma sono ancora nel "periodo di grazia". Per esempio, se un utente cancella il suo abbonamento il 5 Marzo ma la scadenza dell'abbonamento è prevista per il 10 Marzo, l'utente fino a quella data sarà in un "periodo di grazia" durante il quale potrà ancora accedere alla tua applicazione. Nota che il metodo `subscribed` continuerà a restituire `true` fino alla data di scadenza.

	if ($user->onGracePeriod())
	{
		//
	}

Il metodo `everSubscribed` può essere utilizzato per determinare se un utente è mai stato abbonato ad un piano della tua applicazione:

	if ($user->everSubscribed())
	{
		//
	}

Il metodo `onPlan` può essere utilizzato per determinare se un utente è abbonato ad un dato piano:

	if ($user->onPlan('monthly'))
	{
		//
	}

<a name="gestire-i-pagamenti-falliti"></a>
## Gestire I Pagamenti Falliti

E se la carta di credito di un cliente scade? Nessun problema - Cashier include un Webhook controller che si occuperà automaticamente di cancellare l'abbonamento al tuo posto. Non devi far altro che far puntare una route al controller controller:

	Route::post('stripe/webhook', 'Laravel\Cashier\WebhookController@handleWebhook');

Tutto qui! Tutti i pagamenti che falliranno saranno catturati e gestiti dal controller. Il controller cancellerà l'abbonamento dopo 3 tentativi di pagamento falliti. L'URI `stripe/webhook` in questo caso è solo un esempio. Devi configurare un URI nelle impostazioni del tuo account Stripe.

<a name="gestire-altri-webhook-di-pagamento"></a>
## Gestire Altri Webhook Di Pagamento

Se ci sono altri eventi Stripe che vuoi gestire, puoi estendere il Webhook controller. I nomi dei tuoi metodi dovranno rispettare le convenzioni di Cashier, in particolare, i metodi dovranno essere preceduti dalla parola `handle` e poi il nome dell'webhook che intendi gestire. Per esempio, se vuoi gestire il webhook `invoice.payment_succeeded`, dovrai aggiungere al tuo controller il metodo `handleInvoicePaymentSucceeded`.

	class WebhookController extends Laravel\Cashier\WebhookController {

		public function handleInvoicePaymentSucceeded($payload)
		{
			// Gestisci l'evento
		}

	}

> **Nota:** Oltre ad aggiornare le informazioni degli abbonamenti nel tuo database, il Webhook controller cancellerà anche l'abbonamento tramite le Stripe API.

<a name="fatture"></a>
## Fatture

Puoi facilmente recuperare un array di tutte le fatture di un utente utilizzando il metodo `invoices`:

	$invoices = $user->invoices();

Quando mostri un elenco di fatture al cliente puoi utilizzare questi metodi per mostrare informazioni rilevanti:

	{{ $invoice->id }}

	{{ $invoice->dateString() }}

	{{ $invoice->dollars() }}

Puoi usare il metodo `downloadInvoice` per generare una fattura in PDF da scaricare. Si, è facilissimo creare le fatture:

	return $user->downloadInvoice($invoice->id, [
		'vendor'  => 'Your Company',
		'product' => 'Your Product',
	]);

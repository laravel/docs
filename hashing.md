# Hashing

- [Introduzione](#introduzione)
- [Uso Base](#uso-base)

<a name="introduzione"></a>
## Introduzione

La facade Laravel `Hash` offre un metodo sicuro Bcrypt di crittografia per memorizzare le password degli utenti. Se stai usando il controller `AuthController` incluso nella tua applicazione Laravel, si prenderà cura di eseguire l'hash della password con Bcrypt contro la versione non crittografata fornita dall'utente. 

Allo stesso modo, il servizio `Registrar` fornito con Laravel permette in maniera opportuna di memorizzare la password crittografata.

<a name="uso-base"></a>
## Uso Base

#### Hash Di Una Password Usando Bcrypt

	$password = Hash::make('secret');

Puoi anche usare la funzione helper `bcrypt`:

	$password = bcrypt('secret');

#### Verifica Di Una Password Tramite Il Metodo Check

	if (Hash::check('secret', $hashedPassword))
	{
		// The passwords match...
	}

#### Verifica Dell’Eventuale Necessità Di Re-Hash Di Una Password

	if (Hash::needsRehash($hashed))
	{
		$hashed = Hash::make('secret');
	}

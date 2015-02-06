# Encryption

- [Introduzione](#introduzione)
- [Utilizzo Base](#utilizzo-base)

<a name="introduzione"></a>
## Introduzione

Laravel fornisce sevizi per criptare utilizzando l'algoritmo AES tramite l'estensione Mcrypt di PHP.

<a name="utilizzo-base"></a>
## Utilizzo Base

#### Criptare Un Valore

	$encrypted = Crypt::encrypt('secret');

> **Nota:** Assicurati di impostare una stringa da 16, 24, o 32 caratteri nel campo `key` del file `config/app.php`. Altrimenti i valori criptati non saranno sicuri.

#### Decriptare Un Valore

	$decrypted = Crypt::decrypt($encryptedValue);

#### Imposta Il Cifrario e il Modo

Puoi impostare il cifrario e la modalità da utilizzare per criptare:

	Crypt::setMode('ctr');

	Crypt::setCipher($cipher);

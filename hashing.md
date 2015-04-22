# Hashing

- [Introdução](#introduction)
- [Uso básico](#basic-usage)

<a name="introducao"></a>
## Introdução

O facade `Hash` do Laravel, fornece um seguro hash Bcrypt para armazenar senhas de usuários. Se você estiver usando o controller `AuthController` que está incluso na sua aplicação Laravel, ele será responsável por verificar as senhas Bcrypt contra as versões un-hashed fornecidas pelo usuário.

Da mesma forma, o serviço `Registrar` que vem com o Laravel faz uma chamada apropriada da função `bcrypt` para senhas armazenadas.

<a name="basic-usage"></a>
## Uso básico

#### Criando um Hash usando Bcrypt

	$password = Hash::make('secret');

Você também pode usar a função helper `bcrypt`;

	$password = bcrypt('secret');

#### Verificando uma senha contra um Hash

	if (Hash::check('secret', $hashedPassword))
	{
		// As senhas conincidem...
	}

#### Verificando se precisa criar um Hash para a senha

	if (Hash::needsRehash($hashed))
	{
		$hashed = Hash::make('secret');
	}

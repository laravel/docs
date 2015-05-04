# Hashing

- [Introduction](#introduction)
- [Basic Usage](#basic-usage)

<a name="introduction"></a>
## Introduction

The Laravel `Hash` facade provides secure Bcrypt hashing for storing user passwords. If you are using the `AuthController` controller that is included with your Laravel application, it will be take care of verifying the Bcrypt password against the un-hashed version provided by the user.

Likewise, the user `Registrar` service that ships with Laravel makes the proper `bcrypt` function call to hash stored passwords.

<a name="basic-usage"></a>
## Basic Usage

#### Hashing A Password Using Bcrypt

	$password = Hash::make('plain-text');

You may also use the `bcrypt` helper function:

	$password = bcrypt('plain-text');

#### Verifying A Password Against A Hash

	if (Hash::check('plain-text', $hashedPassword))
	{
		// The passwords match...
	}

#### Checking If A Password Needs To Be Rehashed

	if (Hash::needsRehash($hashed))
	{
		$hashed = Hash::make('plain-text');
	}

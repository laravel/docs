# Hashing

- [Introduction](#introduction)
- [Basic Usage](#basic-usage)

<a name="introduction"></a>
## Introduction

The Laravel `Hash` [facade](/docs/{{version}}/facades) provides secure Bcrypt hashing for storing user passwords. If you are using the `AuthController` controller that is included with your Laravel application, it will automatically use Bcrypt for registration and authentication.

Bcrypt is a great choice for hashing passwords because its "work factor" is adjustable, which means that the time it takes to generate a hash can be increased as hardware power increases.

<a name="basic-usage"></a>
## Basic Usage

You may hash a password by calling the `make` method on the `Hash` facade:

    <?php

    namespace App\Http\Controllers;

    use Hash;
    use App\User;
    use Illuminate\Http\Request;
    use App\Http\Controllers\Controller;

    class UserController extends Controller
    {
        /**
         * Update the password for the user.
         *
         * @param  Request  $request
         * @param  int  $id
         * @return Response
         */
        public function updatePassword(Request $request, $id)
        {
            $user = User::findOrFail($id);

            // Validate the new password length...

            $user->fill([
                'password' => Hash::make($request->newPassword)
            ])->save();
        }
    }

Alternatively, you may also use the global `bcrypt` helper function:

    bcrypt('plain-text');

#### Verifying A Password Against A Hash

The `check` method allows you to verify that a given plain-text string corresponds to a given hash. However, if you are using the `AuthController` [included with Laravel](/docs/{{version}}/authentication), you will probably not need to use this directly, as the included authentication controller automatically calls this method:

    if (Hash::check('plain-text', $hashedPassword)) {
        // The passwords match...
    }

#### Checking If A Password Needs To Be Rehashed

The `needsRehash` function allows you to determine if the work factor used by the hasher has changed since the password was hashed:

    if (Hash::needsRehash($hashed)) {
        $hashed = Hash::make('plain-text');
    }

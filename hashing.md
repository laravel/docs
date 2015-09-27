# 雜湊

- [簡介](#introduction)
- [基本用法](#basic-usage)

<a name="introduction"></a>
## 簡介

Laravel 透過 `Hash` [facade](/docs/{{version}}/facades) 提供 Bcrypt 加密來保存使用者密碼。如果你在目前的應用當中使用 `AuthController` 控制器，它將自動使用 Bcrypt 加密進行註冊跟驗證。

由於 Bcrypt 的 「加密係數（word fator）」可以任意調整，使它成為最好的加密選擇。這代表每一次加密的時間可以隨著硬體設備的升級而加長。

<a name="basic-usage"></a>
## 基本用法

你可以透過呼叫 `Hash` facade 的 `make` 方法加密一個密碼：

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

另外，你也可以使用 `bcrypt` 輔助方法：

    bcrypt('plain-text');

#### 根據雜湊值驗證密碼

`check` 方法允許你透過一個給定的純字串跟雜湊值進行驗證。如果你目前正使用 [Laravel 內含的](/docs/{{version}}/authentication) `AuthController`，你可能不需要直接使用該方法，它已經包含在控制器當中並且自動呼叫。

    if (Hash::check('plain-text', $hashedPassword)) {
        // The passwords match...
    }

#### 驗證密碼是否須重新加密

`needsRehash` 函式允許你檢查已加密密碼，它所使用的加密係數是否被變更：

    if (Hash::needsRehash($hashed)) {
        $hashed = Hash::make('plain-text');
    }

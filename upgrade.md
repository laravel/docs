# Upgrade Guide

- [Upgrading To 13.0 From 12.x](#upgrade-13.0)

<a name="high-impact-changes"></a>
## High Impact Changes

<div class="content-list" markdown="1">

- TBD

</div>

<a name="medium-impact-changes"></a>
## Medium Impact Changes

<div class="content-list" markdown="1">

- [Authentication Contracts](#authentication-contracts)
</div>

<a name="low-impact-changes"></a>
## Low Impact Changes

<div class="content-list" markdown="1">
- TBD
</div>

<a name="upgrade-13.0"></a>
## Upgrading To 13.0 From 12.x

#### Estimated Upgrade Time: TBD

> [!NOTE]
> We attempt to document every possible breaking change. Since some of these breaking changes are in obscure parts of the framework only a portion of these changes may actually affect your application. Want to save time? You can use [Laravel Shift](https://laravelshift.com/) to help automate your application upgrades.

<a name="updating-dependencies"></a>
### Updating Dependencies

**Likelihood Of Impact: High**

You should update the following dependencies in your application's `composer.json` file:

<div class="content-list" markdown="1">

- TBD

</div>

<a name="carbon-3"></a>

<a name="authentication-contracts"></a>
### Authentication Contracts

**Likelihood Of Impact: Medium**

The `Authenticatable` and `UserProvider` contracts have been decomposed into smaller, focused interfaces following the Interface Segregation Principle. The original contracts are now deprecated and will be removed in a future version.

#### User Identity Contracts

The `Authenticatable` contract has been replaced with:

| New Contract | Purpose |
| --- | --- |
| `Illuminate\Contracts\Auth\Identity\Identifiable` | Core identification methods |
| `Illuminate\Contracts\Auth\Identity\HasPassword` | Password authentication methods |
| `Illuminate\Contracts\Auth\Identity\Rememberable` | "Remember me" token methods |
| `Illuminate\Contracts\Auth\Identity\StatefulIdentifiable` | Combines all three |

If your application implements `Authenticatable`, update to `StatefulIdentifiable`:

```php
use Illuminate\Contracts\Auth\Authenticatable; // [tl! remove]
use Illuminate\Contracts\Auth\Identity\StatefulIdentifiable; // [tl! add]
```

#### User Provider Contracts

The `UserProvider` contract has been replaced with:

| New Contract | Purpose |
| --- | --- |
| `Illuminate\Contracts\Auth\Providers\BasicUserProvider` | Retrieval by ID |
| `Illuminate\Contracts\Auth\Providers\CredentialsUserProvider` | Credential validation |
| `Illuminate\Contracts\Auth\Providers\RecallerUserProvider` | "Remember me" token handling |
| `Illuminate\Contracts\Auth\Providers\StatefulUserProvider` | Combines all three |

If your application implements `UserProvider`, update to `StatefulUserProvider`:

```php
use Illuminate\Contracts\Auth\UserProvider; // [tl! remove]
use Illuminate\Contracts\Auth\Providers\StatefulUserProvider; // [tl! add]
```

#### Custom Guards

If you have implemented a custom guard, the `Guard` contract's `setUser` method signature has changed from `Authenticatable` to `Identifiable`:

```php
// Before
public function setUser(Authenticatable $user);

// After
public function setUser(Identifiable $user);
```

Similarly, the `StatefulGuard` contract's `login` method now requires `StatefulIdentifiable`:

```php
// Before
public function login(Authenticatable $user, $remember = false);

// After
public function login(StatefulIdentifiable $user, $remember = false);
```

#### Custom User Providers

If you have implemented a custom user provider, the method signatures have changed to use `Identifiable` instead of `Authenticatable`:

```php
// Before
public function updateRememberToken(Authenticatable $user, $token);
public function validateCredentials(Authenticatable $user, array $credentials);
public function rehashPasswordIfRequired(Authenticatable $user, array $credentials, bool $force = false);

// After
public function updateRememberToken(Identifiable $user, $token);
public function validateCredentials(Identifiable $user, array $credentials);
public function rehashPasswordIfRequired(Identifiable $user, array $credentials, bool $force = false);
```

> [!WARNING]
> Since provider methods now accept the base `Identifiable` type, your custom implementations must verify the user implements the required sub-interface before calling interface-specific methods. Use intersection types whenever possible:
> ```php
> public function validateCredentials(Identifiable&HasPassword $user, array $credentials)
> {
>     // Now safe to call $user->getAuthPassword()
> }
> ```

> [!NOTE]
> The deprecated `Authenticatable` and `UserProvider` contracts extend their new counterparts. However, custom guard and provider implementations must update their method signatures to match the new contracts.
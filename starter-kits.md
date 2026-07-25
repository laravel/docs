---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Стартові набори

- [Вступ](#introduction)
- [Створення застосунку за допомогою стартового набору](#creating-an-application)
- [Доступні стартові набори](#available-starter-kits)
    - [React](#react)
    - [Svelte](#svelte)
    - [Vue](#vue)
    - [Livewire](#livewire)
- [Налаштування стартового набору](#starter-kit-customization)
    - [React](#react-customization)
    - [Svelte](#svelte-customization)
    - [Vue](#vue-customization)
    - [Livewire](#livewire-customization)
- [Автентифікація](#authentication)
    - [Увімкнення та вимкнення можливостей](#enabling-and-disabling-features)
    - [Налаштування створення користувача та скидання пароля](#customizing-actions)
    - [Двофакторна автентифікація](#two-factor-authentication)
    - [Обмеження частоти](#rate-limiting)
- [Команди](#teams)
- [Автентифікація через WorkOS AuthKit](#workos)
- [Inertia SSR](#inertia-ssr)
- [Стартові набори від спільноти](#community-maintained-starter-kits)
- [Часті запитання](#faqs)

<a name="introduction"></a>
## Вступ

Щоб дати вам фору в розробці нового застосунку Laravel, ми з радістю пропонуємо [стартові набори застосунків](https://laravel.com/starter-kits). Ці набори дають фору в створенні вашого наступного застосунку Laravel і містять маршрути, контролери та представлення, потрібні для реєстрації та автентифікації користувачів. Для автентифікації стартові набори використовують [Laravel Fortify](/docs/{{version}}/fortify).

Хоча ви можете вільно користуватися цими наборами, вони не обов'язкові. Ви можете створити власний застосунок з нуля, просто встановивши свіжу копію Laravel. Хай там як, ми знаємо, що ви створите щось чудове!

<a name="creating-an-application"></a>
## Створення застосунку за допомогою стартового набору

Щоб створити новий застосунок Laravel за допомогою одного з наших стартових наборів, спершу [встановіть PHP та CLI-інструмент Laravel](/docs/{{version}}/installation#installing-php). Якщо PHP і Composer уже встановлені, ви можете встановити CLI-інструмент інсталятора Laravel через Composer:

```shell
composer global require laravel/installer
```

Далі створіть новий застосунок Laravel за допомогою CLI інсталятора Laravel. Інсталятор запропонує обрати бажаний стартовий набір:

```shell
laravel new my-app
```

Після створення застосунку Laravel вам залишиться лише встановити фронтенд-залежності через NPM і запустити сервер розробки Laravel:

```shell
cd my-app
npm install && npm run build
composer run dev
```

Щойно ви запустите сервер розробки Laravel, ваш застосунок буде доступний у браузері за адресою [http://localhost:8000](http://localhost:8000).

<a name="available-starter-kits"></a>
## Доступні стартові набори

<a name="react"></a>
### React

Наш стартовий набір React дає надійну сучасну відправну точку для створення застосунків Laravel із фронтендом на React за допомогою [Inertia](https://inertiajs.com).

Inertia дозволяє створювати сучасні односторінкові застосунки на React, використовуючи класичну серверну маршрутизацію та контролери. Це дає змогу поєднати потужність React на фронтенді з неймовірною продуктивністю Laravel на бекенді та блискавичною компіляцією Vite.

Стартовий набір React використовує React 19, TypeScript, Tailwind і бібліотеку компонентів [shadcn/ui](https://ui.shadcn.com).

<a name="svelte"></a>
### Svelte

Наш стартовий набір Svelte дає надійну сучасну відправну точку для створення застосунків Laravel із фронтендом на Svelte за допомогою [Inertia](https://inertiajs.com).

Inertia дозволяє створювати сучасні односторінкові застосунки на Svelte, використовуючи класичну серверну маршрутизацію та контролери. Це дає змогу поєднати потужність Svelte на фронтенді з неймовірною продуктивністю Laravel на бекенді та блискавичною компіляцією Vite.

Стартовий набір Svelte використовує Svelte 5, TypeScript, Tailwind і бібліотеку компонентів [shadcn-svelte](https://www.shadcn-svelte.com/).

<a name="vue"></a>
### Vue

Наш стартовий набір Vue дає чудову відправну точку для створення застосунків Laravel із фронтендом на Vue за допомогою [Inertia](https://inertiajs.com).

Inertia дозволяє створювати сучасні односторінкові застосунки на Vue, використовуючи класичну серверну маршрутизацію та контролери. Це дає змогу поєднати потужність Vue на фронтенді з неймовірною продуктивністю Laravel на бекенді та блискавичною компіляцією Vite.

Стартовий набір Vue використовує Vue Composition API, TypeScript, Tailwind і бібліотеку компонентів [shadcn-vue](https://www.shadcn-vue.com/).

<a name="livewire"></a>
### Livewire

Наш стартовий набір Livewire дає ідеальну відправну точку для створення застосунків Laravel із фронтендом на [Laravel Livewire](https://livewire.laravel.com).

Livewire - це потужний спосіб створювати динамічні реактивні інтерфейси, використовуючи лише PHP. Він чудово підходить командам, які здебільшого працюють із шаблонами Blade і шукають простішу альтернативу SPA-фреймворкам на JavaScript, як-от React, Svelte і Vue.

Стартовий набір Livewire використовує Livewire, Tailwind і бібліотеку компонентів [Flux UI](https://fluxui.dev).

<a name="starter-kit-customization"></a>
## Налаштування стартового набору

<a name="react-customization"></a>
### React

Наш стартовий набір React побудований на Inertia 3, React 19, Tailwind 4 і [shadcn/ui](https://ui.shadcn.com). Як і в усіх наших наборах, увесь код бекенду та фронтенду міститься у вашому застосунку, що дозволяє повністю його налаштувати.

Більшість коду фронтенду розташована в каталозі `resources/js`. Ви вільні змінювати будь-який код, щоб налаштувати вигляд і поведінку свого застосунку:

```text
resources/js/
├── components/    # Reusable React components
├── hooks/         # React hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```

Щоб опублікувати додаткові компоненти shadcn, спершу [знайдіть потрібний компонент](https://ui.shadcn.com). Далі опублікуйте його за допомогою `npx`:

```shell
npx shadcn@latest add switch
```

У цьому прикладі команда опублікує компонент Switch у `resources/js/components/ui/switch.tsx`. Щойно компонент опубліковано, ви можете використовувати його на будь-якій зі своїх сторінок:

```jsx
import { Switch } from "@/components/ui/switch"

const MyPage = () => {
  return (
    <div>
      <Switch />
    </div>
  );
};

export default MyPage;
```

<a name="react-available-layouts"></a>
#### Доступні макети

Стартовий набір React містить два основні макети на вибір: макет із бічною панеллю («sidebar») і макет із шапкою («header»). За замовчуванням використовується макет із бічною панеллю, але ви можете перемкнутися на макет із шапкою, змінивши макет, що імпортується на початку файлу `resources/js/layouts/app-layout.tsx` вашого застосунку:

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```

<a name="react-sidebar-variants"></a>
#### Варіанти бічної панелі

Макет із бічною панеллю має три варіанти: типовий, «inset» і «floating». Ви можете обрати той, що подобається найбільше, змінивши компонент `resources/js/components/app-sidebar.tsx`:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="react-authentication-page-layout-variants"></a>
#### Варіанти макета сторінок автентифікації

Сторінки автентифікації, що входять до стартового набору React, - як-от сторінки входу та реєстрації, - також мають три варіанти макета: «simple», «card» і «split».

Щоб змінити макет автентифікації, змініть макет, що імпортується на початку файлу `resources/js/layouts/auth-layout.tsx` вашого застосунку:

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```

<a name="svelte-customization"></a>
### Svelte

Наш стартовий набір Svelte побудований на Inertia 3, Svelte 5, Tailwind і [shadcn-svelte](https://www.shadcn-svelte.com/). Як і в усіх наших наборах, увесь код бекенду та фронтенду міститься у вашому застосунку, що дозволяє повністю його налаштувати.

Більшість коду фронтенду розташована в каталозі `resources/js`. Ви вільні змінювати будь-який код, щоб налаштувати вигляд і поведінку свого застосунку:

```text
resources/js/
├── components/    # Reusable Svelte components
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration and Svelte rune modules
├── pages/         # Page components
└── types/         # TypeScript definitions
```

Щоб опублікувати додаткові компоненти shadcn-svelte, спершу [знайдіть потрібний компонент](https://www.shadcn-svelte.com). Далі опублікуйте його за допомогою `npx`:

```shell
npx shadcn-svelte@latest add switch
```

У цьому прикладі команда опублікує компонент Switch у `resources/js/components/ui/switch/switch.svelte`. Щойно компонент опубліковано, ви можете використовувати його на будь-якій зі своїх сторінок:

```svelte
<script lang="ts">
    import { Switch } from '@/components/ui/switch'
</script>

<div>
    <Switch />
</div>
```

<a name="svelte-available-layouts"></a>
#### Доступні макети

Стартовий набір Svelte містить два основні макети на вибір: макет із бічною панеллю («sidebar») і макет із шапкою («header»). За замовчуванням використовується макет із бічною панеллю, але ви можете перемкнутися на макет із шапкою, змінивши макет, що імпортується на початку файлу `resources/js/layouts/AppLayout.svelte` вашого застосунку:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.svelte'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.svelte'; // [tl! add]
```

<a name="svelte-sidebar-variants"></a>
#### Варіанти бічної панелі

Макет із бічною панеллю має три варіанти: типовий, «inset» і «floating». Ви можете обрати той, що подобається найбільше, змінивши компонент `resources/js/components/AppSidebar.svelte`:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="svelte-authentication-page-layout-variants"></a>
#### Варіанти макета сторінок автентифікації

Сторінки автентифікації, що входять до стартового набору Svelte, - як-от сторінки входу та реєстрації, - також мають три варіанти макета: «simple», «card» і «split».

Щоб змінити макет автентифікації, змініть макет, що імпортується на початку файлу `resources/js/layouts/AuthLayout.svelte` вашого застосунку:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.svelte'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.svelte'; // [tl! add]
```

<a name="vue-customization"></a>
### Vue

Наш стартовий набір Vue побудований на Inertia 3, Vue 3 Composition API, Tailwind і [shadcn-vue](https://www.shadcn-vue.com/). Як і в усіх наших наборах, увесь код бекенду та фронтенду міститься у вашому застосунку, що дозволяє повністю його налаштувати.

Більшість коду фронтенду розташована в каталозі `resources/js`. Ви вільні змінювати будь-який код, щоб налаштувати вигляд і поведінку свого застосунку:

```text
resources/js/
├── components/    # Reusable Vue components
├── composables/   # Vue composables / hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```

Щоб опублікувати додаткові компоненти shadcn-vue, спершу [знайдіть потрібний компонент](https://www.shadcn-vue.com). Далі опублікуйте його за допомогою `npx`:

```shell
npx shadcn-vue@latest add switch
```

У цьому прикладі команда опублікує компонент Switch у `resources/js/components/ui/Switch.vue`. Щойно компонент опубліковано, ви можете використовувати його на будь-якій зі своїх сторінок:

```vue
<script setup lang="ts">
import { Switch } from '@/components/ui/switch'
</script>

<template>
    <div>
        <Switch />
    </div>
</template>
```

<a name="vue-available-layouts"></a>
#### Доступні макети

Стартовий набір Vue містить два основні макети на вибір: макет із бічною панеллю («sidebar») і макет із шапкою («header»). За замовчуванням використовується макет із бічною панеллю, але ви можете перемкнутися на макет із шапкою, змінивши макет, що імпортується на початку файлу `resources/js/layouts/AppLayout.vue` вашого застосунку:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```

<a name="vue-sidebar-variants"></a>
#### Варіанти бічної панелі

Макет із бічною панеллю має три варіанти: типовий, «inset» і «floating». Ви можете обрати той, що подобається найбільше, змінивши компонент `resources/js/components/AppSidebar.vue`:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```

<a name="vue-authentication-page-layout-variants"></a>
#### Варіанти макета сторінок автентифікації

Сторінки автентифікації, що входять до стартового набору Vue, - як-от сторінки входу та реєстрації, - також мають три варіанти макета: «simple», «card» і «split».

Щоб змінити макет автентифікації, змініть макет, що імпортується на початку файлу `resources/js/layouts/AuthLayout.vue` вашого застосунку:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```

<a name="livewire-customization"></a>
### Livewire

Наш стартовий набір Livewire побудований на Livewire 4, Tailwind і [Flux UI](https://fluxui.dev/). Як і в усіх наших наборах, увесь код бекенду та фронтенду міститься у вашому застосунку, що дозволяє повністю його налаштувати.

Більшість коду фронтенду розташована в каталозі `resources/views`. Ви вільні змінювати будь-який код, щоб налаштувати вигляд і поведінку свого застосунку:

```text
resources/views
├── components            # Reusable components
├── flux                  # Customized Flux components
├── layouts               # Application layouts
├── pages                 # Livewire pages
├── partials              # Reusable Blade partials
├── dashboard.blade.php   # Authenticated user dashboard
├── welcome.blade.php     # Guest user welcome page
```

<a name="livewire-available-layouts"></a>
#### Доступні макети

Стартовий набір Livewire містить два основні макети на вибір: макет із бічною панеллю («sidebar») і макет із шапкою («header»). За замовчуванням використовується макет із бічною панеллю, але ви можете перемкнутися на макет із шапкою, змінивши макет, який використовує файл `resources/views/layouts/app.blade.php` вашого застосунку. Крім того, вам слід додати атрибут `container` до головного компонента Flux:

```blade
<x-layouts::app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts::app.header>
```

<a name="livewire-authentication-page-layout-variants"></a>
#### Варіанти макета сторінок автентифікації

Сторінки автентифікації, що входять до стартового набору Livewire, - як-от сторінки входу та реєстрації, - також мають три варіанти макета: «simple», «card» і «split».

Щоб змінити макет автентифікації, змініть макет, який використовує файл `resources/views/layouts/auth.blade.php` вашого застосунку:

```blade
<x-layouts::auth.split>
    {{ $slot }}
</x-layouts::auth.split>
```

<a name="authentication"></a>
## Автентифікація

Усі стартові набори використовують [Laravel Fortify](/docs/{{version}}/fortify) для обробки автентифікації. Fortify надає маршрути, контролери та логіку для входу, реєстрації, скидання пароля, підтвердження електронної пошти тощо.

Fortify автоматично реєструє наведені нижче маршрути автентифікації залежно від того, які можливості увімкнено у вашому конфігураційному файлі `config/fortify.php`:

<div class="overflow-auto">

| Маршрут                            | Метод  | Опис                                    |
| ---------------------------------- | ------ | --------------------------------------- |
| `/login`                           | `GET`    | Показати форму входу                  |
| `/login`                           | `POST`   | Автентифікувати користувача           |
| `/logout`                          | `POST`   | Вийти з облікового запису             |
| `/register`                        | `GET`    | Показати форму реєстрації             |
| `/register`                        | `POST`   | Створити нового користувача           |
| `/forgot-password`                 | `GET`    | Показати форму запиту скидання пароля |
| `/forgot-password`                 | `POST`   | Надіслати посилання для скидання      |
| `/reset-password/{token}`          | `GET`    | Показати форму скидання пароля        |
| `/reset-password`                  | `POST`   | Оновити пароль                        |
| `/email/verify`                    | `GET`    | Показати повідомлення про підтвердження |
| `/email/verify/{id}/{hash}`        | `GET`    | Підтвердити адресу електронної пошти  |
| `/email/verification-notification` | `POST`   | Надіслати лист підтвердження ще раз   |
| `/user/confirm-password`           | `GET`    | Показати форму підтвердження пароля   |
| `/user/confirm-password`           | `POST`   | Підтвердити пароль                    |
| `/two-factor-challenge`            | `GET`    | Показати форму перевірки 2FA          |
| `/two-factor-challenge`            | `POST`   | Перевірити код 2FA                    |

</div>

Команда Artisan `php artisan route:list` дозволяє переглянути всі маршрути вашого застосунку.

<a name="enabling-and-disabling-features"></a>
### Увімкнення та вимкнення можливостей

Ви можете керувати тим, які можливості Fortify увімкнено, у конфігураційному файлі `config/fortify.php` вашого застосунку:

```php
use Laravel\Fortify\Features;

'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
    Features::twoFactorAuthentication([
        'confirm' => true,
        'confirmPassword' => true,
    ]),
],
```

Щоб вимкнути можливість, закоментуйте або вилучіть відповідний запис із масиву `features`. Наприклад, вилучіть `Features::registration()`, щоб вимкнути публічну реєстрацію.

Використовуючи стартові набори [React](#react), [Svelte](#svelte) чи [Vue](#vue), вам також потрібно буде прибрати всі згадки маршрутів вимкненої можливості у коді фронтенду. Наприклад, якщо ви вимикаєте підтвердження електронної пошти, слід прибрати імпорти та звернення до маршрутів `verification` у ваших компонентах React, Svelte чи Vue. Це потрібно, бо ці набори використовують Wayfinder для типобезпечної маршрутизації, який генерує визначення маршрутів під час збірки. Якщо ви посилатиметеся на маршрути, яких більше немає, збірка вашого застосунку завершиться помилкою.

<a name="customizing-actions"></a>
### Налаштування створення користувача та скидання пароля

Коли користувач реєструється або скидає пароль, Fortify викликає класи дій, розташовані в каталозі `app/Actions/Fortify` вашого застосунку:

<div class="overflow-auto">

| Файл                          | Опис                                       |
| ----------------------------- | ------------------------------------------ |
| `CreateNewUser.php`           | Валідує та створює нових користувачів      |
| `ResetUserPassword.php`       | Валідує та оновлює паролі користувачів     |
| `PasswordValidationRules.php` | Визначає правила валідації паролів         |

</div>

Наприклад, щоб налаштувати логіку реєстрації вашого застосунку, відредагуйте дію `CreateNewUser`:

```php
public function create(array $input): User
{
    Validator::make($input, [
        'name' => ['required', 'string', 'max:255'],
        'email' => ['required', 'email', 'max:255', 'unique:users'],
        'phone' => ['required', 'string', 'max:20'], // [tl! add]
        'password' => $this->passwordRules(),
    ])->validate();

    return User::create([
        'name' => $input['name'],
        'email' => $input['email'],
        'phone' => $input['phone'], // [tl! add]
        'password' => Hash::make($input['password']),
    ]);
}
```

<a name="two-factor-authentication"></a>
### Двофакторна автентифікація

Стартові набори містять вбудовану двофакторну автентифікацію (2FA), що дозволяє користувачам захистити свої облікові записи будь-яким TOTP-сумісним застосунком-автентифікатором. 2FA увімкнено за замовчуванням через `Features::twoFactorAuthentication()` у конфігураційному файлі `config/fortify.php` вашого застосунку.

Опція `confirm` вимагає від користувачів підтвердити код, перш ніж 2FA буде повністю увімкнено, а `confirmPassword` вимагає підтвердження пароля перед увімкненням чи вимкненням 2FA. Докладніше дивіться в [документації Fortify щодо двофакторної автентифікації](/docs/{{version}}/fortify#two-factor-authentication).

<a name="rate-limiting"></a>
### Обмеження частоти

Обмеження частоти запобігає перебору паролів і повторним спробам входу, які могли б перевантажити ваші точки автентифікації. Ви можете налаштувати поведінку обмеження частоти Fortify у `FortifyServiceProvider` вашого застосунку:

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a name="teams"></a>
## Команди

Стартові набори React, Svelte, Vue і Livewire можна також згенерувати з підтримкою команд. Коли можливість команд увімкнено, кожен користувач належить до однієї чи кількох команд і має поточну команду. Під час реєстрації нові користувачі автоматично отримують особисту команду. Набори також містять екрани керування командами: створення команд, перемикання між ними, запрошення учасників і оновлення даних команди.

Коли маршрут прив'язаний до поточної команди, її slug входить до URL. Наприклад, маршрут панелі керування стає `/{current_team}/dashboard`, а сторінки керування командами використовують маршрути на кшталт `settings/teams/{team}`. Використовуючи параметри маршруту `{current_team}` і `{team}`, стартові набори автоматично перевіряють, що автентифікований користувач належить до запитаної команди, перш ніж надати доступ до маршруту.

Щоб зручніше генерувати URL з урахуванням команди, стартові набори реєструють значення URL за замовчуванням для поточної команди автентифікованого користувача. Це дозволяє викликам хелперів на кшталт `route('dashboard')` автоматично включати slug поточної команди. Коли користувач входить, реєструється чи перемикає команди, набори оновлюють поточну команду та ці значення за замовчуванням, тож згенеровані посилання й далі використовують правильний контекст команди.

Створюючи чи перейменовуючи команду, стартові набори також не дають користувачам обирати зарезервовані імена, які могли б утворити небезпечні чи конфліктні сегменти маршрутів. Наприклад, не можна використовувати імена, що збігалися б із префіксами маршрутів на кшталт `settings`, `login` чи `dashboard`.

<a name="workos"></a>
## Автентифікація через WorkOS AuthKit

За замовчуванням стартові набори React, Svelte, Vue і Livewire використовують вбудовану систему автентифікації Laravel, що пропонує вхід, реєстрацію, скидання пароля, підтвердження електронної пошти тощо. Крім того, ми пропонуємо варіант кожного набору на основі [WorkOS AuthKit](https://authkit.com), який дає:

<div class="content-list" markdown="1">

- Соціальну автентифікацію (Google, Microsoft, GitHub та Apple)
- Автентифікацію за допомогою passkey
- «Magic Auth» на основі електронної пошти
- SSO

</div>

Використання WorkOS як провайдера автентифікації [потребує облікового запису WorkOS](https://workos.com). WorkOS пропонує безкоштовну автентифікацію для застосунків із до 1 мільйона активних користувачів на місяць.

Щоб використовувати WorkOS AuthKit як провайдера автентифікації вашого застосунку, оберіть варіант WorkOS під час створення нового застосунку зі стартовим набором через `laravel new`.

### Налаштування вашого стартового набору WorkOS

Після створення нового застосунку зі стартовим набором на основі WorkOS задайте змінні середовища `WORKOS_CLIENT_ID`, `WORKOS_API_KEY` і `WORKOS_REDIRECT_URL` у файлі `.env` вашого застосунку. Ці значення мають збігатися з тими, що надані вам у панелі WorkOS для вашого застосунку:

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```

Крім того, налаштуйте URL головної сторінки застосунку в панелі WorkOS. Саме на цей URL перенаправлятимуться користувачі після виходу з вашого застосунку.

<a name="configuring-authkit-authentication-methods"></a>
#### Налаштування методів автентифікації AuthKit

Використовуючи стартовий набір на основі WorkOS, ми радимо вимкнути автентифікацію «Email + Password» у налаштуваннях WorkOS AuthKit вашого застосунку, дозволивши користувачам автентифікуватися лише через провайдерів соціальної автентифікації, passkey, «Magic Auth» і SSO. Це дозволяє вашому застосунку взагалі не мати справи з паролями користувачів.

<a name="configuring-authkit-session-timeouts"></a>
#### Налаштування тайм-аутів сесії AuthKit

Крім того, ми радимо налаштувати тайм-аут неактивності сесії WorkOS AuthKit так, щоб він відповідав налаштованому порогу тайм-ауту сесії вашого застосунку Laravel, який зазвичай становить дві години.

<a name="inertia-ssr"></a>
### Inertia SSR

Стартові набори React, Svelte і Vue сумісні з можливостями [рендерингу на боці сервера](https://inertiajs.com/server-side-rendering) від Inertia. Щоб зібрати сумісний з Inertia SSR бандл для вашого застосунку, виконайте команду `build:ssr`:

```shell
npm run build:ssr
```

Для зручності також доступна команда `composer dev:ssr`. Вона запустить сервер розробки Laravel і сервер Inertia SSR після збірки SSR-сумісного бандла, дозволяючи протестувати застосунок локально з рушієм серверного рендерингу Inertia:

```shell
composer dev:ssr
```

<a name="community-maintained-starter-kits"></a>
### Стартові набори від спільноти

Створюючи новий застосунок Laravel за допомогою інсталятора Laravel, ви можете передати прапорцю `--using` будь-який стартовий набір від спільноти, доступний на Packagist:

```shell
laravel new my-app --using=example/starter-kit
```

<a name="creating-starter-kits"></a>
#### Створення стартових наборів

Щоб ваш стартовий набір був доступний іншим, вам потрібно опублікувати його на [Packagist](https://packagist.org). Ваш набір має визначати потрібні йому змінні середовища у файлі `.env.example`, а всі потрібні команди після встановлення слід перелічити в масиві `post-create-project-cmd` файлу `composer.json` набору.

<a name="faqs"></a>
### Часті запитання

<a name="faq-upgrade"></a>
#### Як мені оновитися?

Кожен стартовий набір дає вам надійну відправну точку для наступного застосунку. Маючи повне право власності на код, ви можете доопрацьовувати, налаштовувати й будувати свій застосунок саме так, як задумали. Утім, оновлювати сам стартовий набір не потрібно.

<a name="faq-enable-email-verification"></a>
#### Як увімкнути підтвердження електронної пошти?

Підтвердження електронної пошти можна додати, розкоментувавши імпорт `MustVerifyEmail` у вашій моделі `App/Models/User.php` і переконавшись, що модель реалізує інтерфейс `MustVerifyEmail`:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
// ...

class User extends Authenticatable implements MustVerifyEmail
{
    // ...
}
```

Після реєстрації користувачі отримуватимуть лист підтвердження. Щоб обмежити доступ до певних маршрутів, доки адресу користувача не підтверджено, додайте до цих маршрутів `middleware` `verified`:

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```

> [!NOTE]
> Підтвердження електронної пошти не потрібне, коли ви використовуєте варіант стартових наборів на основі [WorkOS](#workos).

<a name="faq-modify-email-template"></a>
#### Як змінити типовий шаблон листа?

Можливо, ви захочете налаштувати типовий шаблон листа, щоб він краще відповідав брендингу вашого застосунку. Щоб змінити цей шаблон, опублікуйте представлення листів у своєму застосунку такою командою:

```
php artisan vendor:publish --tag=laravel-mail
```

Це створить кілька файлів у `resources/views/vendor/mail`. Ви можете змінювати будь-який із них, а також файл `resources/views/vendor/mail/themes/default.css`, щоб змінити вигляд типового шаблону листа.

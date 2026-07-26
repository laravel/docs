---
git: b0b1c3e17c715880e0c380cd30061da6ca952c9d
---
# Laravel Mix

- [Вступ](#introduction)

<a name="introduction"></a>
## Вступ

> [!WARNING]
> Laravel Mix - застарілий пакет, який більше активно не підтримується. Як сучасну альтернативу можна використовувати [Vite](/docs/{{version}}/vite).

[Laravel Mix](https://github.com/laravel-mix/laravel-mix) - пакет, розроблений Джеффрі Веєм, творцем [Laracasts](https://laracasts.com), - надає плавний API для опису кроків збірки [webpack](https://webpack.js.org) у вашому застосунку Laravel через кілька поширених препроцесорів CSS і JavaScript.

Іншими словами, Mix робить компіляцію та мініфікацію файлів CSS і JavaScript вашого застосунку елементарною справою. Простими ланцюжками методів ви можете плавно описати свій конвеєр ресурсів. Наприклад:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

Якщо ви колись губилися й почувалися приголомшеними, беручись за webpack і компіляцію ресурсів, Laravel Mix вам сподобається. Проте користуватися ним під час розробки застосунку не обов'язково: ви вільні взяти будь-який інший інструмент для конвеєра ресурсів - або не брати жодного.

> [!NOTE]
> У нових установках Laravel на зміну Laravel Mix прийшов Vite. Документацію щодо Mix шукайте на [офіційному сайті Laravel Mix](https://laravel-mix.com/). Якщо ви хочете перейти на Vite, перегляньте наш [посібник з міграції на Vite](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite).

---
title: "Laravel Mix"
---

- [Introdução](#introduction)

<a id="introduction"></a>
## Introdução

> **Aviso:**
> O Laravel Mix é um pacote legado que não é mais mantido ativamente. O [Vite](../vite/) pode ser usado como uma alternativa moderna.

[Laravel Mix](https://github.com/laravel-mix/laravel-mix), um pacote desenvolvido por Jeffrey Way, criador do [Laracasts](https://laracasts.com), fornece uma API fluente para definir etapas de build do [webpack](https://webpack.js.org) para sua aplicação Laravel, usando vários pré-processadores comuns de CSS e JavaScript.

Em outras palavras, o Mix facilita a compilação e minificação dos arquivos CSS e JavaScript da sua aplicação. Através de encadeamento simples de métodos, você pode definir seu pipeline de assets de forma fluente. Por exemplo:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

Se você já se sentiu confuso e sobrecarregado ao começar com o webpack e a compilação de assets, você vai adorar o Laravel Mix. No entanto, você não é obrigado a usá-lo durante o desenvolvimento da sua aplicação; você é livre para usar qualquer ferramenta de pipeline de assets que desejar, ou mesmo nenhuma.

> **Nota:**
> O Vite substituiu o Laravel Mix nas novas instalações do Laravel. Para a documentação do Mix, visite o site oficial do [Laravel Mix](https://laravel-mix.com/). Se você deseja migrar para o Vite, consulte nosso [guia de migração para o Vite](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite).

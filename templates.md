# Şablonlar

- [Denetçi Yerleşimleri(Controller Layouts)](#controller-layouts)
- [Blade Şablonlama](#blade-templating)
- [Diğer Blade Kontrol Yapıları](#other-blade-control-structures)

<a name="controller-layouts"></a>
## Denetçi Yerleşimleri(Controller Layouts)

Şablonları kullanmanın bir metodu da Laravel aracılığıyla sağlanan denetçi yerleşimleridir(controller layouts). Denetleyicide(controllerda) `layout` özelliğini belirtirken , tanımlanan görünüm(view) sizin için oluşturulacak ve kabul edilecek olan bu yanıt(response) eylemlerden(actions) döndürülecektir.

**Denetçide Yerleşim(Layout) Tanımlama**

	class UserController extends BaseController {

		/**
		 * Yerleşim(Layout) yanıtlar(responses) için kullanılmalıdır.
		 */
		protected $layout = 'layouts.master';

		/**
		 * Kullanıcı profilini göster.
		 */
		public function showProfile()
		{
			$this->layout->content = View::make('user.profile');
		}

	}

<a name="blade-templating"></a>
## Blade Şablonlama

Blade basit ve yeterli güce sahip Laravel tarafından sağlanan bir şablon(template) motorudur. Unlike controller layouts, Blade is driven by _template inheritance_ and _sections_. Tüm Blade şablonları `.blade.php` uzantısına sahip olmalıdır.

**Blade Yerleşim(Layout) Tanımlamak**

	<!-- app/views/layouts/master.blade.php içinde depolanır. -->

	<html>
		<body>
			@section('sidebar')
				Burası ana sidebar'dır.
			@show

			<div class="container">
				@yield('content')
			</div>
		</body>
	</html>

**Blade Yerleşim(Layout) Kullanmak**

	@extends('layouts.master')

	@section('sidebar')
		@parent

		<p>Burası ana sidebar'a eklendi.</p>
	@stop

	@section('content')
		<p>Bu benim body içeriğimdir.</p>
	@stop

Görünümlerdeki `extend` bir Blade yerleşimi(layout) sadece yerleşimdeki bölümleri geçersiz kıldığını unutmayın.Yerleşimin(Layout) içeriği `@parent` kullanılarak çocuk(child) görünüme dahil edilebilir,sidebar veya foooter gibi içeriklerin yerleşim(layout) bölümüne eklemenizi sağlar.

<a name="other-blade-control-structures"></a>
## Diğer Blade Kontrol Yapıları

**Veriyi Yazdırma**

	Merhaba, {{ $name }}.

	Geçerli UNIX zamanı {{ time() }}.

Tabiikide,tüm kullanıcılara sağlanan veri temizlenmeli ve kurtulmalıdır.Çıktıyı kurtarmak için üçlü küme ayracı sözdizimini kullanabilirsiniz:

	Merhaba, {{{ $name }}}.

> **Not:** Uygulamanızda kullanıcılara sağlanan içeriğine çok dikkat edin.Her zaman ve herhangi bir HTML içerik için üçlü küme ayracı sözdizimini kullanın.

**If Demeçleri**

	@if (count($kayitlar) === 1)
		Bir kaydım var!
	@elseif (count($kayitlar) > 1)
		Birden fazla kaydım var!
	@else
		Herhangi bir kaydım yok!
	@endif

	@unless (Auth::check())
		Giriş yapmadınız.
	@endunless

**Döngüler**

	@for ($i = 0; $i < 10; $i++)
		Varolan değer {{ $i }}
	@endfor

	@foreach ($users as $user)
		<p>Kullanıcı {{ $user->id }}</p>
	@endforeach

	@while (true)
		<p>Sonsuza kadar döngüdeyim.</p>
	@endwhile

**Alt-Görünümleri(Sub-Views) Dahil Etmek**

	@include('view.name')

**Dil Satırlarını Gösterme**

	@lang('language.line')

	@choice('language.line', 1);

**Yorumlar**

	{{-- Bu yorum HTML olarak yorumlanmayacaktır --}}

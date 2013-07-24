# Şablonlar

- [Denetçi Düzenleri](#controller-layouts)
- [Blade Şablonları](#blade-templating)
- [Diğer Blade Kontrol Yapıları](#other-blade-control-structures)

<a name="controller-layouts"></a>
## Denetçi Düzenleri

Laravel'de şablon kullanma yöntemlerinden birisi denetçi düzenleri üzerinden gerçekleştirilir. İlgili denetçideki `layout` özelliğinin belirlenmesiyle, belirlemiş olduğunuz görünüm oluşturulacak ve eylemlerden dönmüş cevap olarak kabul edilecektir.

**Bir Denetçide Bir Düzen Tanımlanması**

	class UyeController extends BaseController {

		/**
		 * Cevaplar için kullanılacak olan düzen.
		 */
		protected $layout = 'layouts.master';

		/**
		 * Uye profilini göster.
		 */
		public function showProfil()
		{
			$this->layout->content = View::make('uye.profil');
		}

	}

<a name="blade-templating"></a>
## Blade Şablonları

Blade Laravel'le gelen basit ama güçlü bir şablon motorudur. Denetçi düzenlerinden farklı olarak, Blade _şablon kalıtımı_ ve _kesimler_ (sections) ile yürütülür. Tüm Blade şablonlarının uzantısı `.blade.php` olmalıdır.

**Bir Blade Düzeninin Tanımlanması**

	<!-- app/views/layouts/master.blade.php 'de bulunmaktadır-->

	<html>
		<body>
			@section('sidebar')
				This is the master sidebar.
			@show

			<div class="container">
				@yield('content')
			</div>
		</body>
	</html>

**Bir Blade Düzeninin Kullanılması**

	@extends('layouts.master')

	@section('sidebar')
		@parent

		<p>Burası master sidebar'a eklenmiştir.</p>
	@stop

	@section('content')
		<p>Burası kendi content bölümümdür.</p>
	@stop

Bir Blade düzenini genişleten (`extend`) görünümlerin, düzenden gelen kesimleri değiştirmekten başka bir şey yapmadığını unutmayın. İlgili düzenin içeriği bir kesimde `@parent` direktifi kullanılarak çocuk görünüme katılabilir, böylece bir kenar çubuğu veya altbilgi gibi bir düzen kesimine eklemeler yapabilirsiniz.

<a name="other-blade-control-structures"></a>
## Diğer Blade Kontrol Yapıları

**Veri Yazdırılması**

	Merhaba {{ $isim }}.

	Şu anki UNIX zaman damgası {{ time() }}'dır.

Tabii ki, kullanıcılardan gelen tüm veriler escape edilmeli ya da arındırılmalıdır. Çıktıyı escape etmek için, üçlü küme parantezi sözdizimini kullanabilirsiniz:

	Merhaba {{{ $isim }}}.

> **Not:** Uygulamanızın kullanıcılarından gelen verileri yazdıracağınız zaman çok dikkatli olun. İçerikte olabilecek HTML antitelerini escape etmek amacıyla her zaman için üçlü küme parantezi sözdizimi kullanın.

**If Cümleleri**

	@if (count($records) === 1)
		Tek kayıt var!
	@elseif (count($records) > 1)
		Birden çok kayıt var!
	@else
		Hiç kayıt yok!
	@endif

	@unless (Auth::check())
		Giriş yapmadınız.
	@endunless

**Döngüler**

	@for ($i = 0; $i < 10; $i++)
		Şu anki değer {{ $i }}'dir.
	@endfor

	@foreach ($uyeler as $uye)
		<p>Bu, üye {{ $uye->id }}'dir.</p>
	@endforeach

	@while (true)
		<p>Sonsuz döngüdeyim.</p>
	@endwhile

**Alt Görünümlerin Dahil Edilmesi**

	@include('view.ismi')

**Dil Satırlarının Gösterilmesi**

	@lang('language.line')

	@choice('language.line', 1);

**Yorumlar**

	{{-- Bu yorum, gösterilen HTML içerisinde olmayacaktır --}}

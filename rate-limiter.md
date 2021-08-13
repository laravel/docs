# Rate Limiter

- [Introduction](#introduction)
- [Basic usage](#basic-usage)
- [Attempts](#attempts)
- [Clearing](#clearing)
- [Custom cache store](#custom-cache-store)

<a name="introduction"></a>
## Introduction

Laravel includes a simple to use Rate Limiting abstraction which, in conjunction with your application [cache](cache), provides an easy way to limit any action inside your project during a window of time.

> {note} To rate limit HTTP requests, you should use the [rate limiter middleware](routing#rate-limiting).

<a name="basic-usage"></a>
## Basic usage

The `RateLimiter` facade grants access to most tools to work with rate limiting in just a few lines.

The most basic way to use the Rate Limiter is to call `attempt()`, which rate limits a given callback. It works with the name of the action, the maximum number of attempts each 60 seconds, the callback, and an optional decay window. It returns `false` when the action has no more attempts left, otherwise it will return the callback result or `true`.

    use Illuminate\Support\Facades\RateLimiter;
    
    $executed = RateLimiter::attempt('send message', 5, function() {
        // ...
    });
    
    if (!$executed) {
      return 'Too many messages sent!';
    }

<a name="attempts"></a>
## Attempts

To check if a key was attempted too many times, use the `tooManyAttempts()` with the number of maximum attempts.

    use Illuminate\Support\Facades\RateLimiter;
    
    if (RateLimiter::tooManyAttempts('send message', 5) {
        return 'Too many attempts!';
    }

Otherwise, you may want to use `retriesLeft()` to receive the number of attempts left, or `attempts()` to compare with a number of attempts manually. After your code is attempted, remember to call `hit()` to increase the number of attempts for a given window of time in seconds.


    use Illuminate\Support\Facades\RateLimiter;
    
    if (RateLimiter::retriesLeft('send message', 5)) {
        // ...
        
        RateLimiter::hit($key, 300);
    }
    
    return 'Attempts done: ' . RateLimiter::attempts('send message');

<a name="clearing"></a>
## Clearing

You can reset the number of attempts using `resetAttempts()`, which is useful when a you want to retry a key from zero but still keep the same  decay window. For example, we can reset the number of attempts when the message is set as read by the receiver.


    use App\Models\Message;
    use Illuminate\Support\Facades\RateLimiter;
    
    public function read(Message $message)
    {
        $message->markAsRead();
        
        RateLimiter::resetAttempts('send message');
        
        return $message;
    }

The Rate Limiter works by saving in the cache both the number of attempts and decay time. The `clear()` method removes this data so a Rate Limiting key can start fresh. For example, we can clear Rate Limiting if the user that logs in is an admin.

    use Illuminate\Http\Request;
    use Illuminate\Support\Facades\RateLimiter;
    
    public function login(Request $request)
    {
        // ...
        
        if ($user->isAdmin()) {
            RateLimiter::clear('send message');
        }
    }

<a name="custom-cache-store"></a>
## Custom cache store

The Rate Limiter uses your application cache, which in fresh Laravel installation is the filesystem. In some applications this won't affect performance, but if you rely heavily on the Rate Limiter, you may want to change it for a more faster driver by providing custom Cache Store when resolving it. You can do that on your `AppServiceProvider` using [contextual binding](container#contextual-binding) and returning a [cache store](cache#accessing-multiple-cache-stores).

    use Illuminate\Cache\RateLimiter;
    use Illuminate\Contracts\Cache\Repository;
    
    public function register()
    {
        $this->app->when(RateLimiter::class)->needs(Repository::class)->give(function () {
            return cache()->store('redis');
        });
    }

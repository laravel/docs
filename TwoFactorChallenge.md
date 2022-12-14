Hi so if you are using Laravel Fortify without jetstream you will face a common issue that it will not trigger two factor challenge at the time of login.So
Here is the solution.

If you send post request or ajax post request it will show you {"two_factor":true} in response.

Now make a check if two_factor == true show your two factor challenge page otherwise login user.

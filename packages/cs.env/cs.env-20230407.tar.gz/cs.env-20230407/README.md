Some environment related functions.

*Latest release 20230407*:
getenv: new parse callable parameter to parse the value.

* LOGDIR, VARRUN, FLAGDIR: lambdas defining standard places used in other modules

* envsub: replace substrings of the form '$var' with the value of 'var' from `environ`.

* getenv: fetch environment value, optionally performing substitution

## Function `envsub(s, environ=None, default=None)`

Replace substrings of the form '$var' with the value of 'var' from environ.

Parameters:
* `environ`: environment mapping, default `os.environ`.
* `default`: value to substitute for unknown vars;
        if `default` is `None` a `ValueError` is raised.

## Function `getenv(var, default=None, environ=None, dosub=False, parse=None)`

Fetch environment value.

Parameters:
* `var`: name of variable to fetch.
* `default`: default value if not present. If not specified or None,
  raise KeyError.
* `environ`: environment mapping, default `os.environ`.
* `dosub`: if true, use envsub() to perform environment variable
  substitution on `default` if it used. Default value is `False`.
* `parse`: optional callable to parse the environment variable;
  *NOTE*: if this raises `ValueError` and there is a default, issue
  a warning and return `default`

## Function `LOGDIR(environ=None)`

various standard locations used in the cs.* modules

# Release Log



*Release 20230407*:
getenv: new parse callable parameter to parse the value.

*Release 20190103*:
* Drop getLogin and getHomeDir, unused.
* Make get_standard_var private as _get_standard_var.

*Release 20170905.1*:
Tweak doco and DISTINFO.

*Release 20170905*:
Add LOGDIR, VARRUN, FLAGDIR wrappers for new get_standard_var function to provide standard policy variables.

*Release 20160828*:
Update metadata with "install_requires" instead of "requires".

*Release 20150118*:
Initial PyPI release.

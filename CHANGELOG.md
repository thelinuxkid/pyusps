# CHANGELOG

## 1.0.0

See https://github.com/thelinuxkid/pyusps/issues/10 for
the motivation of many of these changes.

### Changed

- Drop support for anythin below Python 3.6
- Main signature changes from `verify(user_id, *args)` to `verify(user_id, args)`
  You must always supply an iterable of inputs. Single inputs are no longer supported,
  just wrap them in a length-one list if you need. Always returns a list of 
  `dicts`/`USPSError`s.
- Instead of `OrderedDict`s, we just return plain old `dict`s.
- Changed returned/raised `ValueError`s from not-found addresses to be always-returned
  `USPSError`s
- Instead of `TypeError` or `ValueError` from parsing errors, we now consistently raise
  `RuntimeError`s
- Removed `api_url` from global namespace. IDK why you would have relied on this though.

### Added

- Supports supplying an iterable of addresses, no longer needs the __len__ method.
- Each supplied input now only needs to have a `__getitem__()` method. Before, it
  needed that but also a `get()` method.
- If you supply an empty iterable as input, you get back an empty list, not an error.
- The new `USPSError` includes the attributes `code: str` and `description: str`
  so you can get the original error without having to do string parsing.
- Testing on GitHub Actions!
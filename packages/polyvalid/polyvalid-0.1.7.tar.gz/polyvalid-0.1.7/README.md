# polyvalid

`polyvalid` is a Rust library for validating package names, usernames, namespace names, and app names. The library provides a single source of truth for validating the names with the following rules:

1. Start with an alphabet character
2. Have one or more alphanumeric characters, `_` or `-`
3. End with an alphanumeric character

Additionally, the library checks if the name contains `--` since it can break URL rules.

The library can be used from Python and JS through the provided bindings.


## Using the library
The library can be used from rust, python or javascript. The following describes how to use it from all three languages.

### Rust

```bash
cargo add polyvalid
```

```rust
use polyvalid;

let name: String = "polyvalid";

assert!(polyvalid::is_app_name_valid(name));
```

### Python


```bash
pip add polyvalid
```

```python
import polyvalid

name = "polyvalid"
polyvalid.is_app_name_valid(name) # returns True
```


### Javascript

```bash
npm i polyvalid
```

```js
import "polyvalid";
name = "polyvalid";
polyvalid.is_valid_name(name); // returns true
```


## Next steps

- [ ] Add CI to autopublish to wapm, pypi, npm
- [ ] Add tests for python and JS versions of the library
- [ ] Add wrapper around the python library (to improve usability)

## Contributing

Contributions are welcome! If you'd like to contribute to `polyvalid`, please follow these steps:

1. Fork the repo and create a new branch for your changes.
2. Make your changes, write tests, and ensure that the tests pass.
3. Submit a pull request to the `polyvalid` repo.
4. Wait for feedback or approval from the maintainers.

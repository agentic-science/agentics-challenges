# Public Validation Data

The committed public data is intentionally tiny. It validates binary parsing, output shape, and tolerance handling, but it is not representative of official benchmark cost.

Regenerate it with:

```sh
python tools/generate_assets.py --root . --preset public
```

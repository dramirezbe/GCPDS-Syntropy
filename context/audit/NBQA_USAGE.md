# NBQA Usage

## Fatal Issue Gate

```bash
nbqa ruff "$NOTEBOOK" --select=F821,F822,F823 --output-format=json --ignore=F821
```

## If No Fatal Issues

```bash
nbqa ruff "$NOTEBOOK" --select=E,F,I --fix --ignore=F821   # isort, style errors
nbqa black "$NOTEBOOK"                         # format (black)
nbqa yapf "$NOTEBOOK"                          # format (yapf)
```

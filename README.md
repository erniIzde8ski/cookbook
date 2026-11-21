# cookbook

A cookbook written in Typst. [Downloads updated daily here.](https://github.com/ernieIzde8ski/cookbook/releases/tag/latest)

## Development

### Requirements

- git (duh)
- [`prek`](https://prek.j178.dev/installation/) (NOT pre-commit)
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) (optional)
- [`tinymist`](https://github.com/Myriad-Dreamin/tinymist) (optional, built
  against Typst v0.15.0 or higher)
- Fonts:
  - Bitstream Vera Sans
  - Source Sans Pro
  - Ysabeau
  - Twemoji

On Void Linux:

```
xi -u
xi source-sans-pro texlive-core ttf-bitstream-vera twemoji
```

You will need to set the formatter to `typstyle`, `lineLength=90`, prose
wrapping, and `/path/to/checkout/src/` base directory. I find it works better
in Neovim than in VSCode, for whatever reason.

Setup:

```bash
# Prek will auto-install all the tools we need in an isolated environment for
# us. The "optional" utils are only required if you want to run them manually
# too.
prek install

# optional, for Python scripts
uv sync
```

### Utilities

- Run formatters & linters: `prek`
- Build: `doit`
- Generate new recipe: `./new.py <section> <name>`

# Setup

Use as a submodule. Note that it must be named `generator` for the Github CI script to work

```bash
git submodule add git@github.com:JosefUtbult/SiteGenerator.git generator
```

Copy the Github CI script to the root repository

```bash
cp -r generator/ci/.github .
```

Add `static/` to `.gitignore`

```bash
echo "static/" >> .gitignore
```

Copy `docs/` folder template

```bash
cp -r generator/docs_template docs
```

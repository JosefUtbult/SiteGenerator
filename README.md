# Setup

Use as a submodule

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

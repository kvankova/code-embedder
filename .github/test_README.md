# Testing README

This is a test readme.

This will update:
```python:.github/workflows/test_code_embedder.yml
name: Test Code Embedder

on: pull_request

jobs:
  code_embedder:
    name: "Code embedder"
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          ref: ${{ github.event.pull_request.head.ref }}

      - name: Run code embedder
        uses: ./
        with:
          readme_paths: .github/test_README.md .github/test_empty_README.md
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

```

This will update:
```yaml:.github/release-drafter-config.yml
name-template: 'v$RESOLVED_VERSION 🌈'
tag-template: 'v$RESOLVED_VERSION'
change-template: '- $TITLE @$AUTHOR (#$NUMBER)'

version-resolver:
  major:
    labels:
      - 'major'
      - 'breaking'
      - 'breaking change'
  minor:
    labels:
      - 'minor'
  default: patch

categories:
  - title: 🏆 Highlights
    labels: highlight
  - title: ✨ Features
    labels:
      - feature
      - enhancement
  - title: 🚀 Performance improvements
    labels: performance
  - title: 🐛 Bug Fixes
    labels:
      - fix
      - bugfix
      - bug
  - title: 📖 Documentation
    labels: documentation
  - title: 🛠️ Other improvements
    labels: internal

exclude-labels:
  - skip changelog
  - release

replacers:
  # Remove conventional commits from titles
  - search: '/- (build|chore|ci|depr|docs|feat|fix|perf|refactor|release|test)(\(.*\))?(\!)?\: /g'
    replace: '- '

template: |
  $CHANGES

```

This won't update:
```python
print("Hello, World!")
```

# AGENTS.md (project)

## Overrides
install: python -m pip install -r requirements.txt
lint: python -m pyflakes src
test: python -m pytest -q --disable-warnings
test:it: python -m pytest -q -m 'it'
coverage_min: 80

components: [auth, api, notify, db]

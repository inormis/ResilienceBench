.PHONY: install validate

install:
\tpython -m pip install -r requirements.txt

validate:
\tpython scripts/validate.py

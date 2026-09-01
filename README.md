# risk-scoring

Transaction risk scoring. Rules come from a YAML file, so `PyYAML` is on the path that
reads configuration; `requests` is used to fetch the sanctions list.

```
risk_scoring/config.py   loads rules.yaml (yaml.safe_load)
risk_scoring/score.py    the scoring rules
risk_scoring/client.py   sanctions lookup over HTTP (requests)
rules.yaml               thresholds and weights
tests/                   unittest, no test framework dependency
```

Dependency versions in `requirements.txt` are deliberately old, so a scan has something
to find.

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests
```

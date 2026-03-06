# Contributing

Thanks for considering a contribution.

## Workflow
1. Create a branch from `main`.
2. Keep changes scoped and documented.
3. Add or update tests when behavior changes.
4. Open a pull request with a clear summary.

## Local checks
```bash
pip install -r projects/aws-inventory-tool/requirements.txt
pytest projects/aws-inventory-tool/tests -q
```

## Standards
- Do not commit secrets or credentials.
- Keep automation scripts small and maintainable.
- Prefer explicit logging for operational scripts.

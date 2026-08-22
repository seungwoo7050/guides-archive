test:
	PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
check: test
	PYTHONDONTWRITEBYTECODE=1 python3 kernel-model.py lifecycle examples/lifecycle.json >/dev/null
clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

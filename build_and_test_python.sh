for py in 3.15 3.14 3.13 3.12 3.11 3.10 3.9; do
  echo "=== Python $py ==="
  uv sync --locked --python "$py" --extra all --extra dev || exit 1
  uv run --locked --python "$py" --extra all --extra dev ruff check --config pyproject.toml || exit 1
  uv run --locked --python "$py" --extra all --extra dev pytest || exit 1
  uv run --locked --python "$py" --extra all --extra dev coverage run -m unittest discover -s tests/ || exit 1
  uv run --locked --python "$py" --extra all --extra dev coverage report -m || exit 1
  echo "=== Python $py checks ended==="
done
# Contributing

This is an Infosys internship project by **M. Ramya Srivalli**.

It is shared publicly for reference and learning purposes.

If you find a bug or want to suggest an improvement, feel free to open an issue.

## How to Report Issues

1. Go to the **Issues** tab on GitHub
2. Click **New Issue**
3. Describe the problem clearly — include steps to reproduce

## Code Style

- Python: follow PEP 8
- JavaScript: ES6+ with clear variable names
- Always add comments to explain non-obvious logic

## Running Tests Before Submitting

```bash
pip install pytest httpx fastapi uvicorn
pytest Milestone_4/test_m4_ivr.py -v
```

All tests must pass before any code change is considered complete.
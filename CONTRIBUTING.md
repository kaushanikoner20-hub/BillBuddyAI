# Contributing to BillBuddy AI

Thanks for your interest! Small, clear contributions are welcome.

## Getting started

1. Fork the repository and clone your fork.
2. Follow the setup steps in [README.md](README.md).
3. Create a branch: `git checkout -b my-change`

## Guidelines

- Keep code simple and readable. Beginner-friendly is a goal.
- Do not add paid APIs, API keys, or cloud AI services.
- Never commit real receipts, databases, or secrets. Use fake sample data.
- Add or update tests for backend changes.

## Before opening a pull request

```powershell
cd backend
python -m pytest

cd ..\frontend
npm run build
```

Then push your branch and open a pull request describing what changed and why.

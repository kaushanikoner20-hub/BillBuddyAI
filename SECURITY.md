# Security Policy

## Handling sensitive financial documents

Receipts and invoices can contain names, addresses, card fragments, and purchase history.

- Process documents locally. Do not send them to cloud services.
- Never commit real receipts, exports, databases, or `.env` files. The `.gitignore` excludes them, but double-check before every commit.
- Use fake or heavily redacted samples in issues, screenshots, and tests.
- Store uploads and the database in a folder only you can access, and consider disk encryption (for example BitLocker on Windows).
- This project has no authentication yet. Run it only on your own computer and do not expose it to the internet.

## Reporting a vulnerability

Please do **not** open a public issue for security problems.

Use GitHub's private reporting: on the repository page, open the **Security** tab and choose **Report a vulnerability**.
Include what you found, how to reproduce it, and the possible impact. Do not include real financial documents.

You can expect an acknowledgement as soon as the maintainer is able. This is a volunteer project, so no fixed response time is guaranteed.

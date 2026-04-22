# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x (Current) | :white_check_mark: |
| < 1.0   | :x:                |

---

## Reporting a Vulnerability

The AI Credit Intelligence Engine handles financial and credit-related data.
We take security vulnerabilities seriously.

**Please do NOT open a public GitHub issue for security vulnerabilities.**

Instead, report privately via:

- **Email:** itsarnav.singh80@gmail.com
- **LinkedIn DM:** [Arnav Singh](https://www.linkedin.com/in/arnav-singh-a87847351)
- **GitHub Private Advisory:** Go to the Security tab → Click "Report a vulnerability"

### Include in Your Report

- Description of the vulnerability
- Steps to reproduce
- Potential impact (especially on credit/financial data)
- Suggested fix (optional)

---

## Response Timeline

| Action          | Timeframe             |
| --------------- | --------------------- |
| Acknowledgement | Within 48 hours       |
| Status Update   | Within 5 business days|
| Fix / Resolution| Within 30 days        |

---

## Security Practices

- All PRs are reviewed by the maintainer before merging
- No sensitive data (API keys, credentials) is hardcoded
- ML models handle financial data — inputs are validated and scaled before processing
- Dependencies (Scikit-learn, Pandas, Streamlit, etc.) are periodically reviewed
- Contributors must follow our [Code of Conduct](docs/CODEOFCONDUCT.md)

---

## Disclosure Policy

Once a vulnerability is resolved:

1. A patched version will be released
2. Reporter will be credited (if they wish)
3. A brief summary of the fix will be shared

---

## Contact

**Arnav Singh** — Project Maintainer & NSoC'26 Admin

- Email: itsarnav.singh80@gmail.com
- LinkedIn: https://www.linkedin.com/in/arnav-singh-a87847351
- GitHub: https://github.com/Arnav-Singh-5080
# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | :white_check_mark: Active |
| < Latest | :x: No |

Always use the latest version to receive security patches and improvements.

---

## Reporting a Vulnerability

The Africa Fintech API team takes security seriously — especially for financial services handling real money. We appreciate your efforts to responsibly disclose any security concerns.

**Please do NOT report security vulnerabilities through public GitHub issues.**

### Step-by-Step Reporting Process

1. **Identify the vulnerability** — Document the issue with clear reproduction steps.
2. **Email the security team** at **raphasha27@github.com** with the following:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment (especially for financial data)
   - Suggested fix (if any)
3. **Wait for acknowledgment** — You will receive a response within **48 hours**.
4. **Collaborate on the fix** — We may reach out for additional details.
5. **Disclosure** — We will coordinate a public disclosure timeline with you.

### What to Include

- Type of vulnerability (e.g., SQL injection, authentication bypass, IDOR)
- Affected component and version
- Attack vector and prerequisites
- Proof of concept (if available)
- Your suggested remediation
- Potential impact on financial transactions or user data

---

## Security Response Timeline

| Phase | Timeframe |
|-------|-----------|
| Initial acknowledgment | 48 hours |
| Severity assessment | 3 business days |
| Patch development | 5–10 business days |
| Coordinated disclosure | 30 days after fix |

Financial data vulnerabilities may receive expedited timelines. We will keep you informed throughout the process.

---

## Security Design

This project implements the following security measures:

- **JWT Authentication** — Stateless tokens with configurable expiry
- **Bcrypt Password Hashing** — Secure credential storage with salt
- **Redis Rate Limiting** — Abuse prevention per API key/IP
- **Input Validation** — Pydantic models validate all API inputs
- **SQL Injection Protection** — SQLAlchemy ORM with parameterized queries
- **Idempotency Keys** — Prevent duplicate transactions
- **Audit Logging** — Complete transaction history for compliance
- **Environment Variables** — No hardcoded secrets

---

## Security Best Practices for Users

When deploying or developing with Africa Fintech API:

### Configuration
- Always use **environment variables** for `DATABASE_URL`, `JWT_SECRET`, and `REDIS_URL`
- Never commit `.env` files or secrets to version control
- Use strong, randomly generated JWT secrets (minimum 256 bits)
- Set short token expiry for production (15 minutes recommended)

### Authentication
- Enforce strong password policies for user registration
- Rotate JWT secrets periodically
- Implement token refresh rotation
- Monitor for unusual authentication patterns

### Financial Security
- Validate all monetary amounts server-side
- Use idempotency keys for all write operations
- Implement transaction limits per user/wallet
- Log all financial operations for audit trails

### Network
- Deploy behind a reverse proxy with TLS termination
- Enable CORS only for trusted origins
- Use HTTPS for all API communications
- Restrict database access to application network

### Dependencies
- Run `pip audit` for Python dependency vulnerabilities
- Enable Dependabot alerts for automatic vulnerability notifications
- Review dependency updates before merging

---

## Dependency Management

### Python Dependencies

```bash
# Check for known vulnerabilities
pip install pip-audit
pip-audit

# Update dependencies
pip install --upgrade -r requirements.txt

# Verify package integrity
pip install pip-audit
pip-audit --fix
```

### Automated Scanning

- **Dependabot** is enabled for automatic dependency update PRs.
- **CI pipeline** runs `pip-audit` on every PR.
- Review and merge Dependabot PRs promptly.
- Pin dependency versions in `requirements.txt` for reproducibility.

---

## Responsible Disclosure

We follow [coordinated disclosure](https://en.wikipedia.org/wiki/Coordinated_vulnerability_disclosure) principles:

- Report vulnerabilities privately before public disclosure.
- We will credit reporters in release notes (unless anonymity is preferred).
- We ask that you do not exploit the vulnerability beyond what is necessary to demonstrate it.
- We will not pursue legal action against researchers who follow this policy.

---

## Contact

- **Security Email**: raphasha27@github.com
- **General Issues**: [GitHub Issues](../../issues)

Thank you for helping keep Africa Fintech API and its users safe.

cat > README.md << 'EOF'
# ShadowMap — Web Reconnaissance Tool

> By Sipar Security | Free Edition | v1.0

A lightweight, open-source web reconnaissance tool built for bug bounty hunters and penetration testers.

---

## What It Does

- Passive subdomain enumeration via certificate transparency logs
- DNS recon and zone transfer attempts
- Port scanning — top 20 common ports
- Clean terminal output

---

## Installation

```bash
git clone https://github.com/siparsecurity/shadowmap.git
cd shadowmap
pip install -r requirements.txt
```

---

## Usage

```bash
python3 main.py --domain example.com
python3 main.py --domain example.com --skip-ports
python3 main.py --domain example.com --skip-dns
```

---

## What's Included — Free vs Pro

| Feature | Free | Pro |
|---|---|---|
| Passive subdomain enumeration | ✅ | ✅ |
| Active brute-force with SecLists | ❌ | ✅ |
| DNS recon & zone transfer | ✅ | ✅ |
| Port scanning — top 20 ports | ✅ | ✅ |
| Technology fingerprinting | ❌ | ✅ |
| Misconfiguration detection | ❌ | ✅ |
| Stealth modes | ❌ | ✅ |
| HTML / PDF report generation | ❌ | ✅ |
| JSON export | ❌ | ✅ |

ShadowMap Pro coming soon — [siparsecurity.github.io](https://siparsecurity.github.io)

---

## Requirements

- Python 3.10+
- `requests`
- `dnspython`
- `rich`

---

## Responsible Use

This tool is for authorized security testing only.
Always have written permission before scanning any target.

---

## About

Built by **Sipar Security** — an open-source cybersecurity company from Pakistan.

- 🌐 [siparsecurity.github.io](https://siparsecurity.github.io)
- 📧 siparsecurity@gmail.com
- 💼 [LinkedIn](https://linkedin.com/company/siparsecurity)
- ⭐ [GitHub](https://github.com/siparsecurity)
EOF

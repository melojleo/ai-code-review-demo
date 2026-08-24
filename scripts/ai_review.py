import os
import sys
import requests


api_key = "".join(os.environ["GEMINI_API_KEY"].split())

if not api_key.startswith("AIza"):
    raise ValueError(
        "GEMINI_API_KEY does not look like a valid Gemini API key"
    )

print(f"API key loaded: {bool(api_key)}")
print(f"API key length: {len(api_key)}")
print(f"Starts with AIza: {api_key.startswith('AIza')}")

diff_file = sys.argv[1]

with open(diff_file, "r", encoding="utf-8") as f:
    diff = f.read()


prompt = f"""
You are a senior software engineer performing a Pull Request code review.

Review ONLY the changed code provided in the Git diff below.

Focus on:
- Bugs
- Security vulnerabilities
- Hardcoded secrets
- Error handling
- Performance
- Maintainability
- Code quality
- Best practices

Do not complain about minor formatting or stylistic preferences.

Return a concise Pull Request review in Markdown.

Use this format:

# 🤖 AI Code Review

## Summary
Provide a very short overall assessment.

## Findings

For each relevant issue:

### 🔴 HIGH / 🟠 MEDIUM / 🟡 LOW

**File:** filename

**Issue:** Explain the problem.

**Recommendation:** Explain how to fix it.

At the end include:

## ✅ Positive aspects

Mention anything that was implemented well.

If there are no significant issues, explicitly say so.

Git diff:

{diff}
"""


url = (
    "https://generativelanguage.googleapis.com/"
    f"v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
)

headers = {
    "Content-Type": "application/json"
}


payload = {
    "contents": [
        {
            "parts": [
                {
                    "text": prompt
                }
            ]
        }
    ]
}


response = requests.post(
    url,
    headers=headers,
    json=payload,
    timeout=120
)

response.raise_for_status()

data = response.json()

review = data["candidates"][0]["content"]["parts"][0]["text"]

print(review)

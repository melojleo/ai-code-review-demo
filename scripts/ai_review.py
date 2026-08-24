import os
import sys
import requests


api_key = os.environ["GEMINI_API_KEY"].strip()

if not api_key:
    raise ValueError("GEMINI_API_KEY is empty")


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

Return a concise Pull Request review in Markdown.

Git diff:

{diff}
"""


url = (
    "https://generativelanguage.googleapis.com/"
    "v1beta/models/gemini-3.7-flash:generateContent"
)

print("MODEL USED: gemini-3.7-flash", file=sys.stderr)


headers = {
    "x-goog-api-key": api_key,
    "Content-Type": "application/json",
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


if not response.ok:
    print("Gemini error:", response.status_code)
    print(response.text)
    response.raise_for_status()


data = response.json()

review = data["candidates"][0]["content"]["parts"][0]["text"]

print(review)

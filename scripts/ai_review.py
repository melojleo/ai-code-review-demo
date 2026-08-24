import os
import sys
import time
import requests


api_key = os.environ["GEMINI_API_KEY"].strip()

if not api_key:
    raise ValueError("GEMINI_API_KEY is empty")


diff_file = sys.argv[1]

with open(diff_file, "r", encoding="utf-8") as f:
    diff = f.read()


prompt = f"""
Review this Pull Request diff.

Identify only important issues related to:
- bugs
- security
- error handling
- maintainability

Be concise.

Return Markdown using this structure:

# 🤖 AI Code Review

## Summary
One short sentence.

## Findings

For each relevant issue:

### 🔴 HIGH / 🟠 MEDIUM / 🟡 LOW

**File:** filename

**Issue:** explanation

**Recommendation:** recommended fix

If there are no important issues, say:
"No significant issues found."

DIFF:

{diff[:30000]}
"""


MODEL = "gemini-3.5-flash-lite"

print(f"MODEL USED: {MODEL}", file=sys.stderr)


url = (
    "https://generativelanguage.googleapis.com/"
    f"v1beta/models/{MODEL}:generateContent"
)


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
    ],
    "generationConfig": {
        "maxOutputTokens": 1200
    }
}


for attempt in range(3):

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=180
        )

        if not response.ok:

            print(
                f"Gemini API error: {response.status_code}",
                file=sys.stderr
            )

            print(
                response.text,
                file=sys.stderr
            )

            raise SystemExit(1)

        break

    except requests.exceptions.ReadTimeout:

        if attempt == 2:
            raise

        print(
            "Gemini timeout - retrying...",
            file=sys.stderr
        )

        time.sleep(5)


data = response.json()

review = data["candidates"][0]["content"]["parts"][0]["text"]

print(review)

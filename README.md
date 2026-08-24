# AI-Assisted Pull Request Review --- Azure DevOps

## Objective

Reduce manual review effort, improve consistency, and detect issues
earlier without changing the existing Azure DevOps workflow.

## How It Works

``` text
Developer → Pull Request → Azure Pipeline → AI Review → PR Comments → Human Approval
```

When a PR is created or updated, an Azure Pipeline extracts the code
diff, sends it to an AI model, and posts findings back to the PR through
the Azure DevOps REST API.

Reviews can be customized to check:

-   Security
-   Bugs
-   Performance
-   Coding standards
-   Project-specific architecture rules

A working Claude implementation reports feedback appearing in the PR in
roughly **30--60 seconds**.

Source: [Claude Code Review on Azure DevOps: Build It
Yourself](https://www.linkedin.com/pulse/claude-code-review-azure-devops-build-yourself-nitin-garg-vcoqc)

## AI Options

| Option | Implementation | Key Advantage | Indicative Cost |
|---|---|---|---|
| **Claude (Anthropic)** | Azure Pipeline → Claude API → Azure DevOps REST API | Strong code reasoning and highly customizable review rules | API consumption; token-based pricing can make individual reviews inexpensive depending on PR size and model |
| **OpenAI / Azure OpenAI** | Azure Pipeline → OpenAI/Azure OpenAI → Azure DevOps REST API | Strong reasoning and good fit with Microsoft/Azure governance | Token-based. For reference, GPT-5 pricing is $1.25/M input tokens + $10/M output tokens; cheaper model tiers are available |
| **CodeRabbit** | Native Azure DevOps integration | Purpose-built product with minimal custom development and maintenance | Pro: **$24/user/month** annually; Pro Plus: **$48/user/month** annually |

### Pricing References

- [Anthropic pricing reference](https://www-cdn.anthropic.com/files/4zrzovbb/website/3684c2faafb97418665782cea0001f439f74b1d2.pdf)
- [OpenAI GPT-5 model and pricing](https://developers.openai.com/api/docs/models/gpt-5)
- [CodeRabbit pricing](https://www.coderabbit.ai/pricing)

## Business Value

**Faster reviews** --- AI provides the first-pass review in seconds,
allowing senior developers to focus on architecture and business logic
rather than repetitive checks.

**Consistent quality** --- Every PR can be evaluated against the same
security, quality, naming, and architecture standards.

**Earlier defect detection** --- Potential bugs, security problems,
performance issues, and maintainability concerns are identified before
merge.

**Less reviewer bottleneck** --- Developers receive immediate feedback
instead of waiting for another developer to become available.

**Project-specific knowledge** --- Custom solutions using Claude or
OpenAI can encode internal engineering standards directly into the
review prompt.

**Human remains accountable** --- AI acts as a **first reviewer, not the
final approver**.

## Illustrative Time-Saving Scenario

The savings should be presented as an **estimate to validate during a
PoC**, rather than as a universal percentage.

> **Example:** 100 PRs/month × 30 min average manual review = **50
> reviewer hours/month**.

If AI removes only 30% of repetitive first-pass review work:

> **\~15 engineering hours/month saved**

This is in addition to faster developer feedback and reduced review
queues.

The ROI can be especially attractive for a custom API solution because
inference cost per review can be small compared with engineering time.

The referenced Claude Azure DevOps implementation describes the API cost
as "pennies per review" and demonstrates that the integration can be
built directly with Azure Pipelines and the Azure DevOps REST API,
without requiring a third-party extension.

Source: [Claude Code Review on Azure DevOps: Build It
Yourself](https://www.linkedin.com/pulse/claude-code-review-azure-devops-build-yourself-nitin-garg-vcoqc)

## Recommended PoC

Compare:

-   **Claude**
-   **Azure OpenAI / OpenAI**
-   **CodeRabbit**

Test the alternatives against **20--30 historical Pull Requests**.

Measure:

-   Useful findings
-   False positives
-   Review time saved
-   Cost per PR
-   Security findings
-   Developer acceptance


## Key Message

> **AI does not replace the human reviewer. It automates repetitive
> first-level review work, provides developers with faster feedback, and
> allows engineers to focus on architecture, business logic, and
> higher-value decisions.**

## Sources

-   [Claude + Azure DevOps
    implementation](https://www.linkedin.com/pulse/claude-code-review-azure-devops-build-yourself-nitin-garg-vcoqc)
-   [Azure OpenAI PR review
    example](https://techcommunity.microsoft.com/blog/healthcareandlifesciencesblog/azure-openai-gpt-model-to-review-pull-requests-for-azure-devops/3851470)
-   [CodeRabbit Azure DevOps
    documentation](https://docs.coderabbit.ai/platforms/azure-devops/)
-   [CodeRabbit pricing](https://www.coderabbit.ai/pricing)
-   [OpenAI model
    pricing](https://developers.openai.com/api/docs/models/gpt-5)


# AI-Assisted Pull Request Review Demo

## 1. Objective

This demo shows how AI can be integrated into a Pull Request workflow to provide an automated first-level code review.

The demo uses:

- GitHub
- GitHub Actions
- Gemini API
- Python
- Pull Request comments

The same concept can later be implemented in Azure DevOps using Azure Pipelines and the Azure DevOps REST API.

---

## 2. High-Level Flow

```text
Developer
    ↓
Pull Request
    ↓
GitHub Action
    ↓
Get PR Diff
    ↓
Gemini API
    ↓
AI Code Review
    ↓
Automatic PR Comment
    ↓
Human Reviewer
```

The AI does not replace the human reviewer. It provides an automated first review so that obvious issues can be identified earlier.

> **Screenshot suggestion:** Add an overview screenshot of the repository or the Pull Request workflow here.

---

## 3. Repository Structure

```text
ai-code-review-demo/
│
├── src/
│   └── user_service.py
│
├── scripts/
│   └── ai_review.py
│
└── .github/
    └── workflows/
        └── ai-code-review.yml
```

---

## 4. Create the Initial Application Code

Create:

```text
src/user_service.py
```

Initial code:

```python
import os
import requests


def get_user(user_id):
    if not user_id:
        raise ValueError("user_id is required")

    api_url = os.getenv("API_URL")

    response = requests.get(
        f"{api_url}/users/{user_id}",
        timeout=10
    )

    response.raise_for_status()

    return response.json()
```

Commit this version to the `main` branch.

![alt text](image-1.png) Repository structure and the initial `user_service.py` file.

---

## 5. Create a Gemini API Key

Create an API key in Google AI Studio.

Store the key securely in GitHub:

```text
Repository
→ Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

Create:

```text
GEMINI_API_KEY
```

The API key must never be committed to the repository.

![alt text](image-2.png) GitHub Actions secrets page showing `GEMINI_API_KEY`. Do not expose the secret value.

---

## 6. Create the AI Review Script

Create:

```text
scripts/ai_review.py
```

Example implementation:

```python
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
            print(response.text, file=sys.stderr)
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
```

### What the script does

1. Reads the Git diff generated by the Pull Request.
2. Sends the changed code to the Gemini API.
3. Asks the model to focus on important review topics.
4. Produces a concise Markdown review.
5. Returns the generated review to the GitHub Action.

---

## 7. Create the GitHub Action

Create:

```text
.github/workflows/ai-code-review.yml
```

Example workflow:

```yaml
name: AI Code Review

on:
  pull_request:
    types:
      - opened
      - synchronize
      - reopened

permissions:
  contents: read
  pull-requests: write

jobs:
  ai-review:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install Python dependencies
        run: |
          pip install requests

      - name: Get Pull Request diff
        env:
          GH_TOKEN: ${{ github.token }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
        run: |
          gh pr diff "$PR_NUMBER" > pr.diff

      - name: Run AI Code Review
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          python scripts/ai_review.py pr.diff > review.md

      - name: Post AI Review to Pull Request
        env:
          GH_TOKEN: ${{ github.token }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
        run: |
          gh pr comment "$PR_NUMBER" --body-file review.md
```

### What the workflow does

When a Pull Request is opened, updated or reopened, the workflow automatically:

1. Checks out the repository.
2. Gets the Pull Request diff.
3. Runs the AI review script.
4. Posts the AI response as a Pull Request comment.

![alt text](image-3.png) GitHub Actions workflow showing all steps completed successfully.

---

## 8. Create a Test Branch

Create:

```text
feature/customer-api
```

Use `main` as the base branch.

---

## 9. Introduce Intentional Issues

For the demo, replace `src/user_service.py` with:

```python
import requests


def get_user(user_id):

    password = "SuperSecret123"

    url = "https://api.company.com/users/" + user_id

    response = requests.get(url)

    print("Database password:", password)

    return response.json()
```

This intentionally introduces:

- Hardcoded credentials
- Sensitive data written to logs
- Missing HTTP timeout
- Missing error handling
- Missing HTTP status validation
- Missing input validation

Commit the change to the feature branch.

---

## 10. Create the Pull Request

Create a Pull Request:

```text
feature/customer-api
        ↓
      main
```

Example title:

```text
Add customer API integration
```

Example description:

```text
This PR introduces the new customer API integration.
```

![alt text](<Screenshot 2026-08-24 115200.png>) Pull Request diff showing the intentionally introduced issues.

---

## 11. Automatic AI Review

As soon as the Pull Request is created, GitHub Actions starts the AI review automatically.

```text
Checkout repository
        ↓
Get Pull Request diff
        ↓
Run AI Code Review
        ↓
Post AI Review to Pull Request
```

No developer interaction with the AI model is required.

![alt text](<Screenshot 2026-08-24 120108.png>) GitHub Action execution with all steps marked as successful.

---

## 12. AI Comment in the Pull Request

The generated review is posted automatically in the Pull Request conversation.

Example:

```text
🤖 AI Code Review

Summary

The changes introduce security and reliability concerns.

🔴 HIGH

File: src/user_service.py

Issue:
A password is hardcoded directly in the source code
and later written to the application logs.

Recommendation:
Use a secure secret management solution and never
log credentials.


🟠 MEDIUM

Issue:
The HTTP request does not define a timeout.

Recommendation:
Define an appropriate request timeout.


🟠 MEDIUM

Issue:
HTTP errors are not handled.

Recommendation:
Validate the response status and handle request exceptions.
```

![alt text](image-4.png) 
Main demo screenshot — show the AI review comment directly inside the Pull Request.

---

## 13. Developer Fixes the Issues

Update the same feature branch with corrected code:

```python
import os
import requests


def get_user(user_id):

    if not user_id:
        raise ValueError("user_id is required")

    api_url = os.getenv("API_URL")

    response = requests.get(
        f"{api_url}/users/{user_id}",
        timeout=10
    )

    response.raise_for_status()

    return response.json()
```

Commit the changes to the same Pull Request.

Because the workflow listens for the `synchronize` event, the AI review runs automatically again.

---

## 14. Second Review

```text
Developer fixes code
        ↓
New commit
        ↓
Pull Request updated
        ↓
AI review automatically runs again
        ↓
New review comment
```

Example second review:

```text
🤖 AI Code Review

No significant issues found.

Positive aspects:

- Credentials are no longer hardcoded.
- User input is validated.
- HTTP timeout is configured.
- HTTP response errors are handled.
```

> ![alt text](image-5.png)** 
> Show the original review and the successful second review to demonstrate the full feedback loop.

---

## 15. Business Value Demonstrated

This PoC demonstrates that AI can become part of the normal software development workflow without requiring developers to manually interact with an AI tool.

Main benefits:

- Faster first-level reviews
- Immediate developer feedback
- Consistent review criteria
- Earlier detection of security and reliability issues
- Reduced repetitive work for senior developers
- Less dependency on reviewer availability
- Human reviewers can focus on architecture, business logic and complex decisions

The AI remains an assistant. Final approval and accountability remain with the human reviewer.

---

## 16. Mapping the Demo to Azure DevOps

The demo uses GitHub because it provides a simple environment for the PoC.

The same architecture can be implemented in Azure DevOps:

```text
GitHub Demo                  Azure DevOps

Pull Request                 Pull Request
     ↓                            ↓
GitHub Actions              Azure Pipelines
     ↓                            ↓
PR Diff                     PR Diff
     ↓                            ↓
AI Model       → SAME →     AI Model
     ↓                            ↓
GitHub API                 Azure DevOps REST API
     ↓                            ↓
PR Comment                 PR Comment
```

The AI model and review logic can remain largely unchanged.

For an enterprise implementation, the AI provider can be selected according to security, governance, cost and organizational requirements, for example:

- Azure OpenAI / OpenAI
- Anthropic Claude
- Google Gemini
- Specialized AI code review platforms

---

## 17. Demo Message

A concise way to present the demo to the client:

> **Before a human reviewer even opens the Pull Request, AI has already performed the first level of review and identified potential security, reliability and maintainability issues.**

The objective is not to replace code reviewers, but to allow developers and senior engineers to spend more time on architecture, business logic and higher-value engineering decisions.

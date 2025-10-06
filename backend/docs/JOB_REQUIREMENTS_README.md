# Job Requirements Configuration

The AI resume screening pipeline reads structured requirements from `backend/config/job_requirements.json`. Adjust this file to tailor scoring for different roles—no code changes required.

## Fields

| Key | Type | Purpose |
| --- | --- | --- |
| `job_title` | string | Display name for the role. |
| `required_skills` | array | High-priority skills (weighted heavily). |
| `preferred_skills` | array | Nice-to-have skills that add bonus points. |
| `minimum_experience_years` | number | Required professional experience. |
| `required_education` | string | Minimum education requirement. |
| `scoring_weights` | object | Percentage weights for `technical_skills`, `experience`, and `education`; total must equal 100. |
| `passing_score` | number | Minimum overall score that counts as a pass. |

## Example

```json
{
  "job_title": "Backend Developer",
  "required_skills": [
    "Python",
    "Django",
    "PostgreSQL",
    "Docker",
    "REST API",
    "Git"
  ],
  "preferred_skills": [
    "Kubernetes",
    "Redis",
    "AWS",
    "CI/CD",
    "GraphQL"
  ],
  "minimum_experience_years": 3,
  "required_education": "Bachelor's degree in Computer Science or equivalent",
  "scoring_weights": {
    "technical_skills": 70,
    "experience": 20,
    "education": 10
  },
  "passing_score": 60
}
```

## Update Workflow

1. Open `backend/config/job_requirements.json` in a text editor.
2. Modify skills, weights, or thresholds.
3. Save the file—no server restart required.
4. Upload a resume to validate the changes.

## Tuning Tips

- Allocate 60–70% of the score to technical skills, 20–30% to experience, and the remainder to education.
- Keep the passing score aligned with hiring expectations (50 for moderate, 60+ for selective roles).
- Include synonyms in both `required_skills` and `preferred_skills` (for example, `"JavaScript"`, `"JS"`, `"Node.js"`).

## Validation Safeguards

The backend performs these checks automatically:

- File exists and is readable.
- JSON parses successfully.
- Required keys are present.

A descriptive HTTP error is returned if validation fails.

## Best Practices

- Track different role profiles using separate JSON files (e.g., keep an archive in `backend/config/examples/`).
- Commit only sample files; keep sensitive company-specific data outside version control.
- Backup the configuration before making large-scale edits.

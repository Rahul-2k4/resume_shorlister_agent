# Job Requirements Configuration

This file defines the job requirements used by the AI resume screening system.

## File Location
`job_requirements.json`

## How It Works
The system automatically loads this file when evaluating candidates. You can update these requirements anytime without changing the code!

## Configuration Fields

### `job_title` (string)
The title of the job position
- Example: `"Software Developer"`, `"Data Scientist"`, `"Full Stack Engineer"`

### `required_skills` (array)
List of essential skills candidates must have
- These are weighted heavily in the evaluation (70% by default)
- Example: `["Python", "FastAPI", "SQL", "Git"]`

### `preferred_skills` (array)
Nice-to-have skills that give candidates bonus points
- Combined with required_skills during evaluation
- Example: `["Kubernetes", "CI/CD", "MongoDB"]`

### `minimum_experience_years` (number)
Minimum years of professional experience required
- Example: `2` for 2 years, `5` for 5 years
- Used for experience scoring (20% weight by default)

### `required_education` (string)
Education qualification requirement
- Example: `"Bachelor's degree in Computer Science or related field"`
- Used for education scoring (10% weight by default)

### `scoring_weights` (object)
How different criteria are weighted in the final score
- `technical_skills`: Weight for skills match (default: 70%)
- `experience`: Weight for experience (default: 20%)
- `education`: Weight for education (default: 10%)
- **Total must equal 100%**

### `passing_score` (number)
Minimum score required to qualify
- Candidates scoring at or above this threshold:
  - ✅ Receive acceptance email
  - ✅ Get saved to Google Sheets
- Candidates below this threshold:
  - ❌ Receive rejection email
  - ❌ Not saved to Google Sheets
- Example: `50` (out of 100)

## Example Configuration

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

## How to Update

1. **Edit the file**: Open `job_requirements.json` in any text editor
2. **Modify values**: Change skills, experience, or passing score as needed
3. **Save the file**: That's it! No need to restart the server
4. **Test**: Upload a resume to see the new requirements in action

## Tips

- **Start broad, narrow down**: Begin with general skills, then add specific technologies
- **Balance weights**: Skills usually matter most (60-70%), followed by experience (20-30%) and education (10-20%)
- **Adjust passing score**: 
  - `50-60`: Moderate standards
  - `60-70`: High standards
  - `70+`: Very selective
- **Include variants**: Add variations of skills (e.g., "JavaScript", "JS", "Node.js")

## Validation

The system automatically validates:
- ✅ File exists and is readable
- ✅ JSON is properly formatted
- ✅ Required fields are present
- ❌ If validation fails, you'll see a clear error message

## Notes

- Changes take effect immediately (no server restart needed for most changes)
- The AI will use these requirements to evaluate all future resumes
- Keep the file in the same directory as `app.py`
- Backup your configuration before making major changes!

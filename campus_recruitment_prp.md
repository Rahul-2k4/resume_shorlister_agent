name: "AI-Powered Campus Recruitment Platform"
description: |
  End-to-end campus recruitment automation platform with AI-powered resume screening,
  candidate matching, and integrated feedback system for universities and corporate recruiters.

---

## Goal
Build a comprehensive campus recruitment platform that automates the hiring process through AI-powered resume screening, dynamic student profiles, university system integration, and personalized feedback loops to improve both recruiter efficiency and student placement success.

## Why
- **For Recruiters**: Overwhelmed with massive application volume and manual shortlisting inefficiencies
- **For Students**: Cannot effectively showcase diverse skills and interests for relevant roles, lack visibility into rejection reasons
- **For Universities**: Inefficient data integration leads to poor talent visibility and placement tracking
- **Business Impact**: Reduce recruitment cycle time, increase student engagement, improve match rates and hiring success

## What
An integrated platform that combines:
1. AI-powered resume parsing and candidate screening
2. Dynamic student profile system with skills, interests, and projects
3. University SIS integration for verified data accuracy
4. Automated personalized feedback system for rejected candidates
5. Real-time communication channels between recruiters and students
6. Analytics dashboard for tracking key recruitment metrics

### Success Criteria
- [ ] AI screening reduces manual review time by 70%
- [ ] Automated feedback provided within 24 hours of rejection
- [ ] Student profile completion rate >85%
- [ ] Successful integration with at least 3 university SIS systems
- [ ] Recruiter-student match accuracy >80%
- [ ] Platform handles 10,000+ concurrent applications
- [ ] Mobile and web platforms with real-time updates
- [ ] Average recruitment cycle time reduced by 50%

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window

- url: https://ai.pydantic.dev/
  why: Framework for building AI agents with type safety
  critical: Agent composition patterns, tool integration, multi-provider support

- url: https://fastapi.tiangolo.com/
  why: API framework for building REST endpoints
  section: Authentication, WebSocket support, background tasks
  critical: Async request handling, dependency injection

- url: https://docs.anthropic.com/claude/docs
  why: Claude AI API for resume screening and feedback generation
  section: Prompt engineering, structured outputs, streaming
  critical: Rate limits, token management, context window

- url: https://platform.openai.com/docs/guides/embeddings
  why: Vector embeddings for candidate-job matching
  critical: Embedding models, similarity search, batch processing

- url: https://docs.pydantic.dev/latest/
  why: Data validation and settings management
  section: V2 features, validators, custom types
  critical: Pydantic v2 breaking changes from v1

- url: https://sqlmodel.tiangolo.com/
  why: ORM combining SQLAlchemy and Pydantic
  critical: Async engine setup, relationship patterns

- file: examples/agent/agent.py
  why: Pattern for creating Pydantic AI agents with tools
  critical: Agent initialization, provider switching, error handling

- file: examples/agent/tools.py
  why: Tool function patterns for agents
  critical: Type hints, error handling, async patterns

- file: examples/cli.py
  why: CLI interface patterns using typer
  critical: Command structure, argument parsing, rich output
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: Pydantic v2 syntax differences
# - Use `model_validate()` not `parse_obj()`
# - Use `model_dump()` not `dict()`
# - Validators use `@field_validator` not `@validator`

# CRITICAL: SQLModel async patterns
# - Must use AsyncSession and async engine
# - Relationships require `Relationship()` from SQLModel
# - Use `selectinload()` for eager loading in async contexts

# CRITICAL: FastAPI dependency injection
# - Database sessions must be async context managers
# - Use `Depends()` for dependency injection
# - Background tasks should be used for email/notifications

# CRITICAL: AI Provider rate limits
# - Anthropic: 50 requests/minute (Tier 1)
# - OpenAI: 3,500 requests/minute, 90,000 tokens/minute
# - Implement exponential backoff with tenacity

# CRITICAL: File upload handling
# - Use streaming for large PDF/DOCX resumes
# - Virus scanning before processing
# - Store in S3/blob storage, not database

# GOTCHA: Vector similarity search
# - Normalize embeddings before storing
# - Use cosine similarity, not euclidean distance
# - Batch embedding generation for efficiency
```

### Current Codebase Tree
```bash
campus-recruitment/
├── .env.example
├── README.md
├── requirements.txt
├── pyproject.toml
└── venv_linux/          # Existing virtual environment
```

### Desired Codebase Tree
```bash
campus-recruitment/
├── .env.example                    # Environment variables template
├── .env                           # Local environment (gitignored)
├── README.md                      # Setup and usage documentation
├── requirements.txt               # Python dependencies
├── pyproject.toml                # Project configuration
├── venv_linux/                   # Virtual environment
│
├── src/
│   ├── __init__.py
│   │
│   ├── main.py                   # FastAPI application entry point
│   ├── config.py                 # Settings and configuration
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py           # Database connection and session
│   │   ├── models.py             # SQLModel ORM models
│   │   └── migrations/           # Alembic migrations
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── students.py       # Student profile endpoints
│   │   │   ├── recruiters.py     # Recruiter endpoints
│   │   │   ├── applications.py   # Application submission/tracking
│   │   │   ├── jobs.py           # Job posting endpoints
│   │   │   └── auth.py           # Authentication endpoints
│   │   ├── dependencies.py       # FastAPI dependencies
│   │   └── middleware.py         # Custom middleware
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── screening/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py          # Resume screening agent
│   │   │   ├── tools.py          # Screening tools (parse, score)
│   │   │   └── prompts.py        # Screening prompts
│   │   ├── matching/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py          # Candidate-job matching agent
│   │   │   ├── tools.py          # Matching tools (embeddings, similarity)
│   │   │   └── prompts.py        # Matching prompts
│   │   └── feedback/
│   │       ├── __init__.py
│   │       ├── agent.py          # Feedback generation agent
│   │       ├── tools.py          # Feedback tools
│   │       └── prompts.py        # Feedback prompts
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── resume_parser.py      # PDF/DOCX parsing service
│   │   ├── embedding_service.py  # Vector embedding service
│   │   ├── notification_service.py # Email/SMS notifications
│   │   ├── sis_integration.py    # University SIS integration
│   │   └── storage_service.py    # File storage (S3/local)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── student.py            # Student Pydantic schemas
│   │   ├── recruiter.py          # Recruiter Pydantic schemas
│   │   ├── application.py        # Application Pydantic schemas
│   │   ├── job.py                # Job posting Pydantic schemas
│   │   └── feedback.py           # Feedback Pydantic schemas
│   │
│   └── utils/
│       ├── __init__.py
│       ├── auth.py               # JWT token handling
│       ├── validators.py         # Custom validators
│       └── exceptions.py         # Custom exceptions
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── test_agents/
│   │   ├── test_screening_agent.py
│   │   ├── test_matching_agent.py
│   │   └── test_feedback_agent.py
│   ├── test_api/
│   │   ├── test_students.py
│   │   ├── test_recruiters.py
│   │   └── test_applications.py
│   └── test_services/
│       ├── test_resume_parser.py
│       └── test_embedding_service.py
│
└── cli/
    ├── __init__.py
    └── main.py                   # CLI for admin tasks
```

## Implementation Blueprint

### Data Models and Structure

```python
# src/db/models.py - Core database models

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    RECRUITER = "recruiter"
    UNIVERSITY_ADMIN = "university_admin"

class ApplicationStatus(str, Enum):
    SUBMITTED = "submitted"
    SCREENING = "screening"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    HIRED = "hired"

class User(SQLModel, table=True):
    """Base user model for authentication"""
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: UserRole
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class University(SQLModel, table=True):
    """University/Institution model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    domain: str = Field(unique=True)  # e.g., "stanford.edu"
    sis_api_endpoint: Optional[str] = None
    sis_api_key_encrypted: Optional[str] = None
    
    # Relationships
    students: List["Student"] = Relationship(back_populates="university")

class Student(SQLModel, table=True):
    """Student profile with skills and projects"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    university_id: int = Field(foreign_key="university.id")
    
    # Basic info
    full_name: str
    phone: Optional[str] = None
    graduation_year: int
    major: str
    gpa: Optional[float] = None
    
    # Profile data
    skills: str = Field(default="[]")  # JSON array of skills
    interests: str = Field(default="[]")  # JSON array of interests
    projects: str = Field(default="[]")  # JSON array of project descriptions
    resume_url: Optional[str] = None
    resume_embedding: Optional[str] = None  # Serialized vector
    
    # SIS verified data
    is_verified: bool = Field(default=False)
    verification_date: Optional[datetime] = None
    
    # Relationships
    university: Optional[University] = Relationship(back_populates="students")
    applications: List["Application"] = Relationship(back_populates="student")

class Company(SQLModel, table=True):
    """Company/Recruiter organization"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    domain: str
    industry: Optional[str] = None
    
    # Relationships
    recruiters: List["Recruiter"] = Relationship(back_populates="company")
    jobs: List["Job"] = Relationship(back_populates="company")

class Recruiter(SQLModel, table=True):
    """Recruiter profile"""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    company_id: int = Field(foreign_key="company.id")
    
    full_name: str
    phone: Optional[str] = None
    position: str
    
    # Relationships
    company: Optional[Company] = Relationship(back_populates="recruiters")
    jobs: List["Job"] = Relationship(back_populates="recruiter")

class Job(SQLModel, table=True):
    """Job posting"""
    id: Optional[int] = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="company.id")
    recruiter_id: int = Field(foreign_key="recruiter.id")
    
    title: str
    description: str
    requirements: str  # JSON array of requirements
    preferred_skills: str  # JSON array of skills
    location: str
    job_type: str  # full-time, internship, etc.
    salary_range: Optional[str] = None
    
    # AI matching data
    job_embedding: Optional[str] = None  # Serialized vector
    
    # Status
    is_active: bool = Field(default=True)
    posted_at: datetime = Field(default_factory=datetime.utcnow)
    deadline: Optional[datetime] = None
    
    # Relationships
    company: Optional[Company] = Relationship(back_populates="jobs")
    recruiter: Optional[Recruiter] = Relationship(back_populates="jobs")
    applications: List["Application"] = Relationship(back_populates="job")

class Application(SQLModel, table=True):
    """Student job application"""
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id", index=True)
    job_id: int = Field(foreign_key="job.id", index=True)
    
    status: ApplicationStatus = Field(default=ApplicationStatus.SUBMITTED)
    cover_letter: Optional[str] = None
    
    # AI screening results
    ai_score: Optional[float] = None  # 0-100 match score
    ai_reasoning: Optional[str] = None
    match_highlights: Optional[str] = None  # JSON array
    
    # Timestamps
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    screened_at: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: Optional[Student] = Relationship(back_populates="applications")
    job: Optional[Job] = Relationship(back_populates="applications")
    feedback: Optional["Feedback"] = Relationship(back_populates="application")

class Feedback(SQLModel, table=True):
    """Automated feedback for candidates"""
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", unique=True)
    
    # AI generated feedback
    strengths: str  # JSON array of strengths
    areas_for_improvement: str  # JSON array
    suggestions: str  # JSON array of actionable suggestions
    encouragement: str  # Personalized encouragement message
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    was_sent: bool = Field(default=False)
    sent_at: Optional[datetime] = None
    
    # Relationships
    application: Optional[Application] = Relationship(back_populates="feedback")
```

```python
# src/schemas/student.py - Pydantic schemas for API

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional
from datetime import datetime

class SkillCreate(BaseModel):
    """Individual skill with proficiency"""
    name: str = Field(..., min_length=1, max_length=100)
    proficiency: str = Field(..., pattern="^(beginner|intermediate|advanced|expert)$")

class ProjectCreate(BaseModel):
    """Student project"""
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10, max_length=2000)
    technologies: List[str]
    url: Optional[str] = None
    
    @field_validator('technologies')
    @classmethod
    def validate_technologies(cls, v):
        if len(v) == 0:
            raise ValueError('At least one technology required')
        return v

class StudentProfileCreate(BaseModel):
    """Create student profile"""
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    university_domain: str
    graduation_year: int = Field(..., ge=2024, le=2030)
    major: str = Field(..., min_length=2, max_length=100)
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    phone: Optional[str] = None
    skills: List[SkillCreate]
    interests: List[str]
    projects: List[ProjectCreate]

class StudentProfileResponse(BaseModel):
    """Student profile response"""
    id: int
    full_name: str
    email: str
    university_name: str
    graduation_year: int
    major: str
    gpa: Optional[float]
    skills: List[SkillCreate]
    interests: List[str]
    projects: List[ProjectCreate]
    is_verified: bool
    profile_completion: int  # 0-100 percentage
    created_at: datetime
    
    model_config = {"from_attributes": True}
```

### Implementation Tasks

```yaml
Task 1: Project Setup and Configuration
  CREATE .env.example:
    - Add all required environment variables
    - Include API keys for Claude, OpenAI
    - Database connection strings
    - JWT secret key template
    - File storage configuration
  
  CREATE src/config.py:
    - PATTERN: Use pydantic-settings BaseSettings
    - Load from .env using python-dotenv
    - Validate all required settings on startup
    - Include AI provider configurations with rate limits
  
  CREATE requirements.txt:
    - fastapi[all]>=0.104.0
    - pydantic-ai>=0.0.13
    - sqlmodel>=0.0.14
    - alembic>=1.12.0
    - python-jose[cryptography]
    - passlib[bcrypt]
    - python-multipart
    - anthropic
    - openai
    - PyPDF2
    - python-docx
    - pytest>=7.4.0
    - pytest-asyncio
    - httpx
    - ruff
    - mypy

Task 2: Database Setup
  CREATE src/db/database.py:
    - PATTERN: Async SQLAlchemy engine
    - Create async session factory
    - Implement get_session() dependency for FastAPI
    - CRITICAL: Use AsyncSession and async with statements
  
  CREATE src/db/models.py:
    - Implement all models from blueprint above
    - CRITICAL: Use SQLModel for ORM + Pydantic integration
    - Add proper indexes on frequently queried fields
    - PRESERVE: Use datetime.utcnow for all timestamps
  
  SETUP Alembic:
    - alembic init src/db/migrations
    - Configure env.py for async SQLModel
    - Create initial migration with all tables

Task 3: Authentication & Authorization
  CREATE src/utils/auth.py:
    - Implement JWT token creation and verification
    - Password hashing with bcrypt
    - PATTERN: Use python-jose for JWT
  
  CREATE src/api/routes/auth.py:
    - POST /auth/register (student/recruiter registration)
    - POST /auth/login (JWT token generation)
    - POST /auth/refresh (token refresh)
    - GET /auth/me (current user info)
    - PATTERN: Return JWT in response body, not cookies
  
  CREATE src/api/dependencies.py:
    - get_current_user() dependency
    - require_role(role: UserRole) dependency
    - get_db_session() dependency
    - CRITICAL: Handle token expiry gracefully

Task 4: Resume Parser Service
  CREATE src/services/resume_parser.py:
    - FUNCTION: parse_pdf_resume(file_bytes: bytes) -> dict
    - FUNCTION: parse_docx_resume(file_bytes: bytes) -> dict
    - Extract: name, email, phone, education, skills, experience
    - PATTERN: Use PyPDF2 for PDFs, python-docx for DOCX
    - CRITICAL: Handle malformed files gracefully
    - Return structured dict with extracted sections
  
  TEST: Create test_resume_parser.py
    - Test with sample PDF and DOCX resumes
    - Test with corrupted files (should not crash)
    - Test extraction accuracy

Task 5: Vector Embedding Service
  CREATE src/services/embedding_service.py:
    - FUNCTION: generate_resume_embedding(text: str) -> List[float]
    - FUNCTION: generate_job_embedding(description: str, requirements: str) -> List[float]
    - FUNCTION: calculate_similarity(vec1: List[float], vec2: List[float]) -> float
    - PATTERN: Use OpenAI text-embedding-ada-002
    - CRITICAL: Normalize embeddings before storing
    - CRITICAL: Batch API calls to respect rate limits
    - CACHE: Implement simple in-memory cache for repeated texts
  
  TEST: Create test_embedding_service.py
    - Test embedding generation
    - Test similarity calculation (known similar texts should score >0.7)
    - Test batch processing

Task 6: Resume Screening Agent
  CREATE src/agents/screening/prompts.py:
    - SYSTEM_PROMPT: Define agent role as resume screener
    - Include criteria: skills match, experience relevance, education fit
    - Instruct to return structured output with score and reasoning
  
  CREATE src/agents/screening/tools.py:
    - FUNCTION: extract_resume_sections(resume_text: str) -> dict
    - FUNCTION: match_skills(candidate_skills: List[str], required_skills: List[str]) -> dict
    - Use @tool decorator from pydantic-ai
  
  CREATE src/agents/screening/agent.py:
    - PATTERN: Follow examples/agent/agent.py structure
    - Initialize Agent with Claude or OpenAI
    - Register tools from tools.py
    - FUNCTION: screen_application(resume_text: str, job_description: str) -> ScreeningResult
    - CRITICAL: Include temperature=0.3 for consistent scoring
    - Return: score (0-100), reasoning, match_highlights
  
  TEST: Create test_screening_agent.py
    - Mock AI responses
    - Test with matching resume (should score >70)
    - Test with non-matching resume (should score <40)
    - Test error handling when AI unavailable

Task 7: Matching Agent with Embeddings
  CREATE src/agents/matching/prompts.py:
    - SYSTEM_PROMPT: Define agent as candidate-job matcher
    - Instruct to consider both semantic similarity and explicit requirements
  
  CREATE src/agents/matching/tools.py:
    - FUNCTION: get_similar_candidates(job_embedding: List[float], top_k: int) -> List[dict]
    - FUNCTION: get_suitable_jobs(student_embedding: List[float], top_k: int) -> List[dict]
    - Query database for vectors with high cosine similarity
  
  CREATE src/agents/matching/agent.py:
    - PATTERN: Multi-step agent reasoning
    - Step 1: Get semantically similar candidates via embeddings
    - Step 2: AI agent ranks based on detailed criteria
    - FUNCTION: find_best_matches(job_id: int, limit: int) -> List[MatchResult]
    - CRITICAL: Combine vector similarity (60%) + AI scoring (40%)
  
  TEST: Create test_matching_agent.py
    - Test with known good matches
    - Test ranking consistency

Task 8: Feedback Generation Agent
  CREATE src/agents/feedback/prompts.py:
    - SYSTEM_PROMPT: Empathetic career advisor persona
    - Instruct to provide constructive, actionable feedback
    - CRITICAL: Always end with encouragement
  
  CREATE src/agents/feedback/tools.py:
    - FUNCTION: identify_gaps(candidate_skills: List[str], required_skills: List[str]) -> List[str]
    - FUNCTION: suggest_improvements(gaps: List[str], career_goal: str) -> List[str]
  
  CREATE src/agents/feedback/agent.py:
    - FUNCTION: generate_feedback(application: Application, job: Job, student: Student) -> Feedback
    - Structure: strengths (3-5 points), improvements (2-4 points), suggestions (3-5 actionable items)
    - CRITICAL: Personalize based on student's year, major, existing skills
    - Tone: encouraging, specific, actionable
  
  TEST: Create test_feedback_agent.py
    - Test feedback quality (should have all sections)
    - Test tone (no negative language)
    - Test personalization

Task 9: Student Profile API
  CREATE src/api/routes/students.py:
    - POST /students/profile (create profile with resume upload)
    - GET /students/profile/me (get own profile)
    - PUT /students/profile/me (update profile)
    - POST /students/profile/resume (upload/update resume)
    - GET /students/applications (list own applications)
    - PATTERN: Use FastAPI File upload for resumes
    - CRITICAL: Validate file type (PDF/DOCX only)
    - CRITICAL: Generate embedding after profile creation/update
  
  INTEGRATION:
    - After resume upload: parse_resume -> extract data -> generate_embedding
    - Store file in storage_service, save URL in database
    - Background task to generate embedding (non-blocking)

Task 10: Job Posting API
  CREATE src/api/routes/jobs.py:
    - POST /jobs (create job posting - recruiter only)
    - GET /jobs (list active jobs with filters)
    - GET /jobs/{id} (get job details)
    - PUT /jobs/{id} (update job - recruiter only)
    - DELETE /jobs/{id} (deactivate job - recruiter only)
    - GET /jobs/{id}/matches (get AI-matched candidates - recruiter only)
    - CRITICAL: Generate job embedding on creation
    - CRITICAL: Use role-based access control
  
  INTEGRATION:
    - On job creation: generate_job_embedding -> store in database
    - GET /jobs/{id}/matches: use matching agent to find top candidates

Task 11: Application Submission & Screening
  CREATE src/api/routes/applications.py:
    - POST /applications (submit application)
    - GET /applications/{id} (get application status)
    - GET /applications/{id}/feedback (get AI feedback if rejected)
    - PATTERN: Use FastAPI BackgroundTasks for async screening
  
  INTEGRATION:
    - On submission:
      1. Create application record (status=SUBMITTED)
      2. Trigger background task: screen_application
      3. Return immediate confirmation
    - Background screening:
      1. Run screening_agent
      2. Update application with score and reasoning
      3. If rejected: generate_feedback -> create Feedback record -> send notification
      4. Update status to SHORTLISTED or REJECTED
  
  CREATE background_tasks.py:
    - FUNCTION: process_application_screening(application_id: int)
    - CRITICAL: Handle all errors gracefully, log failures
    - CRITICAL: Update application status even if AI fails (manual review)

Task 12: Notification Service
  CREATE src/services/notification_service.py:
    - FUNCTION: send_application_status_update(student_email: str, status: str, job_title: str)
    - FUNCTION: send_feedback_email(student_email: str, feedback: Feedback)
    - FUNCTION: send_new_match_notification(recruiter_email: str, student_name: str, score: int)
    - PATTERN: Use SendGrid or SMTP for emails
    - PATTERN: Template-based emails with HTML
    - CRITICAL: Queue emails, don't block API responses
    - FALLBACK: Log to file if email service unavailable

Task 13: University SIS Integration
  CREATE src/services/sis_integration.py:
    - FUNCTION: verify_student(email: str, university_id: int) -> bool
    - FUNCTION: fetch_student_data(email: str, university_id: int) -> dict
    - PATTERN: API client with retry logic
    - CRITICAL: Store API credentials encrypted
    - CRITICAL: Implement per-university adapter pattern (different APIs)
    - Mock implementation for universities without API
  
  CREATE src/api/routes/students.py endpoint:
    - POST /students/profile/verify (trigger SIS verification)
    - INTEGRATION: Call sis_integration service, update is_verified flag

Task 14: Analytics Dashboard Backend
  CREATE src/api/routes/analytics.py:
    - GET /analytics/recruiter/overview (recruiter dashboard)
      - Total applications, screening stats, hired count
      - Average time-to-hire, top skills in hired candidates
    - GET /analytics/student/progress (student dashboard)
      - Application count by status
      - Average score, feedback summary
      - Suggested skill improvements
    - PATTERN: Aggregation queries with SQLAlchemy
    - CRITICAL: Cache expensive queries (5 min TTL)

Task 15: CLI for Admin Tasks
  CREATE cli/main.py:
    - PATTERN: Follow examples/cli.py structure with typer
    - COMMAND: seed-data (populate sample data for testing)
    - COMMAND: verify-embeddings (check embedding consistency)
    - COMMAND: reprocess-applications (re-run screening if needed)
    - COMMAND: generate-report (export analytics to CSV)
    - Use rich for formatted output

Task 16: Main Application Setup
  CREATE src/main.py:
    - Initialize FastAPI app
    - Include all routers with proper prefixes
    - Add CORS middleware for web/mobile clients
    - Add rate limiting middleware
    - Add request logging middleware
    - Include exception handlers for custom exceptions
    - CRITICAL: Startup event to initialize database connection
    - CRITICAL: Shutdown event to close connections
  
  PATTERN:
    app = FastAPI(title="Campus Recruitment Platform", version="1.0.0")
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(students.router, prefix="/api/students", tags=["students"])
    # ... other routers
```

### Pseudocode for Critical Flows

```python
# Task 11 - Application Screening Flow (MOST CRITICAL)

# src/api/routes/applications.py
@router.post("/applications", status_code=201)
async def submit_application(
    application_data: ApplicationCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    """
    Submit job application and trigger AI screening
    
    Flow:
    1. Validate student has complete profile with resume
    2. Check not already applied to this job
    3. Create application record (status=SUBMITTED)
    4. Queue background screening task
    5. Return immediate success response
    """
    # CRITICAL: Validate student profile is complete
    student = await get_student_by_user_id(db, current_user.id)
    if not student.resume_url:
        raise HTTPException(400, "Resume required before applying")
    if not student.resume_embedding:
        raise HTTPException(400, "Profile still processing, try again in 1 minute")
    
    # GOTCHA: Check for duplicate application
    existing = await check_existing_application(db, student.id, application_data.job_id)
    if existing:
        raise HTTPException(400, "Already applied to this job")
    
    # Create application record
    application = Application(
        student_id=student.id,
        job_id=application_data.job_id,
        cover_letter=application_data.cover_letter,
        status=ApplicationStatus.SUBMITTED
    )
    db.add(application)
    await db.commit()
    await db.refresh(application)
    
    # CRITICAL: Queue background screening (non-blocking)
    background_tasks.add_task(
        process_application_screening,
        application.id
    )
    
    # Return immediate confirmation
    return {
        "message": "Application submitted successfully",
        "application_id": application.id,
        "status": "submitted",
        "estimated_screening_time": "2-5 minutes"
    }


# src/services/background_tasks.py
async def process_application_screening(application_id: int):
    """
    Background task to screen application with AI
    
    Flow:
    1. Load application, student, job from DB
    2. Run screening agent with resume + job description
    3. Update application with AI score and reasoning
    4. If rejected: generate feedback and send notification
    5. If shortlisted: notify recruiter
    """
    async with get_db_session() as db:
        try:
            # PATTERN: Load all required data with relationships
            application = await db.get(
                Application,
                application_id,
                options=[
                    selectinload(Application.student),
                    selectinload(Application.job)
                ]
            )
            
            if not application:
                logger.error(f"Application {application_id} not found")
                return
            
            # Update status to screening
            application.status = ApplicationStatus.SCREENING
            await db.commit()
            
            # CRITICAL: Load resume content from storage
            resume_content = await storage_service.get_file_content(
                application.student.resume_url
            )
            
            # CRITICAL: Run AI screening agent
            from agents.screening.agent import screening_agent
            
            screening_result = await screening_agent.screen_application(
                resume_text=resume_content,
                job_description=application.job.description,
                job_requirements=json.loads(application.job.requirements),
                student_profile={
                    "skills": json.loads(application.student.skills),
                    "projects": json.loads(application.student.projects),
                    "gpa": application.student.gpa,
                    "major": application.student.major
                }
            )
            
            # Update application with screening results
            application.ai_score = screening_result.score
            application.ai_reasoning = screening_result.reasoning
            application.match_highlights = json.dumps(screening_result.highlights)
            application.screened_at = datetime.utcnow()
            
            # CRITICAL: Determine if shortlisted (threshold = 70)
            if screening_result.score >= 70:
                application.status = ApplicationStatus.SHORTLISTED
                
                # Notify recruiter of strong match
                await notification_service.send_new_match_notification(
                    recruiter_email=application.job.recruiter.user.email,
                    student_name=application.student.full_name,
                    job_title=application.job.title,
                    score=screening_result.score
                )
            else:
                application.status = ApplicationStatus.REJECTED
                
                # CRITICAL: Generate personalized feedback
                from agents.feedback.agent import feedback_agent
                
                feedback_data = await feedback_agent.generate_feedback(
                    application=application,
                    job=application.job,
                    student=application.student,
                    screening_result=screening_result
                )
                
                # Create feedback record
                feedback = Feedback(
                    application_id=application.id,
                    strengths=json.dumps(feedback_data.strengths),
                    areas_for_improvement=json.dumps(feedback_data.improvements),
                    suggestions=json.dumps(feedback_data.suggestions),
                    encouragement=feedback_data.encouragement_message
                )
                db.add(feedback)
                
                # Send feedback email
                await notification_service.send_feedback_email(
                    student_email=application.student.user.email,
                    student_name=application.student.full_name,
                    job_title=application.job.title,
                    feedback=feedback_data
                )
                
                feedback.was_sent = True
                feedback.sent_at = datetime.utcnow()
            
            application.updated_at = datetime.utcnow()
            await db.commit()
            
            logger.info(
                f"Screening completed for application {application_id}: "
                f"score={screening_result.score}, status={application.status}"
            )
            
        except Exception as e:
            # CRITICAL: Never let screening failure block the application
            logger.error(f"Screening failed for application {application_id}: {str(e)}")
            
            # Set to manual review
            application.status = ApplicationStatus.SUBMITTED
            application.ai_reasoning = f"Automatic screening failed: {str(e)[:200]}"
            await db.commit()


# src/agents/screening/agent.py
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from .prompts import SCREENING_SYSTEM_PROMPT
from .tools import extract_key_skills, calculate_experience_match
from pydantic import BaseModel

class ScreeningResult(BaseModel):
    """Structured screening output"""
    score: float  # 0-100
    reasoning: str
    highlights: list[str]  # Key matching points
    concerns: list[str]  # Potential red flags or gaps

# PATTERN: Initialize agent with specific model
screening_agent = Agent(
    model=AnthropicModel("claude-sonnet-4-5-20250929"),
    system_prompt=SCREENING_SYSTEM_PROMPT,
    result_type=ScreeningResult
)

# Register tools
@screening_agent.tool
async def extract_key_skills(resume_text: str) -> dict:
    """
    Extract and categorize technical and soft skills from resume
    
    Returns:
        dict with 'technical', 'soft', and 'domain' skill lists
    """
    # PATTERN: Use regex + keyword matching for skill extraction
    # CRITICAL: Normalize skill names (e.g., "JavaScript" vs "javascript")
    pass

@screening_agent.tool  
async def calculate_experience_match(
    student_projects: list[dict],
    required_experience: str
) -> dict:
    """
    Calculate how well student's project experience matches requirements
    
    Returns:
        dict with match_score (0-1) and matching_projects list
    """
    # PATTERN: Semantic matching of project descriptions
    pass

async def screen_application(
    resume_text: str,
    job_description: str,
    job_requirements: list[str],
    student_profile: dict
) -> ScreeningResult:
    """
    Main screening function - coordinates agent execution
    
    CRITICAL: Set temperature=0.3 for consistency
    CRITICAL: Include retry logic for API failures
    """
    from tenacity import retry, stop_after_attempt, wait_exponential
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def _screen_with_retry():
        result = await screening_agent.run(
            f"""
            Screen this candidate for the job position.
            
            RESUME:
            {resume_text[:4000]}  # Truncate to fit context
            
            JOB DESCRIPTION:
            {job_description}
            
            REQUIREMENTS:
            {json.dumps(job_requirements)}
            
            STUDENT PROFILE:
            - GPA: {student_profile.get('gpa', 'N/A')}
            - Major: {student_profile['major']}
            - Skills: {json.dumps(student_profile['skills'])}
            - Projects: {len(student_profile['projects'])} projects
            
            Provide a comprehensive screening with score (0-100) and detailed reasoning.
            """,
            model_settings={"temperature": 0.3}
        )
        return result.data
    
    return await _screen_with_retry()


# src/agents/feedback/agent.py  
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from .prompts import FEEDBACK_SYSTEM_PROMPT
from pydantic import BaseModel

class FeedbackData(BaseModel):
    """Structured feedback output"""
    strengths: list[str]  # 3-5 positive points
    improvements: list[str]  # 2-4 constructive areas
    suggestions: list[str]  # 3-5 actionable next steps
    encouragement_message: str  # Personalized closing

feedback_agent = Agent(
    model=AnthropicModel("claude-sonnet-4-5-20250929"),
    system_prompt=FEEDBACK_SYSTEM_PROMPT,
    result_type=FeedbackData
)

async def generate_feedback(
    application: Application,
    job: Job,
    student: Student,
    screening_result: ScreeningResult
) -> FeedbackData:
    """
    Generate personalized, constructive feedback for rejected candidates
    
    CRITICAL: Tone must be encouraging and growth-focused
    CRITICAL: Suggestions must be specific and actionable
    """
    result = await feedback_agent.run(
        f"""
        Generate constructive feedback for a student who was not selected.
        
        STUDENT CONTEXT:
        - Name: {student.full_name}
        - Year: {student.graduation_year}
        - Major: {student.major}
        - GPA: {student.gpa}
        - Current Skills: {json.loads(student.skills)}
        
        JOB APPLIED FOR:
        - Title: {job.title}
        - Company: {job.company.name}
        - Requirements: {json.loads(job.requirements)}
        
        SCREENING RESULTS:
        - Score: {screening_result.score}/100
        - Reasoning: {screening_result.reasoning}
        - Concerns: {screening_result.concerns}
        
        Create feedback that:
        1. Acknowledges their strengths genuinely
        2. Identifies specific skill gaps professionally
        3. Provides actionable steps to improve
        4. Encourages continued job search with optimism
        
        Remember: This student is early in their career. Be supportive.
        """,
        model_settings={"temperature": 0.7}  # Higher for more personalized tone
    )
    
    return result.data


# src/agents/matching/agent.py
from pydantic_ai import Agent
from .tools import get_candidates_by_embedding_similarity
from pydantic import BaseModel

class MatchResult(BaseModel):
    """Single candidate match result"""
    student_id: int
    student_name: str
    match_score: float  # Combined score (0-100)
    embedding_similarity: float  # Raw cosine similarity
    ai_reasoning: str
    key_strengths: list[str]

class MatchingResults(BaseModel):
    """List of matched candidates"""
    matches: list[MatchResult]
    total_candidates_evaluated: int

matching_agent = Agent(
    model=AnthropicModel("claude-sonnet-4-5-20250929"),
    result_type=MatchingResults
)

@matching_agent.tool
async def get_candidates_by_embedding_similarity(
    job_id: int,
    top_k: int = 50
) -> list[dict]:
    """
    Retrieve top K candidates by vector similarity
    
    CRITICAL: Use cosine similarity on normalized embeddings
    CRITICAL: Only return students with complete, verified profiles
    """
    async with get_db_session() as db:
        # Get job embedding
        job = await db.get(Job, job_id)
        if not job.job_embedding:
            raise ValueError("Job embedding not generated")
        
        job_vec = json.loads(job.job_embedding)
        
        # PATTERN: Query with vector similarity
        # In production: Use pgvector or Pinecone for efficient search
        # For MVP: Calculate in Python (inefficient but works)
        
        query = select(Student).where(
            Student.is_verified == True,
            Student.resume_embedding.isnot(None)
        )
        result = await db.execute(query)
        students = result.scalars().all()
        
        # Calculate similarities
        candidates = []
        for student in students:
            student_vec = json.loads(student.resume_embedding)
            similarity = calculate_cosine_similarity(job_vec, student_vec)
            
            candidates.append({
                "student_id": student.id,
                "student_name": student.full_name,
                "similarity": similarity,
                "skills": json.loads(student.skills),
                "gpa": student.gpa,
                "major": student.major,
                "projects": json.loads(student.projects)
            })
        
        # Sort by similarity and return top K
        candidates.sort(key=lambda x: x["similarity"], reverse=True)
        return candidates[:top_k]

async def find_best_matches(job_id: int, limit: int = 10) -> MatchingResults:
    """
    Find best candidate matches using hybrid approach
    
    Flow:
    1. Get top 50 candidates by embedding similarity (fast)
    2. AI agent re-ranks based on detailed analysis (slow but accurate)
    3. Return top N matches with reasoning
    
    CRITICAL: Combine vector similarity (60%) + AI evaluation (40%)
    """
    # Step 1: Vector search narrows candidates
    top_candidates = await get_candidates_by_embedding_similarity(job_id, top_k=50)
    
    # Load job details
    async with get_db_session() as db:
        job = await db.get(Job, job_id)
    
    # Step 2: AI re-ranks with detailed evaluation
    result = await matching_agent.run(
        f"""
        Rank these candidates for the job position.
        
        JOB:
        - Title: {job.title}
        - Description: {job.description}
        - Requirements: {json.loads(job.requirements)}
        - Preferred Skills: {json.loads(job.preferred_skills)}
        
        CANDIDATES (already filtered by semantic similarity):
        {json.dumps(top_candidates, indent=2)}
        
        For each candidate:
        1. Evaluate fit based on skills, experience, and potential
        2. Assign a match score (0-100)
        3. Provide specific reasoning for the score
        4. Highlight 2-3 key strengths
        
        Return top {limit} candidates ranked by match score.
        Consider both current skills AND learning potential.
        """,
        model_settings={"temperature": 0.2}
    )
    
    # CRITICAL: Combine scores (60% vector, 40% AI)
    final_matches = []
    for match in result.data.matches[:limit]:
        # Find original similarity score
        original = next(c for c in top_candidates if c["student_id"] == match.student_id)
        
        # Weighted combination
        combined_score = (
            original["similarity"] * 0.6 +
            (match.match_score / 100) * 0.4
        ) * 100
        
        match.match_score = combined_score
        final_matches.append(match)
    
    # Sort by combined score
    final_matches.sort(key=lambda x: x.match_score, reverse=True)
    
    return MatchingResults(
        matches=final_matches,
        total_candidates_evaluated=len(top_candidates)
    )
```

## Integration Points

```yaml
FILE_STORAGE:
  provider: "AWS S3 or local filesystem"
  configuration:
    - Resume files stored with path: uploads/resumes/{user_id}/{timestamp}_{filename}
    - Max file size: 5MB
    - Allowed types: application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document
  integration:
    - Upload on student profile creation/update
    - Generate presigned URLs for recruiter access (S3 only)

DATABASE_MIGRATIONS:
  - migration: "001_initial_schema"
    tables: [User, University, Student, Company, Recruiter, Job, Application, Feedback]
  - migration: "002_add_embedding_columns"
    changes:
      - ALTER TABLE students ADD COLUMN resume_embedding TEXT
      - ALTER TABLE jobs ADD COLUMN job_embedding TEXT
      - CREATE INDEX idx_student_verified ON students(is_verified, resume_embedding)
  - migration: "003_add_application_indexes"
    changes:
      - CREATE INDEX idx_app_status ON applications(status, applied_at)
      - CREATE INDEX idx_app_student ON applications(student_id, status)

EMAIL_TEMPLATES:
  - file: templates/emails/application_submitted.html
    variables: [student_name, job_title, company_name, expected_response_time]
  - file: templates/emails/application_rejected_with_feedback.html
    variables: [student_name, job_title, strengths, improvements, suggestions, encouragement]
  - file: templates/emails/new_match_notification.html
    variables: [recruiter_name, student_name, job_title, match_score, profile_url]

API_RATE_LIMITS:
  anthropic:
    requests_per_minute: 50
    tokens_per_minute: 40000
    retry_strategy: exponential_backoff
  openai:
    requests_per_minute: 3500
    tokens_per_minute: 90000
    retry_strategy: exponential_backoff
  
CACHING_STRATEGY:
  embeddings:
    - Cache resume embeddings for 30 days
    - Cache job embeddings until job is updated
  analytics:
    - Cache dashboard queries for 5 minutes
    - Invalidate on new applications

WEBSOCKET_EVENTS:
  - event: "application_status_updated"
    payload: {application_id, new_status, timestamp}
    subscribers: [student_dashboard]
  - event: "new_match_found"
    payload: {job_id, student_id, match_score}
    subscribers: [recruiter_dashboard]
```

## Validation Loop

### Level 1: Code Quality & Type Safety
```bash
# Run these FIRST before any testing
source venv_linux/bin/activate

# Format code
ruff format src/ tests/

# Lint and auto-fix
ruff check src/ tests/ --fix

# Type checking (CRITICAL for Pydantic models)
mypy src/ --strict

# Expected: No errors. Fix any issues before proceeding.
```

### Level 2: Unit Tests
```python
# tests/test_agents/test_screening_agent.py
import pytest
from unittest.mock import Mock, patch
from src.agents.screening.agent import screen_application, ScreeningResult

@pytest.mark.asyncio
async def test_screening_high_match():
    """Test screening with well-matched candidate"""
    resume_text = """
    John Doe
    Computer Science, Stanford University
    GPA: 3.8
    Skills: Python, React, PostgreSQL, Docker
    Projects:
    - Built e-commerce platform with 10k users
    - Developed ML model for fraud detection
    """
    
    job_description = "Full-stack developer with Python and React experience"
    job_requirements = ["Python", "React", "Database experience"]
    student_profile = {
        "gpa": 3.8,
        "major": "Computer Science",
        "skills": [{"name": "Python", "proficiency": "advanced"}],
        "projects": [{"title": "E-commerce platform"}]
    }
    
    result = await screen_application(
        resume_text=resume_text,
        job_description=job_description,
        job_requirements=job_requirements,
        student_profile=student_profile
    )
    
    assert isinstance(result, ScreeningResult)
    assert result.score >= 70, f"Expected high score for good match, got {result.score}"
    assert len(result.highlights) >= 2
    assert len(result.reasoning) > 50

@pytest.mark.asyncio
async def test_screening_poor_match():
    """Test screening with poorly matched candidate"""
    resume_text = """
    Jane Smith
    English Literature, UC Berkeley
    GPA: 3.5
    Skills: Creative writing, Research
    """
    
    job_description = "Senior backend engineer with 5+ years Go experience"
    job_requirements = ["Go", "Kubernetes", "Microservices", "5+ years experience"]
    
    result = await screen_application(
        resume_text=resume_text,
        job_description=job_description,
        job_requirements=job_requirements,
        student_profile={"gpa": 3.5, "major": "English", "skills": [], "projects": []}
    )
    
    assert result.score < 50, f"Expected low score for poor match, got {result.score}"
    assert len(result.concerns) > 0

@pytest.mark.asyncio  
async def test_screening_api_failure_retry():
    """Test retry logic when AI API fails"""
    with patch('src.agents.screening.agent.screening_agent.run') as mock_run:
        # Fail twice, succeed third time
        mock_run.side_effect = [
            Exception("API timeout"),
            Exception("Rate limit"),
            Mock(data=ScreeningResult(score=75, reasoning="Good match", highlights=[], concerns=[]))
        ]
        
        result = await screen_application(
            resume_text="test",
            job_description="test",
            job_requirements=[],
            student_profile={}
        )
        
        assert mock_run.call_count == 3
        assert result.score == 75

# tests/test_api/test_applications.py
import pytest
from httpx import AsyncClient
from src.main import app

@pytest.mark.asyncio
async def test_submit_application_success(async_client: AsyncClient, auth_headers: dict):
    """Test successful application submission"""
    # Assume student profile and job exist from fixtures
    application_data = {
        "job_id": 1,
        "cover_letter": "I am excited to apply..."
    }
    
    response = await async_client.post(
        "/api/applications",
        json=application_data,
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "application_id" in data
    assert data["status"] == "submitted"
    assert "estimated_screening_time" in data

@pytest.mark.asyncio
async def test_submit_application_without_resume(async_client: AsyncClient, auth_headers_no_resume: dict):
    """Test application submission fails without resume"""
    response = await async_client.post(
        "/api/applications",
        json={"job_id": 1},
        headers=auth_headers_no_resume
    )
    
    assert response.status_code == 400
    assert "Resume required" in response.json()["detail"]

@pytest.mark.asyncio
async def test_duplicate_application(async_client: AsyncClient, auth_headers: dict):
    """Test cannot apply twice to same job"""
    application_data = {"job_id": 1, "cover_letter": "Test"}
    
    # First application succeeds
    response1 = await async_client.post("/api/applications", json=application_data, headers=auth_headers)
    assert response1.status_code == 201
    
    # Second application fails
    response2 = await async_client.post("/api/applications", json=application_data, headers=auth_headers)
    assert response2.status_code == 400
    assert "Already applied" in response2.json()["detail"]

# Run all tests
# pytest tests/ -v --asyncio-mode=auto --cov=src --cov-report=html
```

### Level 3: Integration Tests
```bash
# Start the application
source venv_linux/bin/activate
uvicorn src.main:app --reload --port 8000

# In another terminal, run integration tests:

# Test 1: Create student profile with resume
curl -X POST http://localhost:8000/api/students/profile \
  -H "Content-Type: multipart/form-data" \
  -F "full_name=John Doe" \
  -F "email=john@stanford.edu" \
  -F "university_domain=stanford.edu" \
  -F "graduation_year=2025" \
  -F "major=Computer Science" \
  -F "resume=@sample_resume.pdf"
# Expected: 201 Created with profile_id

# Test 2: Submit application
curl -X POST http://localhost:8000/api/applications \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"job_id": 1, "cover_letter": "I am interested..."}'
# Expected: 201 Created with application_id

# Test 3: Wait for screening (check logs)
tail -f logs/app.log | grep "Screening completed"
# Expected: See screening completion within 2-5 minutes

# Test 4: Check application status
curl http://localhost:8000/api/applications/1 \
  -H "Authorization: Bearer $TOKEN"
# Expected: Status updated to "shortlisted" or "rejected" with ai_score

# Test 5: Get feedback (if rejected)
curl http://localhost:8000/api/applications/1/feedback \
  -H "Authorization: Bearer $TOKEN"
# Expected: Feedback object with strengths, improvements, suggestions
```

### Level 4: Load Testing (Optional for MVP)
```bash
# Install locust for load testing
pip install locust

# Test concurrent application submissions
locust -f tests/load/test_applications.py --host=http://localhost:8000
# Expected: >100 requests/second without errors
# Expected: API response time <500ms (excluding AI screening)
```

## Final Validation Checklist

### Functionality
- [ ] Student can create profile and upload resume
- [ ] Resume is parsed and embedding generated
- [ ] Recruiter can post jobs with embeddings
- [ ] Student can submit applications
- [ ] AI screening runs automatically in background
- [ ] Screening completes within 5 minutes
- [ ] Rejected candidates receive personalized feedback within 24 hours
- [ ] Feedback is constructive and actionable
- [ ] Shortlisted candidates appear in recruiter dashboard
- [ ] Recruiter can view AI match scores and reasoning
- [ ] Matching agent finds relevant candidates for jobs
- [ ] Email notifications sent for status changes

### Code Quality
- [ ] All tests pass: `pytest tests/ -v --asyncio-mode=auto`
- [ ] No linting errors: `ruff check src/ tests/`
- [ ] No type errors: `mypy src/ --strict`
- [ ] Code coverage >80%: `pytest --cov=src --cov-report=term`
- [ ] All files <500 lines
- [ ] All functions have docstrings
- [ ] No hardcoded secrets (use .env)

### Performance
- [ ] Application submission responds in <500ms
- [ ] AI screening completes in <5 minutes for 90% of applications
- [ ] Dashboard loads in <2 seconds
- [ ] System handles 100 concurrent users
- [ ] Embedding generation is batched efficiently

### Security
- [ ] JWT authentication on all protected routes
- [ ] Password hashing with bcrypt
- [ ] File upload validation (type, size, virus scan)
- [ ] SQL injection prevention (use ORM, no raw queries)
- [ ] Rate limiting on API endpoints
- [ ] CORS configured correctly
- [ ] API keys stored in environment variables, not code

### Documentation
- [ ] README.md has complete setup instructions
- [ ] .env.example has all required variables
- [ ] API endpoints documented (consider adding OpenAPI/Swagger)
- [ ] Example requests/responses provided
- [ ] Known limitations documented

---

## Anti-Patterns to Avoid

- ❌ Don't store embeddings in database as JSON strings in production - use pgvector extension
- ❌ Don't process AI screening synchronously - always use background tasks
- ❌ Don't send emails synchronously - queue them
- ❌ Don't store resumes in database - use blob storage (S3/Azure)
- ❌ Don't use the same AI model call for screening and feedback - separate agents
- ❌ Don't skip validation of user inputs - always validate with Pydantic
- ❌ Don't catch all exceptions with bare `except:` - be specific
- ❌ Don't store passwords in plain text - always hash
- ❌ Don't commit .env files - always gitignore
- ❌ Don't make AI calls without retry logic - APIs can be unreliable
- ❌ Don't use high temperature for scoring (use 0.2-0.3) - use higher (0.6-0.8) for creative feedback
- ❌ Don't forget to normalize embeddings before similarity calculation
- ❌ Don't block API responses waiting for AI - return immediately and process async

---

## Success Metrics (Post-Launch)

### Key Performance Indicators
- **Recruitment Efficiency**: 50% reduction in time-to-hire
- **Screening Accuracy**: >80% AI screening decisions aligned with recruiter manual review
- **Candidate Engagement**: >60% of rejected candidates read feedback
- **Platform Adoption**: >75% of recruiters use AI matching feature
- **Student Satisfaction**: >4.0/5.0 rating on feedback usefulness
- **System Reliability**: >99% uptime, <1% failed screenings

### Data to Track
- Average screening time
- Distribution of AI scores (should be normal distribution)
- Feedback open rate and read time
- Conversion rate from shortlisted to hired
- Number of appeals/disputes on AI decisions
- API error rates and retry counts

---

## Next Steps After MVP

1. **Advanced Matching**: Add collaborative filtering based on historical hiring data
2. **Interview Scheduling**: Integrate calendar for automated scheduling
3. **Video Interviews**: Add AI-powered video interview analysis
4. **Skill Assessments**: Integrate coding challenges and technical assessments
5. **Mobile Apps**: Native iOS/Android apps with push notifications
6. **Multi-language**: Support non-English resumes and feedback
7. **Advanced Analytics**: ML models to predict hiring success
8. **Bias Detection**: Monitor and mitigate algorithmic bias in screening

---

## Confidence Score: 9/10

This PRP is comprehensive and includes:
✅ Complete data models and schemas
✅ Detailed implementation steps with priorities
✅ Critical pseudocode for complex flows
✅ Integration patterns and gotchas
✅ Comprehensive testing strategy
✅ Validation loops at multiple levels
✅ Security and performance considerations
✅ Clear success criteria

The 9/10 score reflects high confidence that following this PRP will result in a working MVP. The missing 1 point accounts for:
- SIS integration complexity varies by university
- AI model performance may need tuning based on real data
- Load testing results may require optimization

**Recommendation**: Execute this PRP in phases, validating each phase before proceeding to the next. Start with Phase 1 (Tasks 1-6), validate thoroughly, then move to Phase 2 (Tasks 7-11), and finally Phase 3 (Tasks 12-16).
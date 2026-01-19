# Resume Shortlister Agent

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20S3-orange.svg)](https://aws.amazon.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Demo](https://img.shields.io/badge/🤗%20Live%20Demo-HuggingFace-yellow.svg)](https://huggingface.co/spaces/Rahul7009/resume-shortlister-demo)

> **An AI-powered resume screening pipeline that reduced HR screening time by 80%, processing 1,000+ documents in a distributed computing environment.**

## Live Demo

🚀 **[Try the Live Demo on HuggingFace Spaces](https://huggingface.co/spaces/Rahul7009/resume-shortlister-demo)**

Upload a resume and job description to see the AI-powered screening in action!

## Problem Statement

HR teams spend an average of **7 seconds** per resume, yet manually screening hundreds of applications takes **hours**. This project automates the initial screening process using NLP and machine learning, allowing recruiters to focus on qualified candidates.

## Key Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Screening Time (per 100 resumes) | 5+ hours | 1 hour | **80% reduction** |
| Processing Capacity | Manual | 1,000+ docs | **Scalable** |
| Deployment Cycle | Hours | <10 min | **Automated CI/CD** |

## Architecture

```
                                    +------------------+
                                    |   React Frontend |
                                    +--------+---------+
                                             |
                                             v
+----------------+    +------------------+   +------------------+
|  Resume Upload | -> |   FastAPI Server | ->|   NLP Pipeline   |
|    (PDF/DOCX)  |    |   (REST API)     |   | (OCR + Ranking)  |
+----------------+    +--------+---------+   +--------+---------+
                               |                      |
                               v                      v
                      +------------------+   +------------------+
                      |   AWS S3 Storage |   |  ML Ranking Model|
                      +------------------+   +------------------+
```

## Tech Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | Python, FastAPI, Pydantic |
| **Frontend** | React, HTML, CSS |
| **AI/ML** | OCR (Tesseract), NLP (spaCy), scikit-learn |
| **Cloud** | AWS EC2, S3, Lambda |
| **DevOps** | Docker, GitHub Actions, CI/CD |
| **Database** | PostgreSQL |

## Features

- **Automated Resume Parsing**: Extract text from PDF/DOCX using OCR
- **NLP-Based Analysis**: Skill extraction, experience parsing, keyword matching
- **Intelligent Ranking**: ML-powered candidate scoring based on job requirements
- **RESTful API**: Clean API endpoints for integration
- **Scalable Architecture**: Containerized deployment on AWS EC2
- **Real-time Processing**: Async processing for batch uploads

## Quick Start

### Prerequisites
- Python 3.9+
- Docker (optional)
- AWS account (for deployment)

### Local Development

```bash
# Clone the repository
git clone https://github.com/Rahul-2k4/resume_shorlister_agent.git
cd resume_shorlister_agent

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend setup (new terminal)
cd frontend
npm install
npm start
```

### Docker Deployment

```bash
docker-compose up --build
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload resume(s) for processing |
| `GET` | `/api/candidates` | Get ranked candidate list |
| `GET` | `/api/candidates/{id}` | Get candidate details |
| `POST` | `/api/job-description` | Set job requirements for matching |

## Project Structure

```
resume_shorlister_agent/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models/              # Pydantic models
│   ├── services/            # Business logic
│   │   ├── ocr.py          # OCR processing
│   │   ├── nlp.py          # NLP pipeline
│   │   └── ranking.py      # ML ranking
│   └── requirements.txt
├── frontend/
│   ├── src/
│   └── package.json
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions
└── README.md
```

## Performance

- **Throughput**: 1,000+ resumes processed in batch mode
- **Latency**: <2s average per resume
- **Accuracy**: 85%+ skill extraction accuracy
- **Uptime**: 99.9% on AWS EC2

## Future Improvements

- [ ] Add support for LinkedIn profile parsing
- [ ] Implement bias detection in screening
- [ ] Add multi-language support
- [ ] Create dashboard for analytics

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) first.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Rahul Tripathi**
- GitHub: [@Rahul-2k4](https://github.com/Rahul-2k4)
- LinkedIn: [rahul-tripathi-335347353](https://linkedin.com/in/rahul-tripathi-335347353)
- Email: rahultripathi7009@gmail.com

---

*Built with passion for efficient hiring*

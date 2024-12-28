touch# Certificate Generator API

A FastAPI-based service that generates certificates for multiple companies/websites. The API allows different organizations to maintain their own certificate templates, fonts, and styling while using a common infrastructure for certificate generation.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Adding New Companies](#adding-new-companies)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## Features

- Multi-company support
- Custom certificate templates per company
- Configurable fonts and text positioning
- Simple REST API interface
- Built with FastAPI for high performance
- Next.js integration support

## Project Structure

```
certificates_api/
├── main.py
├── requirements.txt
├── README.md
├── config/
│   └── company_settings.py
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── certificate_routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── certificate_service.py
│   └── models/
│       ├── __init__.py
│       └── certificate_models.py
├── static/
│   ├── templates/
│   │   ├── dewise/
│   │   │   └── certificate.png
│   │   └── other_company/
│   │       └── certificate.png
│   └── fonts/
│       ├── dewise/
│       │   ├── title.ttf
│       │   └── text.ttf
│       └── other_company/
│           ├── title.ttf
│           └── text.ttf
└── tests/
    └── test_certificate_generator.py
```

## Prerequisites

- Python 3.8+
- pip
- virtualenv or venv
- Node.js and npm (for Next.js frontend)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/skaleway/skaleway-certificate-generator.git
cd skaleway-certificate-generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```


## Configuration

1. Verify the configuration in `config/company_settings.py`:
```python
STATIC_DIR = Path("static")
TEMPLATES_DIR = STATIC_DIR / "templates"
FONTS_DIR = STATIC_DIR / "fonts"
```

## Usage

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. The API will be available at `http://localhost:8000`

3. Access the API documentation at `http://localhost:8000/redoc`

4. Generate a certificate (example using curl):
```bash
curl -X POST "http://localhost:8000/dewise/generate-certificate/" \
-H "Content-Type: application/json" \
-d '{
  "name": "John Doe",
  "course_name": "Solar Installation",
  "created_at": "2024-10-29T12:00:00"
}' --output certificate.png 
```

### Next.js Integration

To integrate with a Next.js frontend:

1. Install axios in your Next.js project:
```bash
npm install axios
```

2. Create an API service file:
```typescript
// services/certificateService.ts
import axios from 'axios';

export const generateCertificate = async (companyId, data) => {
  const response = await axios.post(
    `/api/certificate/${companyId}/generate-certificate/`,
    data
  );
  return response.data;
};
```

## Adding New Companies

See [COMPANY_SETUP.md](COMPANY_SETUP.md) for detailed instructions on adding new companies to the system.

## API Documentation

### Endpoints

#### Generate Certificate
```
POST /{company_id}/generate-certificate/
```

Request Body:
```json
{
  "name": "string",
  "course_name": "string",
  "created_at": "string" // optional, ISO format
}
```

Response:
- Content-Type: image/png
- File download response


## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## Troubleshooting

### Common Issues

1. **Template Not Found Error**
   - Verify that the template image exists in the correct directory
   - Check file permissions

2. **Font Not Found Error**
   - Ensure fonts are placed in the correct company folder
   - Verify font file names match configuration

3. **Invalid Company ID**
   - Check if company is properly configured in `company_settings.py`
   - Verify company ID in API request

### Support

For additional support:
1. Check the [issues](https://github.com/skaleway/skaleway-certificate-generator/issues) page
2. Create a new issue with detailed information about your problem
3. Contact the development team

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

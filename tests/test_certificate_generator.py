import shutil

import pytest
from fastapi.testclient import TestClient
from PIL import Image, ImageFont, ImageDraw
from datetime import datetime
import io
import os
from pathlib import Path

from main import app
from app.services.certificate_service import CertificateGenerator
from config.company_settings import COMPANY_SETTINGS

# Initialize test client
client = TestClient(app)

# Test data
TEST_COMPANY_ID = "test_company"
TEST_DATA = {
    "name": "John Doe",
    "course_name": "Test Course",
    "created_at": "2024-10-29T12:00:00"
}


@pytest.fixture(scope="session")
def setup_test_assets():
    """Create test company assets (template and fonts) for testing"""
    # Create test directories
    templates_dir = Path("static/templates") / TEST_COMPANY_ID
    fonts_dir = Path("static/fonts") / TEST_COMPANY_ID

    templates_dir.mkdir(parents=True, exist_ok=True)
    fonts_dir.mkdir(parents=True, exist_ok=True)
    print(templates_dir)
    # Create a test certificate template
    img = Image.new('RGB', (800, 600), color='white')
    img.save(templates_dir / "certificate.png")

    # Copy a test font (using Arial or any system font for testing)
    # Note: In a real implementation, you'd need to provide a test font file
    test_font_path = fonts_dir / "test_font.ttf"
    if not test_font_path.exists():
        # Define the source font path (adjust this path to where your font is located)
        # For example, on Windows, you might find Arial at:
        source_font_path = Path("tests/test-arial.ttf")  # Adjust for your OS and font

        # Check if the source font exists
        if source_font_path.exists():
            # Copy the font to the test font path
            shutil.copy(source_font_path, test_font_path)
        pass

    # Add test company settings
    COMPANY_SETTINGS[TEST_COMPANY_ID] = {
        "template_path": templates_dir / "certificate.png",
        "fonts": {
            "title": fonts_dir / "test_font.ttf",
            "text": fonts_dir / "test_font.ttf"
        },
        "text_positions": {
            "name": {"x": 0.5, "y": 0.4},
            "course": {"x": 0.5, "y": 0.5},
            "date": {"x": 0.5, "y": 0.6}
        },
        "font_sizes": {
            "name": 60,
            "course": 40,
            "date": 30
        },
        "text_colors": {
            "name": "black",
            "course": "black",
            "date": "black"
        }
    }

    yield

    # Cleanup
    try:
        os.remove(templates_dir / "certificate.png")
        os.remove(fonts_dir / "test_font.ttf")
        os.rmdir(templates_dir)
        os.rmdir(fonts_dir)
    except Exception as e:
        print(f"Cleanup error: {e}")


class TestCertificateGenerator:
    """Unit tests for CertificateGenerator class"""

    def test_init_valid_company(self, setup_test_assets):
        """Test initialization with valid company ID"""
        generator = CertificateGenerator(TEST_COMPANY_ID)
        assert generator.settings == COMPANY_SETTINGS[TEST_COMPANY_ID]

    def test_init_invalid_company(self):
        """Test initialization with invalid company ID"""
        with pytest.raises(ValueError):
            CertificateGenerator("nonexistent_company")

    def test_generate_certificate(self, setup_test_assets):
        """Test certificate generation with valid data"""
        generator = CertificateGenerator(TEST_COMPANY_ID)
        certificate_bytes = generator.generate(
            "John Doe",
            "Test Course",
            datetime.strptime("2024-10-29T12:00:00", "%Y-%m-%dT%H:%M:%S")
        )

        # Verify the output is valid PNG data
        with io.BytesIO(certificate_bytes) as bio:
            img = Image.open(bio)
            assert img.format == "PNG"
            assert img.size == (800, 600)  # Match test template size


class TestCertificateAPI:
    """Integration tests for Certificate API endpoints"""

    def test_generate_certificate_endpoint(self, setup_test_assets):
        """Test the certificate generation endpoint with valid data"""
        response = client.post(
            f"/{TEST_COMPANY_ID}/generate-certificate/",
            json=TEST_DATA
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

        # Verify the response contains valid PNG data
        with io.BytesIO(response.content) as bio:
            img = Image.open(bio)
            assert img.format == "PNG"

    def test_invalid_company_id(self):
        """Test the endpoint with an invalid company ID"""
        response = client.post(
            "/nonexistent_company/generate-certificate/",
            json=TEST_DATA
        )
        assert response.status_code == 400

    def test_invalid_request_data(self, setup_test_assets):
        """Test the endpoint with invalid request data"""
        invalid_data = {
            "name": "",  # Empty name
            "course_name": "Test Course"
        }

        response = client.post(
            f"/{TEST_COMPANY_ID}/generate-certificate/",
            json=invalid_data
        )
        assert response.status_code == 422  # Validation error

    def test_missing_required_fields(self, setup_test_assets):
        """Test the endpoint with missing required fields"""
        incomplete_data = {
            "name": "John Doe"
            # Missing course_name
        }

        response = client.post(
            f"/{TEST_COMPANY_ID}/generate-certificate/",
            json=incomplete_data
        )
        assert response.status_code == 422


class TestCertificateSettings:
    """Tests for certificate settings and configuration"""

    def test_company_settings_structure(self, setup_test_assets):
        """Test the structure of company settings"""
        settings = COMPANY_SETTINGS[TEST_COMPANY_ID]

        required_keys = {
            "template_path",
            "fonts",
            "text_positions",
            "font_sizes",
            "text_colors"
        }

        assert all(key in settings for key in required_keys)
        assert all(key in settings["text_positions"] for key in ["name", "course", "date"])
        assert all(key in settings["font_sizes"] for key in ["name", "course", "date"])

    def test_template_path_exists(self, setup_test_assets):
        """Test that template path exists for test company"""
        template_path = COMPANY_SETTINGS[TEST_COMPANY_ID]["template_path"]
        assert template_path.exists()

    def test_font_paths_exist(self, setup_test_assets):
        """Test that font paths exist for test company"""
        fonts = COMPANY_SETTINGS[TEST_COMPANY_ID]["fonts"]
        for font_path in fonts.values():
            assert font_path.exists()


class TestErrorHandling:
    """Tests for error handling scenarios"""

    def test_invalid_date_format(self, setup_test_assets):
        """Test handling of invalid date format"""
        invalid_data = {
            **TEST_DATA,
            "created_at": "invalid-date"
        }

        response = client.post(
            f"/{TEST_COMPANY_ID}/generate-certificate/",
            json=invalid_data
        )
        assert response.status_code == 422

    def test_very_long_name(self, setup_test_assets):
        """Test handling of extremely long input text"""
        long_data = {
            **TEST_DATA,
            "name": "A" * 1000  # Very long name
        }

        response = client.post(
            f"/{TEST_COMPANY_ID}/generate-certificate/",
            json=long_data
        )
        # Should either handle it gracefully or return an appropriate error
        assert response.status_code in [200, 400]

    def test_special_characters(self, setup_test_assets):
        """Test handling of special characters in input"""
        special_chars_data = {
            **TEST_DATA,
            "name": "John @ Doe 特別な文字"
        }

        response = client.post(
            f"/{TEST_COMPANY_ID}/generate-certificate/",
            json=special_chars_data
        )
        assert response.status_code == 200


def test_concurrent_requests(setup_test_assets):
    """Test handling of concurrent certificate generation requests"""
    import concurrent.futures

    def make_request():
        return client.post(
            f"/{TEST_COMPANY_ID}/generate-certificate/",
            json=TEST_DATA
        )

    # Test with 5 concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(5)]
        responses = [f.result() for f in futures]

    # All requests should be successful
    assert all(response.status_code == 200 for response in responses)
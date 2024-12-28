from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import tempfile
from datetime import datetime

from starlette.background import BackgroundTask

from app.models.certificate_models import CertificateRequest
from app.models.certificate_models import CertificateRequestModel
from app.models.tic_certificate_models import NewFlyerRequest
from app.services.certificate_service import CertificateGenerator
from app.services.certificate_service import TICFlyerGenerator
import os

router = APIRouter()


@router.post("/{templateId}/generate-certificates/")
async def create_certificate(company_id: str, request: CertificateRequestModel):
    try:
        # Initialize generator for company
        generator = CertificateGenerator(company_id)

        # Use current datetime if not provided
        created_at = request.created_at or datetime.now()

        # Generate certificate
        certificate_bytes = generator.generate(
            request.name,
            request.course_name,
            created_at
        )

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            tmp.write(certificate_bytes)
            tmp_path = tmp.name

        # Return file and ensure cleanup
        return FileResponse(
            tmp_path,
            media_type="image/png",
            filename=f"{company_id}_certificate_{request.name.replace(' ', '_')}.png",
            background=BackgroundTask(lambda: os.unlink(tmp_path))
        )


    except ValueError as e:
        # Handle specific value errors that indicate bad input
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, KeyError) as e:
        # Handle cases where the input data structure is incorrect
        raise HTTPException(status_code=422, detail="Invalid input data structure.")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/{company_id}/generate-certificate/")
async def create_certificate(company_id: str, request: CertificateRequest):
    try:
        # Initialize generator for company
        generator = CertificateGenerator(company_id)

        # Use current datetime if not provided
        created_at = request.created_at or datetime.now()

        # Generate certificate
        certificate_bytes = generator.generate(
            request.name,
            request.course_name,
            created_at
        )

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            tmp.write(certificate_bytes)
            tmp_path = tmp.name

        # Return file and ensure cleanup
        return FileResponse(
            tmp_path,
            media_type="image/png",
            filename=f"{company_id}_certificate_{request.name.replace(' ', '_')}.png",
            background=BackgroundTask(lambda: os.unlink(tmp_path))
        )


    except ValueError as e:
        # Handle specific value errors that indicate bad input
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, KeyError) as e:
        # Handle cases where the input data structure is incorrect
        raise HTTPException(status_code=422, detail="Invalid input data structure.")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{company_id}/generate-new-flyer/")
async def create_new_flyer(company_id: str, request: NewFlyerRequest):
    try:
        # Initialize generator for company
        generator = TICFlyerGenerator(company_id)

        # Generate flyer
        flyer_bytes = generator.generate(
            request.name,
            request.template_type,
            request.images
        )

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(flyer_bytes)
            tmp_path = tmp.name

        # Return file and ensure cleanup
        return FileResponse(
            tmp_path,
            media_type="image/png",
            filename=f"{company_id}_flyer_{request.name.replace(' ', '_')}.png",
            background=BackgroundTask(lambda: os.unlink(tmp_path)),
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except (TypeError, KeyError) as e:
        raise HTTPException(status_code=422, detail="Invalid input data structure.")
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
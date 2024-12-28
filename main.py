from fastapi import FastAPI
from app.routes import certificate_routes
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Multi-Company Certificate Generator API",
    redirect_slashes=False,
    
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routes
app.include_router(certificate_routes.router, tags=["certificates"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
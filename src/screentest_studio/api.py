from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from screentest_studio.schemas import HealthResponse, ScreenTestRequest, ScreenTestResponse
from screentest_studio.service import ScreenTestConfigurationError, run_screen_test

load_dotenv()


def _cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(
    title="ScreenTest Studio Agent API",
    version="0.1.0",
    description="Production API for the CrewAI ScreenTest Studio agent crew.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="screentest-studio-agent-api",
        crew_runtime="crewai",
    )


@app.post("/screen-tests", response_model=ScreenTestResponse)
async def create_screen_test(request: ScreenTestRequest) -> ScreenTestResponse:
    try:
        return await asyncio.to_thread(run_screen_test, request)
    except ScreenTestConfigurationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"ScreenTest Studio agents failed: {exc}",
        ) from exc

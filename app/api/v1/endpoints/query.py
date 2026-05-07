from fastapi import APIRouter
from app.models.request_models import QueryRequest
from app.orchestrator.workflow import AgentOrchestrator
from app.core.logger import logger

router = APIRouter()


@router.post("/query")
async def process_query(request: QueryRequest):
    logger.info(f"Received query: {request.query}, session: {request.session_id}")

    result = await AgentOrchestrator.run(
        request.query,
        request.session_id   # ✅ FIXED
    )

    return {
        "status": "completed",
        "data": result
    }
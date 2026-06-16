from __future__ import annotations

import json
import os
import re
import time
import uuid
from typing import Any

from screentest_studio.crew import ScreentestStudioCrew
from screentest_studio.schemas import ScreenTestRequest, ScreenTestResponse


class ScreenTestConfigurationError(RuntimeError):
    pass


def run_screen_test(request: ScreenTestRequest) -> ScreenTestResponse:
    if not os.getenv("OPENAI_API_KEY"):
        raise ScreenTestConfigurationError(
            "OPENAI_API_KEY is required to run the CrewAI agents in production."
        )

    started_at = time.perf_counter()
    run_id = str(uuid.uuid4())
    inputs = {
        "brand_pitch": request.brand_pitch,
        "brand_url": str(request.brand_url) if request.brand_url else "",
    }

    crew_output = ScreentestStudioCrew().crew().kickoff(inputs=inputs)
    raw_output = _stringify_crew_output(crew_output)
    task_outputs = _extract_task_outputs(crew_output)
    parsed_result = _extract_json(raw_output)

    return ScreenTestResponse(
        run_id=run_id,
        status="completed",
        elapsed_seconds=round(time.perf_counter() - started_at, 2),
        result=parsed_result,
        raw_output=raw_output,
        task_outputs=task_outputs,
    )


def _stringify_crew_output(crew_output: Any) -> str:
    for attr in ("raw", "final_output"):
        value = getattr(crew_output, attr, None)
        if value:
            return str(value)

    json_dict = getattr(crew_output, "json_dict", None)
    if json_dict:
        return json.dumps(json_dict, indent=2)

    pydantic_output = getattr(crew_output, "pydantic", None)
    if pydantic_output:
        return pydantic_output.model_dump_json(indent=2)

    return str(crew_output)


def _extract_task_outputs(crew_output: Any) -> list[dict[str, Any]]:
    outputs: list[dict[str, Any]] = []
    for task_output in getattr(crew_output, "tasks_output", []) or []:
        outputs.append(
            {
                "name": getattr(task_output, "name", None)
                or getattr(task_output, "task_name", None),
                "description": getattr(task_output, "description", None),
                "raw": getattr(task_output, "raw", None) or str(task_output),
            }
        )
    return outputs


def _extract_json(text: str) -> dict[str, Any] | None:
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {"items": parsed}
    except json.JSONDecodeError:
        pass

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fenced:
        try:
            return json.loads(fenced.group(1))
        except json.JSONDecodeError:
            pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            parsed = json.loads(text[start : end + 1])
            return parsed if isinstance(parsed, dict) else {"items": parsed}
        except json.JSONDecodeError:
            return None
    return None

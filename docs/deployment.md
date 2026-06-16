# Deployment Notes

## Why Two Deployments?

The CrewAI run can take longer than a typical frontend serverless request. The production path keeps the agent runtime in a containerized FastAPI service on TrueFoundry, while Vercel serves the interactive UI.

## TrueFoundry

TrueFoundry is used for the Python service because it can run a long-lived container, expose a public HTTP port, and manage resources for the agent workload.

The included `deploy.py` follows the TrueFoundry Python SDK service pattern:

- `Build` with `LocalSource`
- `DockerFileBuild`
- exposed HTTP `Port` on `8000`
- CPU and memory resource requests
- env-based secrets and CORS configuration

## Vercel

Vercel hosts only the Next.js UI in `web`. The browser calls the TrueFoundry API through `NEXT_PUBLIC_AGENT_API_URL`.

## Production Checklist

1. Add `OPENAI_API_KEY` as a secret in the TrueFoundry deployment environment.
2. Set `CORS_ORIGINS` to the exact Vercel domain.
3. Deploy the FastAPI service with `python deploy.py`.
4. Verify `GET /health` on the TrueFoundry URL.
5. Set `NEXT_PUBLIC_AGENT_API_URL` in Vercel.
6. Deploy the `web` project to Vercel.
7. Run one end-to-end pitch from the deployed web URL.

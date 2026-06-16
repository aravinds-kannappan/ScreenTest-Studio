# ScreenTest Studio

ScreenTest Studio is a production-oriented web app for pre-screening startup Reels before a founder films them.

It uses:

- CrewAI for the multi-agent creative and audience simulation workflow
- TrueFoundry for the deployed Python agent API
- Vercel for the Next.js web app

## Architecture

```text
Vercel Next.js app
  -> POST /screen-tests on the TrueFoundry service
      -> CrewAI Builder Agent
      -> CrewAI Audience Panel Agent
      -> CrewAI Fixer Agent
      -> structured JSON report for charts, scene cards, and rewrite diffs
```

## Agent Crew

The crew lives in `src/screentest_studio`:

- Builder Agent: turns the brand pitch and optional URL into a brand profile and Reel timeline.
- Audience Panel Agent: creates three synthetic target customers and predicts retention.
- Fixer Agent: rewrites only the weakest scene and re-screens the timeline.

## Local Agent API

```bash
cp .env.example .env
# Add OPENAI_API_KEY to .env
pip install -e .
uvicorn screentest_studio.api:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://localhost:8000/health
```

Run the crew:

```bash
curl -X POST http://localhost:8000/screen-tests \
  -H "Content-Type: application/json" \
  -d '{"brand_pitch":"ScreenTest Studio helps seed-stage founders test short-form video ideas before filming.","brand_url":null}'
```

## Local Web App

```bash
cd web
cp .env.example .env.local
# Set NEXT_PUBLIC_AGENT_API_URL=http://localhost:8000
npm install
npm run dev
```

Open `http://localhost:3000`.

## TrueFoundry Deploy

Install the deploy dependency locally:

```bash
pip install -r requirements-deploy.txt
```

Set deployment env vars:

```bash
export TRUEFOUNDRY_WORKSPACE_FQN="<your-workspace-fqn>"
export OPENAI_API_KEY="<your-openai-key>"
export CORS_ORIGINS="http://localhost:3000,https://your-vercel-domain.vercel.app"
# Optional if your TrueFoundry workspace has a configured host
export TRUEFOUNDRY_SERVICE_HOST="screentest-api.example.com"
```

Deploy:

```bash
python deploy.py
```

The service exposes:

- `GET /health`
- `POST /screen-tests`

## Vercel Deploy

Deploy the `web` directory as the Vercel project root.

Set:

```bash
NEXT_PUBLIC_AGENT_API_URL=https://your-truefoundry-service-url
```

Then deploy from Vercel or with:

```bash
cd web
vercel --prod
```

## Environment

Backend:

- `OPENAI_API_KEY`: required for CrewAI to run the OpenAI model.
- `SCREENTEST_LLM_MODEL`: optional, defaults to `openai/gpt-4o-mini`.
- `CORS_ORIGINS`: comma-separated list of allowed frontend origins.

Frontend:

- `NEXT_PUBLIC_AGENT_API_URL`: public URL of the TrueFoundry FastAPI service.

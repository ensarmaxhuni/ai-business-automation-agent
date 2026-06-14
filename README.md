# AI Business Automation Agent

An enterprise-grade AI business operating assistant built with Python, Streamlit, OpenAI, Pydantic, Pandas, and Plotly. The application automates executive productivity workflows, generates consulting-grade outputs, analyzes meetings, drafts professional communication, supports research, and plans business process automation.

## Product Positioning

This project is designed as a professional AI portfolio application that feels like a commercial SaaS platform rather than a simple chatbot demo.

Core capabilities:

- Executive AI Assistant for strategy, proposals, recommendations, and action plans
- Meeting Intelligence for summaries, decisions, action items, risks, and executive briefs
- Professional Email Generator with multiple stakeholder-ready versions and copy controls
- Business Report Generator for consulting-style reports
- AI Research Analyst for market and strategic briefs
- SWOT Analysis Generator
- Business Automation Planner with process diagnosis, savings estimates, tools, and roadmap
- Analytics dashboard with Plotly charts
- Session history manager
- Export to PDF, DOCX, and TXT
- Dark premium SaaS interface with glassmorphism styling

## Project Structure

```text
ai-business-automation-agent/
  app.py
  pages/
    executive_assistant.py
    meeting_intelligence.py
    email_generator.py
    report_generator.py
    research_analyst.py
    swot_generator.py
    automation_planner.py
  utils/
    analytics.py
    config.py
    export.py
    llm.py
    prompts.py
    schemas.py
    ui.py
  assets/
    logo.png
  .streamlit/
    config.toml
  requirements.txt
  README.md
  .env.example
  .gitignore
```

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Upgrade packaging tools and install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Create a `.env` file from the example:

```bash
copy .env.example .env
```

4. Add your OpenAI API key:

```text
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4.1-mini
DEMO_MODE=false
```

5. Run the application:

```bash
streamlit run app.py
```

## Environment Variables

| Variable | Description | Default |
| --- | --- | --- |
| `OPENAI_API_KEY` | OpenAI API key used for generation | Required for live AI |
| `OPENAI_MODEL` | OpenAI model for structured generation | `gpt-4.1-mini` |
| `OPENAI_TEMPERATURE` | Generation creativity | `0.35` |
| `OPENAI_MAX_TOKENS` | Maximum response tokens | `2200` |
| `DEMO_MODE` | Enables deterministic sample output | `false` |
| `APP_ENV` | Runtime environment name | `development` |
| `LOG_LEVEL` | Python logging level | `INFO` |
| `OUTPUT_DIR` | Output directory for future persistence | `outputs` |

If `OPENAI_API_KEY` is missing, the app automatically runs in demo mode so the interface remains portfolio-ready during local review. The app reads configuration from environment variables, a local `.env` file, or Streamlit secrets.

## Streamlit Cloud Deployment

1. Push this folder to a GitHub repository.
2. In Streamlit Community Cloud, create a new app.
3. Set the entrypoint to:

```text
app.py
```

4. Add secrets in Streamlit Cloud:

```toml
OPENAI_API_KEY = "sk-..."
OPENAI_MODEL = "gpt-4.1-mini"
OPENAI_TEMPERATURE = "0.35"
OPENAI_MAX_TOKENS = "2200"
DEMO_MODE = "false"
```

5. Deploy.

The `.streamlit/config.toml` file provides the dark theme and minimal toolbar configuration for a polished hosted experience.

## Architecture Notes

- `utils/llm.py` centralizes AI provider integration, JSON parsing, error handling, and demo mode.
- `utils/prompts.py` keeps all module prompts and reusable prompt templates in a typed registry.
- `utils/schemas.py` defines Pydantic models for outputs, prompt specs, and history.
- `utils/export.py` contains PDF, DOCX, and TXT exporters.
- `utils/analytics.py` maintains session history and Plotly analytics.
- `utils/ui.py` applies the custom SaaS interface and reusable rendering components.

## Production Considerations

Recommended next steps for a deployed client environment:

- Add persistent storage for history using Postgres, Supabase, or Snowflake.
- Add authentication and role-based access control.
- Add audit logging for prompts and generated outputs.
- Add a vector database for company knowledge retrieval.
- Add approval workflows for external communication.
- Add usage limits, cost tracking, and tenant-level configuration.

## License

This project is provided as a professional portfolio and consulting demonstration project. Adapt licensing terms based on your intended commercial use.

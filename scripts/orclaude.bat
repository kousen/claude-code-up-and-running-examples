@echo off
REM Run Claude Code against any OpenRouter model: orclaude <vendor/model-slug> [claude args...]
if not defined OPENROUTER_API_KEY (
    echo Set OPENROUTER_API_KEY in your environment >&2
    exit /b 1
)
set "ANTHROPIC_BASE_URL=https://openrouter.ai/api"
set "ANTHROPIC_AUTH_TOKEN=%OPENROUTER_API_KEY%"
set "ANTHROPIC_API_KEY="
set "ANTHROPIC_DEFAULT_OPUS_MODEL=%~1"
set "ANTHROPIC_DEFAULT_SONNET_MODEL=%~1"
set "ANTHROPIC_DEFAULT_HAIKU_MODEL=%~1"
set "CLAUDE_CODE_SUBAGENT_MODEL=%~1"
shift
set "ARGS="
:collect
if "%~1"=="" goto run
set "ARGS=%ARGS% %1"
shift
goto collect
:run
claude%ARGS%

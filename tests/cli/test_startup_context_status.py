from types import SimpleNamespace
from unittest.mock import MagicMock, patch


def _import_cli():
    import cli as cli_mod

    return cli_mod


def test_show_status_includes_loaded_context_summary():
    cli_mod = _import_cli()

    stub = SimpleNamespace(
        enabled_toolsets=None,
        model="gpt-5.3-codex",
        api_key="test-key",
        provider="openai-codex",
        _provider_source=None,
        _startup_context_files=["~/.claude/CLAUDE.md", "CLAUDE.md", "AGENTS.md"],
        console=MagicMock(),
    )

    with patch.object(cli_mod, "get_tool_definitions", return_value=[{"name": "terminal"}]):
        cli_mod.HermesCLI._show_status(stub)

    assert stub.console.print.called
    rendered = stub.console.print.call_args[0][0]
    assert "context:" in rendered
    assert "~/.claude/CLAUDE.md" in rendered
    assert "CLAUDE.md" in rendered
    assert "AGENTS.md" in rendered

from unittest.mock import patch

from gateway.run import _discover_gateway_context_files


def test_discovery_includes_repo_claude_when_user_claude_missing(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "CLAUDE.md").write_text("repo guidance", encoding="utf-8")

    fake_home = tmp_path / "fake_home"
    fake_home.mkdir()

    with patch("pathlib.Path.home", return_value=fake_home):
        labels = _discover_gateway_context_files(cwd=str(repo))

    assert "CLAUDE.md" in labels
    assert "~/.claude/CLAUDE.md" not in labels


def test_discovery_includes_user_claude_when_present(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()

    fake_home = tmp_path / "fake_home"
    user_claude_dir = fake_home / ".claude"
    user_claude_dir.mkdir(parents=True)
    (user_claude_dir / "CLAUDE.md").write_text("user guidance", encoding="utf-8")

    with patch("pathlib.Path.home", return_value=fake_home):
        labels = _discover_gateway_context_files(cwd=str(repo))

    assert "~/.claude/CLAUDE.md" in labels

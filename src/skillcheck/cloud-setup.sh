# From REPOSITORY, release RELEASE_VERSION. Add these lines to the end of a Claude Code
# cloud environment's setup script: open the environment's menu, choose Edit, then Setup script.
#
# They install a hook that runs as each session in the environment starts or resumes. It copies
# the skills of REPOSITORY's newest release into ~/.claude/skills, so every session loads them,
# with nothing to upload. If a download fails, the session keeps the skills already there. The
# hook replaces only the skills it installed, which ~/.claude/skills/.claude-code-skills.json
# lists. It also turns off the plugins synced from claude.ai in these sessions, so a plugin's
# copy of a skill never loads beside the hook's copy.
mkdir -p "$HOME/.claude/hooks"
cat > "$HOME/.claude/hooks/claude-code-skills.py" <<'END_OF_SKILLS_HOOK'
HOOK_SOURCE
END_OF_SKILLS_HOOK
python3 - <<'END_OF_SKILLS_SETTINGS'
import json
from pathlib import Path

path = Path.home() / ".claude" / "settings.json"
settings = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
command = 'python3 "$HOME/.claude/hooks/claude-code-skills.py"'
starts = settings.setdefault("hooks", {}).setdefault("SessionStart", [])
# Running this script again replaces the hook rather than adding a second one.
starts[:] = [g for g in starts if all(h.get("command") != command for h in g.get("hooks", []))]
starts.append(
    {"matcher": "startup|resume", "hooks": [{"type": "command", "command": command, "timeout": 60}]}
)
settings["syncClaudeAiPlugins"] = False
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
END_OF_SKILLS_SETTINGS
# Once now, so the environment's cached copy holds the skills even when a session can't download.
python3 "$HOME/.claude/hooks/claude-code-skills.py"

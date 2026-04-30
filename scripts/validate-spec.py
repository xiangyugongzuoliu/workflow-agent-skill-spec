#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PRIVATE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"/Users/[A-Za-z0-9._-]+/"),
    re.compile(r"~/Downloads/"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)(api[_-]?key|token|secret|cookie|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
)

ALLOWED_PRIVATE_PATTERN_FILES = {
    "README.md",
    "CLAUDE.md",
    "docs/security.md",
    "docs/testing.md",
    "docs/credentials.md",
    "docs/skill-file.md",
    "templates/SKILL.md",
    "examples/workflow-skill/workflow/step02-execute.md",
    "scripts/validate-spec.py",
}

STEP_RE = re.compile(r"^step[0-9]{2}-[a-z0-9-]+$")
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")


@dataclass
class Finding:
    path: str
    message: str


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def relative(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def add(findings: list[Finding], root: Path, path: Path, message: str) -> None:
    findings.append(Finding(relative(path, root), message))


def markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if ".git" not in path.parts
    )


def json_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.json")
        if ".git" not in path.parts
    )


def check_json(root: Path, findings: list[Finding]) -> None:
    for path in json_files(root):
        try:
            load_json(path)
        except json.JSONDecodeError as exc:
            add(findings, root, path, f"JSON 无法解析：{exc}")


def check_markdown_fences(root: Path, findings: list[Finding]) -> None:
    for path in markdown_files(root):
        text = path.read_text(encoding="utf-8")
        count = sum(1 for line in text.splitlines() if line.startswith("```"))
        if count % 2:
            add(findings, root, path, f"代码围栏数量为奇数：{count}")


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def check_skill_files(root: Path, findings: list[Finding]) -> None:
    for path in sorted(root.rglob("SKILL.md")):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        if not meta:
            add(findings, root, path, "缺少 YAML frontmatter。")
            continue
        name = meta.get("name", "")
        description = meta.get("description", "")
        if not NAME_RE.match(name):
            add(findings, root, path, "name 必须使用小写字母、数字和连字符。")
        if len(description) < 30:
            add(findings, root, path, "description 过短，无法稳定触发。")
        if "不用于" not in description and "不要" not in text:
            add(findings, root, path, "description 或正文应写清排除场景。")
        for heading in ("## 范围", "## 输入", "## 工作流", "## 输出"):
            if heading not in text:
                add(findings, root, path, f"缺少章节：{heading}")


def check_progress(root: Path, findings: list[Finding]) -> None:
    candidates = [root / "templates/progress.json"]
    candidates.extend(root.glob("examples/**/state/progress.json"))
    for path in candidates:
        if not path.exists():
            continue
        data = load_json(path)
        required = [
            "status",
            "created_at",
            "updated_at",
            "keyword",
            "current_step",
            "completed_steps",
            "failed_steps",
            "outputs",
            "resume_hint",
        ]
        for key in required:
            if key not in data:
                add(findings, root, path, f"progress.json 缺少字段：{key}")
        if data.get("status") not in {"pending", "processing", "completed", "failed"}:
            add(findings, root, path, "status 不在允许集合内。")
        current_step = data.get("current_step")
        if isinstance(current_step, str) and not STEP_RE.match(current_step):
            add(findings, root, path, "current_step 不符合 stepNN-action 格式。")


def check_trigger_eval(root: Path, findings: list[Finding]) -> None:
    path = root / "evals/trigger-queries.json"
    if not path.exists():
        add(findings, root, path, "缺少 trigger eval。")
        return
    data = load_json(path)
    queries = data.get("queries", [])
    if not isinstance(queries, list) or len(queries) < 10:
        add(findings, root, path, "queries 至少需要 10 条。")
        return
    should = [item for item in queries if item.get("should_trigger") is True]
    should_not = [item for item in queries if item.get("should_trigger") is False]
    if len(should) < 5 or len(should_not) < 5:
        add(findings, root, path, "正向和负向触发样例都至少需要 5 条。")
    ids = [item.get("id") for item in queries]
    if len(ids) != len(set(ids)):
        add(findings, root, path, "query id 存在重复。")


def check_runtime(root: Path, findings: list[Finding]) -> None:
    for path in sorted(root.glob("**/config/runtime.json")):
        data = load_json(path)
        if data.get("schema_version") != "1.0":
            add(findings, root, path, "schema_version 必须为 1.0。")
        skill = data.get("skill", "")
        if not isinstance(skill, str) or not NAME_RE.match(skill):
            add(findings, root, path, "skill 字段必须是稳定 hyphen-case 名称。")
        for model in data.get("models", []):
            if model.get("required") and not model.get("sha256"):
                add(findings, root, path, f"必需模型缺少 sha256：{model.get('id')}")
        cache_policy = data.get("cache_policy", {})
        if cache_policy.get("sync") is True:
            add(findings, root, path, "公开 Skill 的 cache_policy.sync 默认不应为 true。")


def check_private_patterns(root: Path, findings: list[Finding]) -> None:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = relative(path, root)
        if rel in ALLOWED_PRIVATE_PATTERN_FILES:
            continue
        if path.suffix not in {".md", ".json", ".py", ".sh", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in PRIVATE_PATTERNS:
            if pattern.search(text):
                add(findings, root, path, f"疑似私有路径或凭据模式：{pattern.pattern}")


def check_required_files(root: Path, findings: list[Finding]) -> None:
    required = [
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "CLAUDE.md",
        "AGENTS.md",
        "CHANGELOG.md",
        "templates/SKILL.md",
        "templates/progress.json",
        "templates/runtime.json",
        "evals/trigger-queries.json",
        "evals/function-cases.json",
        "evals/recovery-cases.json",
        "evals/security-cases.json",
        "evals/runtime-cases.json",
        "docs/specification.md",
        "docs/security.md",
        "docs/testing.md",
        "docs/quality-rubric.md",
        "docs/glossary.md",
        "docs/platform-adapters.md",
        "docs/release.md",
        "schemas/skill.schema.json",
        "schemas/progress.schema.json",
        "schemas/runtime.schema.json",
        "schemas/trigger-eval.schema.json",
        "examples/workflow-skill/config/runtime.json",
        "examples/workflow-skill/scripts/scan-release.sh",
        "examples/workflow-skill/runs/example-run/state/progress.json",
    ]
    for item in required:
        path = root / item
        if not path.exists():
            add(findings, root, path, "缺少必需文件。")


def run(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    check_required_files(root, findings)
    check_json(root, findings)
    check_markdown_fences(root, findings)
    check_skill_files(root, findings)
    check_progress(root, findings)
    check_trigger_eval(root, findings)
    check_runtime(root, findings)
    check_private_patterns(root, findings)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Workflow Agent Skill spec repository.")
    parser.add_argument("--root", default=".", help="Repository root.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings = run(root)
    if findings:
        for finding in findings:
            print(f"{finding.path}: {finding.message}", file=sys.stderr)
        return 1
    print("validate-spec-ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

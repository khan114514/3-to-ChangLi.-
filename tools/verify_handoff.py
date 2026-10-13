#!/usr/bin/env python3
"""Verify the published handoff file manifest and the unmodified QA sources."""

import hashlib
import json
from pathlib import Path


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "manifests/files.json").read_text())
    failures = []
    for relative, expected in manifest["files"].items():
        path = root / relative
        if path.is_symlink() or not path.is_file():
            failures.append({"path": relative, "reason": "missing or symlink"})
        elif sha256(path) != expected["sha256"]:
            failures.append({"path": relative, "reason": "hash mismatch"})
        elif path.stat().st_size != expected["bytes"]:
            failures.append({"path": relative, "reason": "size mismatch"})

    manager = root / "skills/autoresearch-manager"
    release = json.loads((manager / "assets/qa-release.json").read_text())
    for relative, expected in release["files"].items():
        path = manager / "assets/qa-skills" / relative
        if not path.is_file() or sha256(path) != expected:
            failures.append({"path": "skills/autoresearch-manager/assets/qa-skills/" + relative,
                             "reason": "original QA source mismatch"})
    print(json.dumps({"status": "FAIL" if failures else "PASS",
                      "handoff_files": len(manifest["files"]),
                      "qa_files": len(release["files"]),
                      "qa_version": release["release"]["version"],
                      "failures": failures}, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

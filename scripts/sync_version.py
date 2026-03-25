"""pyproject.toml 버전을 읽어 version.py에 동기화하는 스크립트.

사용법:
    python scripts/sync_version.py

CI에서 `changepacks update` 실행 후 이 스크립트를 호출하여
pyproject.toml의 버전을 version.py에 반영한다.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EVIDENCE_TOML = ROOT / "evidence_snv" / "pyproject.toml"
PIPELINE_TOML = ROOT / "pipeline" / "pyproject.toml"
VERSION_PY = ROOT / "version.py"

VERSION_RE = re.compile(r'version\s*=\s*"([^"]+)"')


def read_version_from_toml(toml_path: Path) -> str:
    text = toml_path.read_text(encoding="utf-8")
    match = VERSION_RE.search(text)
    if not match:
        raise ValueError(f"version not found in {toml_path}")
    return match.group(1)


def sync() -> None:
    evi_ver = read_version_from_toml(EVIDENCE_TOML)
    pip_ver = read_version_from_toml(PIPELINE_TOML)

    content = (
        f'EVIDENCE_VERSION = "v{evi_ver}"\n'
        f'PIPELINE_VERSION = "v{pip_ver}"\n'
    )

    VERSION_PY.write_text(content, encoding="utf-8")
    print(f"version.py updated:")
    print(f"  EVIDENCE_VERSION = v{evi_ver}")
    print(f"  PIPELINE_VERSION = v{pip_ver}")


if __name__ == "__main__":
    sync()

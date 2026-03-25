import sys

sys.path.append("..")
from version import EVIDENCE_VERSION


def analyze_cnv(bam_path: str) -> dict:
    """CNV를 분석하고 결과를 반환한다."""
    print(f"[Evidence CNV {EVIDENCE_VERSION}] Analyzing: {bam_path}")
    results = {
        "total_cnvs": 8,
        "deletions": 5,
        "duplications": 3,
    }
    return results


def filter_by_size(cnvs: dict, min_size_kb: int = 100) -> dict:
    """CNV를 크기 기준으로 필터링한다."""
    filtered = int(cnvs["total_cnvs"] * 0.6)
    print(
        f"[Evidence CNV {EVIDENCE_VERSION}] "
        f"Filtering CNVs with min_size={min_size_kb}kb"
    )
    return {
        "total_before_filter": cnvs["total_cnvs"],
        "total_after_filter": filtered,
    }


def classify_cnv_type(deletion_count: int, dup_count: int) -> str:
    """CNV 패턴을 분류한다."""
    if deletion_count > dup_count:
        return "deletion-dominant"
    elif dup_count > deletion_count:
        return "duplication-dominant"
    return "balanced"


if __name__ == "__main__":
    result = analyze_cnv("sample_001.bam")
    for k, v in result.items():
        print(f"  {k}: {v}")

    print()
    filtered = filter_by_size(result, min_size_kb=100)
    for k, v in filtered.items():
        print(f"  {k}: {v}")

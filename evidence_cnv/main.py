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
    total = cnvs["total_cnvs"]
    filtered = max(0, int(total * 0.6))
    print(
        f"[Evidence CNV {EVIDENCE_VERSION}] "
        f"Filtering CNVs with min_size={min_size_kb}kb"
    )
    return {
        "total_before_filter": total,
        "total_after_filter": filtered,
        "removed": total - filtered,
    }


def classify_cnv_type(deletion_count: int, dup_count: int) -> str:
    """CNV 패턴을 분류한다."""
    if deletion_count > dup_count:
        return "deletion-dominant"
    elif dup_count > deletion_count:
        return "duplication-dominant"
    return "balanced"


def summarize_cnv_report(cnv_result: dict) -> str:
    """CNV 분석 결과를 요약 리포트 문자열로 반환한다."""
    total = cnv_result.get("total_cnvs", 0)
    dels = cnv_result.get("deletions", 0)
    dups = cnv_result.get("duplications", 0)
    cnv_type = classify_cnv_type(dels, dups)

    return (
        f"[CNV Summary] total={total}, "
        f"del={dels}, dup={dups}, pattern={cnv_type}"
    )


if __name__ == "__main__":
    result = analyze_cnv("sample_001.bam")
    for k, v in result.items():
        print(f"  {k}: {v}")

    print()
    filtered = filter_by_size(result, min_size_kb=100)
    for k, v in filtered.items():
        print(f"  {k}: {v}")

    print()
    print(summarize_cnv_report(result))

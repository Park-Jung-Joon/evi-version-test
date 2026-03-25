import sys

# Minor trial 1
sys.path.append("..")
from version import EVIDENCE_VERSION


def analyze_snv(vcf_path: str) -> dict:
    """SNV variant를 분석하고 결과를 반환한다."""
    print(f"[Evidence SNV {EVIDENCE_VERSION}] Analyzing: {vcf_path}")
    results = {"total_variants": 150, "pathogenic": 3, "vus": 12, "benign": 135}
    return results


def classify_variant(variant_type: str) -> str:
    """Variant 타입을 분류하여 라벨을 반환한다."""
    labels = {"pathogenic": "P", "vus": "VUS", "benign": "B"}
    return labels.get(variant_type, "Unknown")


def filter_by_quality(variants: dict, min_quality: int = 30) -> dict:
    """Quality score 기준으로 variant를 필터링한다."""
    filtered_count = int(variants["total_variants"] * 0.85)
    print(
        f"[Evidence SNV {EVIDENCE_VERSION}] "
        f"Filtering variants with min_quality={min_quality}"
    )
    return {
        "total_before_filter": variants["total_variants"],
        "total_after_filter": filtered_count,
        "removed": variants["total_variants"] - filtered_count,
    }


if __name__ == "__main__":
    result = analyze_snv("sample_001.vcf")
    for k, v in result.items():
        print(f"  {k}: {v}")

    print()
    filtered = filter_by_quality(result, min_quality=30)
    for k, v in filtered.items():
        print(f"  {k}: {v}")

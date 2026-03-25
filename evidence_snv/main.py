import sys

# Minor trial 1
sys.path.append("..")
from version import EVIDENCE_VERSION


def analyze_snv(vcf_path: str) -> dict:
    """SNV variant를 분석하고 결과 딕셔너리를 반환한다."""
    print(f"[Evidence SNV {EVIDENCE_VERSION}] Analyzing: {vcf_path}")
def analyze_snv(vcf_path: str, genome_build: str = "GRCh38") -> dict:
    """SNV variant를 분석하고 결과 딕셔너리를 반환한다.

    NOTE: API 변경 - genome_build 파라미터 추가 (하위 호환 깨짐)
    기존 호출 코드에서 positional arg로 사용하던 경우 수정 필요.
    """
    print(
        f"[Evidence SNV {EVIDENCE_VERSION}] "
        f"Analyzing: {vcf_path} (build={genome_build})"
    )
    results = {
        "total_variants": 150,
        "pathogenic": 3,
        "vus": 12,
        "benign": 135,
        "genome_build": genome_build,
    }
    return results


def filter_by_quality(
    variants: dict, min_quality: int = 30
) -> dict:
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

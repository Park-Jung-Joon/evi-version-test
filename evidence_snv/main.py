import sys

# Minor trial 1
sys.path.append("..")
from version import EVIDENCE_VERSION


class SnvAnalyzer:
    """SNV 분석기. 기존 함수형 API를 클래스 기반으로 전면 변경.

    Breaking Change: analyze_snv() 함수가 제거되고
    SnvAnalyzer 클래스로 대체됨.
    """

    SUPPORTED_BUILDS = ("GRCh37", "GRCh38")

    def __init__(self, genome_build: str = "GRCh38"):
        if genome_build not in self.SUPPORTED_BUILDS:
            raise ValueError(
                f"Unsupported genome build: {genome_build}. "
                f"Must be one of {self.SUPPORTED_BUILDS}"
            )
        self.genome_build = genome_build

    def analyze(self, vcf_path: str) -> dict:
        print(
            f"[Evidence SNV {EVIDENCE_VERSION}] "
            f"Analyzing: {vcf_path} (build={self.genome_build})"
        )
        return {
            "total_variants": 150,
            "pathogenic": 3,
            "vus": 12,
            "benign": 135,
            "genome_build": self.genome_build,
        }


def filter_by_quality(
    variants: dict, min_quality: int = 30
) -> dict:
    """Quality score 기준으로 variant를 필터링하여 결과를 반환한다."""
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
    analyzer = SnvAnalyzer(genome_build="GRCh38")
    result = analyzer.analyze("sample_001.vcf")
    for k, v in result.items():
        print(f"  {k}: {v}")

    print()
    filtered = filter_by_quality(result, min_quality=30)
    for k, v in filtered.items():
        print(f"  {k}: {v}")

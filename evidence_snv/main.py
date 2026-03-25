import sys

sys.path.append("..")
from version import EVIDENCE_VERSION


class SnvAnalyzer:
    """SNV 분석기 (config dict 기반).

    BREAKING CHANGE: 기존 analyze_snv() 함수 및 genome_build 파라미터가
    제거되고, config dict를 받는 SnvAnalyzer 클래스로 전면 교체됨.
    기존 코드에서 analyze_snv(vcf_path) 호출은 모두 수정 필요.
    """

    SUPPORTED_BUILDS = ("GRCh37", "GRCh38")

    def __init__(self, config: dict):
        genome_build = config.get("genome_build", "GRCh38")
        if genome_build not in self.SUPPORTED_BUILDS:
            raise ValueError(
                f"Unsupported genome build: {genome_build}. "
                f"Must be one of {self.SUPPORTED_BUILDS}"
            )
        self.config = config
        self.genome_build = genome_build
        self.min_quality = config.get("min_quality", 30)

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

    def filter_by_quality(self, variants: dict) -> dict:
        """Quality score 기준으로 variant를 필터링한다."""
        filtered_count = int(variants["total_variants"] * 0.85)
        print(
            f"[Evidence SNV {EVIDENCE_VERSION}] "
            f"Filtering variants with min_quality={self.min_quality}"
        )
        return {
            "total_before_filter": variants["total_variants"],
            "total_after_filter": filtered_count,
            "removed": variants["total_variants"] - filtered_count,
        }


if __name__ == "__main__":
    config = {"genome_build": "GRCh38", "min_quality": 30}
    analyzer = SnvAnalyzer(config)

    result = analyzer.analyze("sample_001.vcf")
    for k, v in result.items():
        print(f"  {k}: {v}")

    print()
    filtered = analyzer.filter_by_quality(result)
    for k, v in filtered.items():
        print(f"  {k}: {v}")

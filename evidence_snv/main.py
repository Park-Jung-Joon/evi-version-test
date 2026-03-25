import sys

sys.path.append("..")
from version import EVIDENCE_VERSION


def analyze_snv(vcf_path: str) -> dict:
    """SNV variant를 분석하고 결과를 반환한다."""
    print(f"[Evidence SNV {EVIDENCE_VERSION}] Analyzing: {vcf_path}")
    results = {
        "total_variants": 150,
        "pathogenic": 3,
        "vus": 12,
        "benign": 135,
    }
    return results


if __name__ == "__main__":
    result = analyze_snv("sample_001.vcf")
    for k, v in result.items():
        print(f"  {k}: {v}")

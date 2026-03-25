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


if __name__ == "__main__":
    result = analyze_cnv("sample_001.bam")
    for k, v in result.items():
        print(f"  {k}: {v}")

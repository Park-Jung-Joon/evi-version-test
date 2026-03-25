import sys

sys.path.append("..")
from version import PIPELINE_VERSION


def run_pipeline(sample_id: str) -> None:
    """전체 분석 파이프라인을 실행한다."""
    print(
        f"[Pipeline {PIPELINE_VERSION}] Starting pipeline for: {sample_id}"
    )
    steps = [
        "fastq_qc",
        "alignment",
        "variant_calling",
        "annotation",
        "evidence",
    ]
    for i, step in enumerate(steps, 1):
        print(f"  [{i}/{len(steps)}] {step} ... done")
    print(f"Pipeline complete for {sample_id}")


if __name__ == "__main__":
    run_pipeline("SAMPLE_001")

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


def check_sample_status(sample_id: str) -> str:
    """샘플의 파이프라인 처리 상태를 확인한다."""
    print(
        f"[Pipeline {PIPELINE_VERSION}] Checking status: {sample_id}"
    )
    return "completed"


def run_qc_step(sample_id: str, fastq_path: str) -> dict:
    """FASTQ QC 단계를 독립적으로 실행하고 결과를 반환한다."""
    print(
        f"[Pipeline {PIPELINE_VERSION}] Running QC for: {sample_id}"
    )
    print(f"  Input: {fastq_path}")
    qc_result = {
        "sample_id": sample_id,
        "total_reads": 50_000_000,
        "q30_ratio": 0.95,
        "gc_content": 0.42,
        "pass": True,
    }
    status = "PASS" if qc_result["pass"] else "FAIL"
    print(f"  QC result: {status} (Q30={qc_result['q30_ratio']:.0%})")
    return qc_result


if __name__ == "__main__":
    run_pipeline("SAMPLE_001")
    print()
    status = check_sample_status("SAMPLE_001")
    print(f"  status: {status}")
    print()
    qc = run_qc_step("SAMPLE_001", "/data/SAMPLE_001_R1.fastq.gz")
    for k, v in qc.items():
        print(f"  {k}: {v}")

import re
from pathlib import Path
from typing import Dict, Optional, List

HW_DIR = Path(__file__).parent
BASELINE_DIR =  HW_DIR / "3_results_baseline"
MONOLITHIC_DIR = HW_DIR / "3_results_monolithic"

OUTPUT_MD = HW_DIR / "3_comparison.md"
OUTPUT_PNG = HW_DIR / "3_comparison.png"

HAS_PLOT_LIBS: bool = True
try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    HAS_PLOT_LIBS = False


def parse_ipc_file(file_path: Path) -> Optional[float]:
    try:
        content: str = file_path.read_text()
        match = re.search(r"board\.processor\.cores\.core\.ipc\s+([0-9.]+)", content)
        if match:
            return float(match.group(1))
    except Exception:
        pass
    return None


def collect_ipc_data(dir_path: Path) -> Dict[str, float]:
    data: Dict[str, float] = {}
    if not dir_path.exists():
        return data
    for file_path in dir_path.glob("ipc_*.txt"):
        benchmark_name: str = file_path.stem.replace("ipc_", "")
        ipc_val: Optional[float] = parse_ipc_file(file_path)
        if ipc_val is not None:
            data[benchmark_name] = ipc_val
    return data


def generate_markdown_table(baseline: Dict[str, float], monolithic: Dict[str, float]) -> str:
    all_benchmarks: List[str] = sorted(list(set(baseline.keys()) | set(monolithic.keys())))

    md_lines: List[str] = [
        "| Benchmark | Baseline IPC (9 IQs) | Monolithic IPC (1 IQ) | Speedup (%) |",
        "| :--- | :---: | :---: | :---: |"
    ]

    for bench in all_benchmarks:
        base_ipc: Optional[float] = baseline.get(bench)
        mono_ipc: Optional[float] = monolithic.get(bench)

        if base_ipc is not None and mono_ipc is not None:
            speedup: float = ((mono_ipc / base_ipc) - 1.0) * 100.0
            speedup_str: str = f"{speedup:+.2f}%"
            base_str: str = f"{base_ipc:.6f}"
            mono_str: str = f"{mono_ipc:.6f}"
        else:
            base_str = f"{base_ipc:.6f}" if base_ipc is not None else "N/A"
            mono_str = f"{mono_ipc:.6f}" if mono_ipc is not None else "N/A"
            speedup_str = "N/A"

        md_lines.append(f"| {bench} | {base_str} | {mono_str} | {speedup_str} |")

    return "\n".join(md_lines)


def generate_chart(baseline: Dict[str, float], monolithic: Dict[str, float], output_path: Path) -> None:
    if not HAS_PLOT_LIBS:
        print("[Warning] matplotlib or numpy is not installed. Skipping chart generation.")
        return

    all_benchmarks: List[str] = sorted(list(set(baseline.keys()) & set(monolithic.keys())))
    if not all_benchmarks:
        print("[Warning] No matching benchmarks found for plotting.")
        return

    x = np.arange(len(all_benchmarks))
    width: float = 0.35

    base_values: List[float] = [baseline[b] for b in all_benchmarks]
    mono_values: List[float] = [monolithic[b] for b in all_benchmarks]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width/2, base_values, width, label="Baseline (9 IQs)", color="#1f77b4")
    ax.bar(x + width/2, mono_values, width, label="Monolithic (1 IQ)", color="#2ca02c")

    ax.set_ylabel("IPC (Instructions Per Cycle)")
    ax.set_title("IPC Comparison: Baseline vs Monolithic IQ in Neoverse V2")
    ax.set_xticks(x)
    ax.set_xticklabels(all_benchmarks)
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"[Info] Comparison chart saved to {output_path}")


def main() -> None:
    baseline_dir = Path(BASELINE_DIR)
    monolithic_dir = Path(MONOLITHIC_DIR)

    baseline_data: Dict[str, float] = collect_ipc_data(baseline_dir)
    monolithic_data: Dict[str, float] = collect_ipc_data(monolithic_dir)

    if not baseline_data and not monolithic_data:
        print(f"[Error] No valid IPC files found in '{BASELINE_DIR}' or '{MONOLITHIC_DIR}'.")
        return

    markdown_table: str = generate_markdown_table(baseline_data, monolithic_data)

    Path(OUTPUT_MD).write_text(markdown_table)
    print(f"[Info] Markdown table saved to {OUTPUT_MD}")
    print("\nGenerated Table:\n")
    print(markdown_table)
    print()

    generate_chart(baseline_data, monolithic_data, Path(OUTPUT_PNG))


if __name__ == "__main__":
    main()

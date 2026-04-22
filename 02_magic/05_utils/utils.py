import json
import re
from pathlib import Path


def load_nb(path: Path):
    """Load a notebook file and return parsed JSON content.

    This helper reads an executed `.ipynb` file from disk. The returned
    dictionary lets us access code cell outputs for comparison logic.
    """
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def stream_text(nb: dict, cell_idx: int) -> str:
    """Collect all stream outputs from a single cell as one string.

    Many notebooks print metrics using stream outputs. This function joins
    those printed fragments so values can be parsed reliably.
    """
    chunks = []
    for output in nb["cells"][cell_idx].get("outputs", []):
        if output.get("output_type") == "stream":
            chunks.append("".join(output.get("text", "")))
    return "\n".join(chunks)


def display_text(nb: dict, cell_idx: int) -> str:
    """Collect all display/execute plain-text outputs from one cell.

    Tables rendered by notebooks are often stored in `display_data` or
    `execute_result`. This helper returns a combined plain-text version.
    """
    chunks = []
    for output in nb["cells"][cell_idx].get("outputs", []):
        if output.get("output_type") in ["display_data", "execute_result"]:
            chunks.append("".join(output.get("data", {}).get("text/plain", [])))
    return "\n".join(chunks)


def first_display_text(outputs: list) -> str:
    """Return the first display-like text block from cell outputs.

    Some cells print messages before showing tables. This function extracts
    the first table-like output to avoid parsing the wrong section.
    """
    for output in outputs:
        if output.get("output_type") in ["display_data", "execute_result"]:
            return "".join(output.get("data", {}).get("text/plain", []))
    return ""


def parse_metric_block(text: str, metrics: list[str]) -> dict:
    """Parse metric values from plain-text table content.

    The function searches each metric name followed by a numeric value.
    Missing metrics are returned as `float("nan")` for explicit handling.
    """
    parsed = {}
    for metric in metrics:
        match = re.search(rf"{re.escape(metric)}\s+([-0-9.]+)", text)
        parsed[metric] = float(match.group(1)) if match else float("nan")
    return parsed


def parse_forecast_baseline_test_metrics(text: str) -> dict:
    """Extract baseline forecasting test metrics from stream output.

    The baseline notebook prints train and test blocks in one stream.
    This helper targets the test block and returns MAE, RMSE, and R2.
    """
    mae_match = re.search(r"--- Test ---\s*MAE:\s*([-0-9.]+)", text)
    rmse_match = re.search(r"--- Test ---[\s\S]*?RMSE:\s*([-0-9.]+)", text)
    r2_match = re.search(r"--- Test ---[\s\S]*?R.?\s*:\s*([-0-9.]+)", text)

    return {
        "Price_MAE": float(mae_match.group(1)) if mae_match else float("nan"),
        "Price_RMSE": float(rmse_match.group(1)) if rmse_match else float("nan"),
        "Price_R2": float(r2_match.group(1)) if r2_match else float("nan"),
    }


def parse_forecast_final_test_metrics(text: str) -> dict:
    """Extract final forecasting test metrics from the comparison table text.

    The forecasting notebook stores validation and test rows together in one
    display output. This helper reads the test row metrics directly.
    """
    match = re.search(r"Test\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)", text)
    return {
        "Price_MAE": float(match.group(1)) if match else float("nan"),
        "Price_RMSE": float(match.group(2)) if match else float("nan"),
        "Price_R2": float(match.group(3)) if match else float("nan"),
        "Directional_Accuracy": float(match.group(4)) if match else float("nan"),
    }

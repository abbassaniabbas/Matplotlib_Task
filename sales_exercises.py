"""Plot monthly company profit and product sales from the supplied CSV."""

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_sales(csv_path: Path):
    with csv_path.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        required = {"month_number", "total_profit", "bathingsoap", "facewash"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing CSV columns: {', '.join(sorted(missing))}")

        rows = [
            {
                "month": int(row["month_number"]),
                "profit": int(row["total_profit"]),
                "bathing_soap": int(row["bathingsoap"]),
                "facewash": int(row["facewash"]),
            }
            for row in reader
        ]

    if not rows:
        raise ValueError("The CSV contains no monthly sales rows")
    return sorted(rows, key=lambda row: row["month"])


def create_plots(rows, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    months = [row["month"] for row in rows]

    # Exercise 1: total profit for every month in a line plot.
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(months, [row["profit"] for row in rows], color="#1769aa", marker="o", linewidth=2)
    ax.set(title="Monthly Total Profit", xlabel="Month", ylabel="Total profit")
    ax.set_xticks(months)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    profit_path = output_dir / "exercise_1_total_profit.png"
    fig.savefig(profit_path, dpi=180)
    plt.close(fig)

    # Exercise 2: separate subplots for bathing soap and facewash.
    fig, (soap_ax, facewash_ax) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    soap_ax.plot(months, [row["bathing_soap"] for row in rows], color="#16866a", marker="o")
    soap_ax.set(title="Bathing Soap Sales", ylabel="Units sold")
    facewash_ax.plot(months, [row["facewash"] for row in rows], color="#c06736", marker="o")
    facewash_ax.set(title="Facewash Sales", xlabel="Month", ylabel="Units sold")
    facewash_ax.set_xticks(months)
    for ax in (soap_ax, facewash_ax):
        ax.grid(alpha=0.3)
    fig.tight_layout()
    products_path = output_dir / "exercise_2_bathing_soap_facewash.png"
    fig.savefig(products_path, dpi=180)
    plt.close(fig)

    return profit_path, products_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "csv_path",
        nargs="?",
        type=Path,
        default=Path("/Users/Abbas/Downloads/company_sales_data.csv"),
        help="Path to the company sales CSV",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path(__file__).resolve().parent / "sales_plots"
    )
    args = parser.parse_args()
    for plot_path in create_plots(read_sales(args.csv_path), args.output_dir):
        print(plot_path)


if __name__ == "__main__":
    main()

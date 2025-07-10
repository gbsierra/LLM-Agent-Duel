import pandas
import matplotlib.pyplot
import seaborn
import os
from pathlib import Path

# Set up directories
NIM_DIR = "benchmarks/nim"
HANOI_DIR = "benchmarks/hanoi"
OUTPUT_DIR = "plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to load CSVs from a folder
def load_csvs(directory):
    dataframes = []
    if not os.path.exists(directory):
        print(f"Warning: Directory {directory} not found. Creating it.")
        os.makedirs(directory)
        return pandas.DataFrame()  # Return empty DataFrame if no files
    for file in Path(directory).glob("*.csv"):
        try:
            df = pandas.read_csv(file)
            # Extract prompt name from filename (e.g., nim_baseline.csv -> baseline)
            prompt_name = file.stem.replace("nim_benchmark_", "").replace("hanoi_benchmark_", "")
            df["prompt"] = prompt_name
            dataframes.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")
    if not dataframes:
        print(f"No CSV files found in {directory}")
        return pandas.DataFrame()
    return pandas.concat(dataframes, ignore_index=True)

# Load data
nim_data = load_csvs(NIM_DIR)
hanoi_data = load_csvs(HANOI_DIR)

# Function to calculate win rates (for Nim only)
def calculate_win_rates(df):
    if df.empty:
        return pandas.DataFrame()
    win_counts = df.groupby(["prompt", "winner"]).size().unstack(fill_value=0)
    win_rates = win_counts.div(win_counts.sum(axis=1), axis=0)
    return win_rates

# Plot 1: Win Rates for Nim (Bar Chart)
if not nim_data.empty:
    nim_win_rates = calculate_win_rates(nim_data)
    if not nim_win_rates.empty:
        fig = matplotlib.pyplot.figure(figsize=(10, 6))
        nim_win_rates.plot(kind="bar", stacked=False)
        matplotlib.pyplot.title("Nim Game Win Rates for Llama3.2 and Gemma3 by Prompt")
        matplotlib.pyplot.xlabel("Prompt")
        matplotlib.pyplot.ylabel("Win Rate")
        matplotlib.pyplot.legend(title="Agent", bbox_to_anchor=(0, 0), loc='lower left', bbox_transform=fig.transFigure)
        matplotlib.pyplot.tight_layout()
        matplotlib.pyplot.savefig(os.path.join(OUTPUT_DIR, "nim_win_rates.png"))
        matplotlib.pyplot.close()
    else:
        print("No win rate data to plot for Nim")
else:
    print("No Nim data to plot")

# Plot 2: Turns per Prompt (Box Plot)
matplotlib.pyplot.figure(figsize=(12, 6))
matplotlib.pyplot.subplot(1, 2, 1)
if not nim_data.empty:
    seaborn.boxplot(x="prompt", y="turns", data=nim_data)
    matplotlib.pyplot.title("Turns per Prompt in Nim Game")
else:
    matplotlib.pyplot.title("No Nim Data Available")
matplotlib.pyplot.xlabel("Prompt")
matplotlib.pyplot.ylabel("Number of Turns")
matplotlib.pyplot.xticks(rotation=45)

matplotlib.pyplot.subplot(1, 2, 2)
if not hanoi_data.empty:
    seaborn.boxplot(x="prompt", y="turns", data=hanoi_data)
    matplotlib.pyplot.title("Turns per Prompt in Towers of Hanoi")
else:
    matplotlib.pyplot.title("No Hanoi Data Available")
matplotlib.pyplot.xlabel("Prompt")
matplotlib.pyplot.ylabel("Number of Turns")
matplotlib.pyplot.xticks(rotation=45)
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.savefig(os.path.join(OUTPUT_DIR, "turns_boxplot.png"))
matplotlib.pyplot.close()

# Plot 3: Illegal Moves per Prompt (Box Plot)
matplotlib.pyplot.figure(figsize=(12, 6))
matplotlib.pyplot.subplot(1, 2, 1)
if not nim_data.empty:
    nim_data_melted = nim_data.melt(id_vars=["prompt"], value_vars=["illegal_moves_agent_a", "illegal_moves_agent_b"],
                                    var_name="agent", value_name="illegal_moves")
    nim_data_melted["agent"] = nim_data_melted["agent"].replace({
        "illegal_moves_agent_a": "Llama3.2", "illegal_moves_agent_b": "Gemma3"
    })
    seaborn.boxplot(x="prompt", y="illegal_moves", hue="agent", data=nim_data_melted)
    matplotlib.pyplot.title("Illegal Moves per Prompt in Nim Game")
else:
    matplotlib.pyplot.title("No Nim Data Available")
matplotlib.pyplot.xlabel("Prompt")
matplotlib.pyplot.ylabel("Illegal Moves")
matplotlib.pyplot.xticks(rotation=45)

matplotlib.pyplot.subplot(1, 2, 2)
if not hanoi_data.empty:
    hanoi_data_melted = hanoi_data.melt(id_vars=["prompt"], value_vars=["illegal_moves_agent_a", "illegal_moves_agent_b"],
                                        var_name="agent", value_name="illegal_moves")
    hanoi_data_melted["agent"] = hanoi_data_melted["agent"].replace({
        "illegal_moves_agent_a": "Llama3.2", "illegal_moves_agent_b": "Gemma3"
    })
    seaborn.boxplot(x="prompt", y="illegal_moves", hue="agent", data=hanoi_data_melted)
    matplotlib.pyplot.title("Illegal Moves per Prompt in Towers of Hanoi")
else:
    matplotlib.pyplot.title("No Hanoi Data Available")
matplotlib.pyplot.xlabel("Prompt")
matplotlib.pyplot.ylabel("Illegal Moves")
matplotlib.pyplot.xticks(rotation=45)
matplotlib.pyplot.tight_layout()
matplotlib.pyplot.savefig(os.path.join(OUTPUT_DIR, "illegal_moves_boxplot.png"))
matplotlib.pyplot.close()

print("\nVisualizations have been saved to the 'plots' directory!\n")
import heapq
import random
import math
import time
import statistics
import matplotlib.pyplot as plt
import pandas as pd

# Function: Merge Sorted Lists using a Min-Heap (Greedy method)
def merge_sorted_lists(sizes):
    heapq.heapify(sizes)
    total_cost = 0

    while len(sizes) > 1:
        first = heapq.heappop(sizes)
        second = heapq.heappop(sizes)
        cost = first + second
        total_cost += cost
        heapq.heappush(sizes, cost)
    return total_cost
# Function: Run Experimental Tests
def run_experiment():
    input_sizes = [5, 10, 50, 100, 500, 1000, 2000, 3000, 5000,10000,20000,50000]
    experimental_times = []
    theoretical_values = []
    for n in input_sizes:
        # create random list sizes
        sizes = [random.randint(1, 1000) for _ in range(n)]
        # measure runtime
        start_time = time.perf_counter_ns()
        merge_sorted_lists(sizes.copy())
        end_time = time.perf_counter_ns()
        elapsed = end_time - start_time
        experimental_times.append(elapsed)
        # theoretical value: O(n log n)
        theoretical_values.append(n * math.log2(n))
        print(f"n = {n:<5} | Time (ns) = {elapsed}")
    return input_sizes, experimental_times, theoretical_values

# Function: Compute Scaling Constant (Median) and Display Table
def compute_scaling(input_sizes, exp, theo):
    ratios = [e / t for e, t in zip(exp, theo)]
    scaling_constant = statistics.median(ratios)
    scaled_theoretical = [t * scaling_constant for t in theo]
    # prepare output table
    df = pd.DataFrame({
        "n": input_sizes,
        "Experimental (ns)": exp,
        "Theoretical": [round(t, 3) for t in theo],
        "Ratio (Exp/Theo)": [round(r, 4) for r in ratios],
        "Scaling Constant (Median)": [round(scaling_constant, 4)] * len(exp),
        "Scaled Theoretical (ns)": [round(st, 3) for st in scaled_theoretical]
    })

    print("\n=== Output Numerical Data ===")
    print(df.to_string(index=False))

    return df, scaling_constant, scaled_theoretical


# Function: Plot Results
def plot_results(input_sizes, experimental, scaled_theoretical):
    plt.figure(figsize=(8, 6))
    plt.plot(input_sizes, experimental, marker='o', label='Experimental Time (ns)')
    plt.plot(input_sizes, scaled_theoretical, marker='s', linestyle='--',
             label='Scaled Theoretical O(n log n)')

    plt.title("Experimental vs Scaled Theoretical Time Complexity\n(Merging Sorted Lists)")
    plt.xlabel("Number of Lists (n)")
    plt.ylabel("Time (nanoseconds)")
    plt.legend()
    plt.grid(True)
    plt.show()


# Main Execution
if __name__ == "__main__":
    input_sizes, exp, theo = run_experiment()
    df, scale, scaled_theo = compute_scaling(input_sizes, exp, theo)
    plot_results(input_sizes, exp, scaled_theo)

    print(f"\nMedian Scaling Constant = {scale:.4f}")

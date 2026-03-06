import pandas as pd
import random

def generate_sample():
    lines = random.randint(20, 400)
    functions = random.randint(0, 10)
    loops = random.randint(0, 15)
    conditionals = random.randint(0, 20)
    nested_depth = random.randint(0, 5)

    # Simulated average function length
    if functions > 0:
        avg_function_length = round(lines / functions, 2)
    else:
        avg_function_length = 0

    # Cyclomatic complexity approximation
    cyclomatic_complexity = loops + conditionals + functions + 1

    # Weighted score logic
    score = (
        lines * 0.01 +
        functions * 0.5 +
        loops * 0.7 +
        conditionals * 0.3 +
        nested_depth * 1.5 +
        cyclomatic_complexity * 0.4
    )

    # Strong rule-based labeling

    if nested_depth >= 3 or cyclomatic_complexity > 25:
        label = "Complex"

    elif (
            nested_depth == 2
            or cyclomatic_complexity > 12
            or avg_function_length > 40
    ):
        label = "Moderate"

    else:
        label = "Clean"

    return {
        "lines_of_code": lines,
        "num_functions": functions,
        "num_loops": loops,
        "num_conditionals": conditionals,
        "nested_loop_depth": nested_depth,
        "avg_function_length": avg_function_length,
        "cyclomatic_complexity": cyclomatic_complexity,
        "label": label
    }

def generate_dataset(n=1500):
    data = [generate_sample() for _ in range(n)]
    df = pd.DataFrame(data)
    df.to_csv("../data/training_dataset.csv", index=False)
    print("Updated dataset generated successfully!")

if __name__ == "__main__":
    generate_dataset()
import sys
import pandas as pd
import numpy as np

def main():
    if len(sys.argv) != 5:
        print("Usage: topsis input.csv weights impacts output.csv")
        sys.exit()

    input_file = sys.argv[1]
    weights = sys.argv[2].split(',')
    impacts = sys.argv[3].split(',')
    output_file = sys.argv[4]

    try:
        data = pd.read_csv(input_file)
    except:
        print("File not found")
        sys.exit()

    if data.shape[1] < 3:
        print("Input file must have at least 3 columns")
        sys.exit()

    values = data.iloc[:, 1:]

    try:
        values = values.astype(float)
    except:
        print("From 2nd to last columns must be numeric")
        sys.exit()

    if len(weights) != values.shape[1] or len(impacts) != values.shape[1]:
        print("Weights, impacts and columns mismatch")
        sys.exit()

    weights = np.array(weights, dtype=float)

    for i in impacts:
        if i not in ['+', '-']:
            print("Impacts must be + or -")
            sys.exit()

    norm = np.sqrt((values**2).sum())
    norm_data = values / norm
    weighted = norm_data * weights

    best, worst = [], []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            best.append(weighted.iloc[:, i].max())
            worst.append(weighted.iloc[:, i].min())
        else:
            best.append(weighted.iloc[:, i].min())
            worst.append(weighted.iloc[:, i].max())

    best = np.array(best)
    worst = np.array(worst)

    d_pos = np.sqrt(((weighted - best)**2).sum(axis=1))
    d_neg = np.sqrt(((weighted - worst)**2).sum(axis=1))

    score = d_neg / (d_pos + d_neg)
    data['Topsis Score'] = score
    data['Rank'] = score.rank(ascending=False).astype(int)

    data.to_csv(output_file, index=False)
    print("TOPSIS completed successfully")

if __name__ == "__main__":
    main()

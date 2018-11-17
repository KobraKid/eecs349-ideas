import pandas as pd
import json
import os

def get_data_by_line(filename, lines):
    data = []
    count = 1
    with open(filename, 'rb') as f:
        for line in f:
            data.append(line)
            if lines == 0 or int(lines) == 0:
                continue
            if count == int(lines):
                break
            else:
                count = count + 1
    return data

def main():
    """
    main
    """
    data = get_data_by_line('Kickstarter_2018-10-18.json', 50)
    df = None
    for d in data:
        if df is None:
            df=pd.read_json(d)
        else:
            pd.concat([df, pd.read_json(d)])
    print(df.head(5))

main()
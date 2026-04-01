import pandas as pd
from config import VOLUME_THRESHOLD

def detect_issues(df):
    zero_volume = df[df["volume"] == 0]
    low_volume = df[
        (df["volume"] > 0) & 
        (df["volume"] < VOLUME_THRESHOLD)
    ]
    
    flagged = {
        "zero": zero_volume,
        "low": low_volume
    }
    
    return flagged


if __name__ == "__main__":
    from query_data import get_daily_volumes
    
    df = get_daily_volumes()
    flagged = detect_issues(df)
    
    print("Zero volume clients:")
    print(flagged["zero"])
    print("\nLow volume clients:")
    print(flagged["low"])
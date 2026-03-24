import pandas as pd
import io


def save_dataframe(df: pd.DataFrame, add_index: bool = False) -> io.BytesIO:
    """Export DataFrame to a binary stream in the specified format."""
    output = io.BytesIO()
    df.to_csv(output, index=add_index)
    output.seek(0)
    return output

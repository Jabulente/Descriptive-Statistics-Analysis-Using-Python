import pandas as pd
import numpy as np

def summary_stats(df, group):
    """
    Calculate comprehensive statistics (mean ± SEM) for all numeric columns grouped by a specified column,
    including grand mean, SEM, and coefficient of variation.
    
    Parameters:
    - df: Input DataFrame
    - group: Column name to group by
    
    Returns:
    - Formatted DataFrame with statistics
    """
    # Identify numeric columns
    Metrics = df.select_dtypes(include=np.number).columns.tolist()
    
    # Calculate overall statistics
    df_without_location = df.drop(columns=[group])
    grand_mean = df_without_location[Metrics].mean()
    sem = df_without_location[Metrics].sem()
    cv = df_without_location[Metrics].std() / df_without_location[Metrics].mean() * 100
    
    # Calculate grouped statistics
    grouped = df.groupby(group)[Metrics].agg(['mean', 'sem']).reset_index()
    
    # Format the output
    summary_df = pd.DataFrame()
    for col in Metrics:
        summary_df[col] = grouped.apply(
            lambda x: f"{x[(col, 'mean')]:.2f} ± {x[(col, 'sem')]:.2f}", axis=1
        )
    
    summary_df.insert(0, group, grouped[group])
    
    # Add grand mean, SEM and CV rows
    grand_mean_row = ['Grand Mean'] + [f"{x:.2f}" for x in grand_mean.tolist()]
    sem_row = ['SEM'] + [f"{x:.2f}" for x in sem.tolist()]
    cv_row = ['%CV'] + [f"{x:.2f}%" for x in cv.tolist()]
    
    summary_df.loc[len(summary_df)] = grand_mean_row
    summary_df.loc[len(summary_df)] = sem_row
    summary_df.loc[len(summary_df)] = cv_row
    
    return summary_df

# Example usage
if __name__ == "__main__":
    # Load your dataset
    df = pd.read_csv("../Datasets/Iris Dataset.csv")
    
    # Generate summary statistics
    results = summary_stats(df, group='Species')
    
    # Display transposed results for better readability
    display(results)

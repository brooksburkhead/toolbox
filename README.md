# Data Science Functions

This repository contains a set of commonly used data science functions that can be imported into any project. These functions are designed to streamline common tasks related to data exploration and analysis.

## Table of Contents

- [EDA Functions](#eda-functions)
  - [get_metadata](#get_metadata)
  - [identify_id_columns](#identify_id_columns)
  - [identify_null_columns](#identify_null_columns)
  - [find_unary_columns](#find_unary_columns)
  - [find_binary_columns](#find_binary_columns)
- [Data Visualization Functions](#data-visualization-functions)
  - [plot_correlation_matrix](#plot_correlation_matrix)
  - [plot_distribution](#plot_distribution)
  - [plot_categorical_counts](#plot_categorical_counts)

## EDA Functions

### get_metadata

```python
def get_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate metadata for a given DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing metadata.
    """
    # Implementation details...
```

### identify_id_columns

```python
def identify_id_columns(df: pd.DataFrame, threshold: float = 90) -> pd.DataFrame:
    """
    Identify columns with high cardinality, suggesting potential identifier columns.

    Args:
        df (pd.DataFrame): Input DataFrame.
        threshold (float, optional): Threshold percentage for identifying high cardinality columns. Defaults to 90.

    Returns:
        pd.DataFrame: DataFrame containing identified columns.
    """
    # Implementation details...

```

### identify_null_columns

```python
def identify_null_columns(df: pd.DataFrame, threshold: float = 75) -> pd.DataFrame:
    """
    Identifies columns with high null percentage.

    Args:
        df (pd.DataFrame): Input DataFrame.
        threshold (float, optional): Threshold percentage for identifying columns with high null percentage. Defaults to 75.

    Returns:
        pd.DataFrame: DataFrame containing identified columns.
    """
    # Implementation details...
```

### find_unary_columns

```python
def find_unary_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify unary columns in a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame or str: DataFrame containing identified columns or a message if none are found.
    """
    # Implementation details...
```

### find_binary_columns

```python
def find_binary_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify binary columns in a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame or str: DataFrame containing identified columns or a message if none are found.
    """
    # Implementation details...
```

## Data Visualization Functions

### plot_correlation_matrix

```python
def plot_correlation_matrix(df: pd.DataFrame, figsize=(10, 8)):
    """
    Visualize the correlation matrix of a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        figsize (tuple): Figure size for the plot.

    Returns:
        None
    """
    # Implementation details...
```

### plot_distribution

```python
def plot_distribution(df: pd.DataFrame, column, figsize=(8, 6)):
    """
    Plot the distribution of a numerical column in a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Name of the numerical column.
        figsize (tuple): Figure size for the plot.

    Returns:
        None
    """
    # Implementation details...
```

### plot_categorical_counts

```python
def plot_categorical_counts(df: pd.DataFrame, column, figsize=(8, 6)):
    """
    Visualize counts of categorical values in a column.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Name of the categorical column.
        figsize (tuple): Figure size for the plot.

    Returns:
        None
    """
    # Implementation details...

```

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def get_metadata(df: pd.DataFrame) -> pd.DataFrame:
  """
   Generate metadata for a given DataFrame.

  Args:
      df (pd.DataFrame): Input DataFrame
      
  Raises:
      ValueError: If the input is not a Pandas DataFrame.
      ValueError: If the input DataFrame is empty
      
  Returns:
      pd.DataFrame: DataFrame containing metadata.
  """
  
  #input validation
  if not isinstance(df, pd.DataFrame):
    raise ValueError("Input must be a Pandas DataFrame")
  
  #check if DataFrame is empty
  if df.empty:
    raise ValueError("Cannot generate metadata for empty DataFrame!")
  
  metadata_df = pd.DataFrame()
  metadata_df['Data Types'] = df.dtypes
  metadata_df['Memory'] = df.memory_usage( deep = True, index = False )
  metadata_df['Rows'] = df.shape[0]
  metadata_df['Nulls'] = df.isnull().sum()
  metadata_df['Null %'] = metadata_df['Nulls'] / df.shape[0] * 100
  metadata_df = pd.concat([metadata_df, df.describe(include = 'all').transpose().astype({"count" : "int"})], axis = 'columns').rename(columns = {"top" : "mode", "50%" : "median"})
  metadata_df['unique'] = df.nunique()
  
  return metadata_df

def identify_id_columns( df: pd.DataFrame, threshold: float = 90 ) -> pd.DataFrame:
  """
  Identify columns with high cardinality, suggesting potential identifier columns.

  Args:
      df (pd.DataFrame): Input DataFrame.
      threshold (float, optional): Threshold percentage for identifying high cardinality columns. Defaults to 90.

  Raises:
      ValueError: If the input is not a Pandas DataFrame.
      ValueError: If the threshold is not a percentage between 0 and 100.

  Returns:
      pd.DataFrame: DataFrame containing identified columns.
  """
  
  #input validation
  if not isinstance(df, pd.DataFrame):
    raise ValueError("Input must be a Pandas DataFrame.")
  
  #check if threshold is a valid percentage
  if not 0 <= threshold <= 100:
    raise ValueError("Threshold must be a percentage between 0 and 100.")
  
  metadata = get_metadata( df )
  high_cardinality_filter = ( metadata["unique"] >= threshold/100 * metadata["count"] )
  high_cardinality_columns = metadata[ high_cardinality_filter ][["unique","count"]].index
  
  identified_columns_df = df[high_cardinality_columns]
  
  return identified_columns_df

def identify_null_columns( df: pd.DataFrame, threshold: float = 75 ) -> pd.DataFrame:
  """
  Identifies columns with high null percentage.

  Args:
      df (pd.DataFrame): Input DataFrame
      threshold (float, optional): Threshold percentage for identifying columns with high null percentage. Defaults to 75.

  Raises:
      ValueError: If the input is not a Pandas DataFrame.
      ValueError: If the threshold is not a percentage between 0 and 100.

  Returns:
      pd.DataFrame or str: DataFrame containing identified columns or a message if none are found.
  """
  #input validation
  if not isinstance(df, pd.DataFrame):
    raise ValueError("Input must be a Pandas DataFrame.")
  
  #check if threshold is a valid percentage
  if not 0 <= threshold <= 100:
    raise ValueError("Threshold must be a percentage between 0 and 100.")
  
  metadata = get_metadata( df )
  high_null_filter = ( metadata["Null %"] >= threshold )
  high_null_columns = metadata[ high_null_filter ].index
  
  if high_null_columns.empty:
    return f"No columns found with more than {threshold}% nulls"
  
  identified_columns_df = df[high_null_columns]
  
  return identified_columns_df

def find_unary_columns( df: pd.DataFrame ) -> pd.DataFrame:
  """
  Identify unary columns in a DataFrame

  Args:
      df (pd.DataFrame): Input DataFrame

  Raises:
      ValueError: If the input is not a Pandas DataFrame

  Returns:
      pd.DataFrame or str: DataFrame containing identified columns or a message if none are found.
  """
  
  #input validation
  if not isinstance(df, pd.DataFrame):
    raise ValueError("Input must be a Pandas DataFrame.")
  
  metadata = get_metadata( df )
  unary_filter = ( metadata["unique"] == 1 )
  unary_columns = metadata[ unary_filter ].index
  
  if unary_columns.empty:
    return "No unary columns found"
  
  identified_unary_columns = df[unary_columns]
  
  return identified_unary_columns

def find_binary_columns( df: pd.DataFrame )-> pd.DataFrame:
  """
  Identify binary columns in a DataFrame

  Args:
      df (pd.DataFrame): Input DataFrame

  Raises:
      ValueError: If the input is not a Pandas DataFrame

  Returns:
      pd.DataFrame or str: DataFrame containing identified columns or a message if none are found.
  """
  
  #input validation
  if not isinstance(df, pd.DataFrame):
    raise ValueError("Input must be a Pandas DataFrame.")
  
  metadata = get_metadata( df )
  binary_filter = ( metadata["unique"] == 2 )
  binary_columns = metadata[ binary_filter ].index
  
  if binary_columns.empty:
    return "No binary columns found"
  
  identified_binary_columns = df[binary_columns]
  
  return identified_binary_columns
                          
def plot_correlation_matrix(df: pd.DataFrame, figsize=(10, 8)) -> None:
    """
    Visualize the correlation matrix of a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        figsize (tuple): Figure size for the plot.

    Returns:
        None
    """
    corr_matrix = df.corr()
    plt.figure(figsize=figsize)
    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Matrix")
    plt.show()

def plot_distribution(df: pd.DataFrame, column, figsize=(8, 6)) -> None:
    """
    Plot the distribution of a numerical column in a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Name of the numerical column.
        figsize (tuple): Figure size for the plot.

    Returns:
        None
    """
    plt.figure(figsize=figsize)
    sns.histplot(df[column], kde=True)
    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.show()

def plot_categorical_counts(df: pd.DataFrame, column, figsize=(8, 6)) -> None:
    """
    Visualize counts of categorical values in a column.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Name of the categorical column.
        figsize (tuple): Figure size for the plot.

    Returns:
        None
    """
    plt.figure(figsize=figsize)
    sns.countplot(x=column, data=df, order=df[column].value_counts().index)
    plt.title(f"Counts of {column}")
    plt.xlabel(column)
    plt.ylabel("Count")
    plt.show()





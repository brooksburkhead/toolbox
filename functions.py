import pandas as pd

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

def id_columns_drop( list_of_cols_to_drop, df ) -> None:

  
  df.drop( list_of_cols_to_drop, axis = 1, inplace = True )
  
  return None

def null_columns_identify( df: pd.DataFrame, threshold: float = 75 ) -> pd.DataFrame:
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
  
  #include metadata in output
  identified_columns_df.metadata = metadata.loc[high_null_columns]
  
  return identified_columns_df

def null_columns_drop( cols, df ):
  '''
  Given a list of columns to delete from a data frame, deletes the columns in-place
  '''
  
  return id_columns_drop( cols, df )

def null_rows_identify( df: pd.DataFrame, threshold = 5 ) -> pd.DataFrame:
  '''
  Identify rows will enough nulls to drop
  '''
  
  md = get_metadata( df )
  filter = ( ( md["Null %"] <= threshold ) & ( md["Nulls"] > 0 ) )
  return  md[ filter ][["Rows", "Nulls","Null %"]].sort_values( by = ["Null %"], ascending = False )

def null_rows_drop( cols, df ):
  '''
  Given a list of columns, deletes the rows with nulls in-place
  '''
  
  df.dropna(subset = cols , how='any', inplace = True )
  return None

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


def find_binary_columns( df ):
  '''
  Given a dataframe, returns a meta dataframe of binary columns
  '''
  
  md = get_metadata( df )
  filter = ( ( md["Data Types"] == "object" ) & ( md["unique"] == 2 ) )
  return md[ filter ]
                          
def encode_binary( cols, df ):
  '''
  Drops binary column, one-hot encodes binary columns, and keeps only one column.
  Returns a modified data frame.
  '''

  one_hot =  pd.get_dummies(df[ cols ], drop_first = True )
  return df.drop( columns = cols ).join( one_hot )

def find_object_with_low_counts( df, threshold = 20 ):
  '''
  Given a dataframe, returns a meta dataframe of object columns with fewer than {threshold} counts.
  '''

  md = get_metadata( df )
  filter = ( ( md["unique"] >= 3 ) & ( md["unique"] <= threshold ) & ( md["Data Types"] == "object") )
  return md[ filter ].sort_values( by = "unique", ascending = False )

def encode_objects( cols, df ):
  '''
  Drops object columns and one-hot encodes object columns.
  Returns a modified data frame.
  '''
  return df.drop( columns = cols ).join( pd.get_dummies(df[ cols ] ) )





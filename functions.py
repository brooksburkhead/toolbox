import pandas as pd
def get_metadata(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
  '''
  Given a dataframe, returns new dataframe containing metadata for given dataframe.
  '''
  metadata_df = pd.DataFrame()
  metadata_df['Data Types'] = df.dtypes
  metadata_df['Memory'] = df.memory_usage(deep = True)
  metadata_df['Rows'] = df.shape[0]
  metadata_df['Nulls'] = df.isnull().sum()
  metadata_df['Null %'] = metadata_df['Nulls'] / df.shape[0] * 100
  metadata_df = pd.concat([metadata_df, df.describe(include = 'all').transpose().astype({"count" : "int"})], axis = 'columns').rename(columns = {"top" : "mode", "50%" : "median"})
  metadata_df['unique'] = df.nunique()
  return metadata_df

def id_columns_identify( df, threshold = 90 ):
  '''
  Identifies columns that could be IDs. Returns a data frame for review.
  '''
  
  md = get_metadata( df )
  filter = ( md["unique"] >= threshold/100 * md["count"] )
  cols_to_del = md[ filter ][["unique","count"]].index
  return df[ cols_to_del ].head()

def id_columns_drop( list_of_cols_to_drop, df ):
  '''
  Given a list of columns to delete from a data frame, deletes the columns in-place
  '''
  
  df.drop( list_of_cols_to_drop, axis = 1, inplace = True )
  return None

def null_columns_identify( df, threshold = 75 ):
  '''
  Identify columns will enough nulls to drop
  '''
  
  md = get_metadata( df )
  filter = ( md["Null %"] >= threshold )
  md[ filter ]
  return md[ filter ][["Rows","Nulls","Null %"]]

def null_columns_drop( cols, df ):
  '''
  Given a list of columns to delete from a data frame, deletes the columns in-place
  '''
  
  return id_columns_drop( cols, df )


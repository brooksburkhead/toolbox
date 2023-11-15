import pandas as pd
def get_metadata(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
  '''
  Given a dataframe, returns new dataframe containing metadata for given dataframe.
  '''
  metadata_df = pd.DataFrame()
  metadata_df['Data Types'] = df.dtypes
  metadata_df['Memory'] = df.memory_usage( deep = True, index = False )
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

def null_rows_identify( df, threshold = 5 ):
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

def find_unary_columns( df ):
  '''
  Given a dataframe, returns a meta dataframe of unary columns
  '''
  md = get_metadata( df )
  filter = ( md["unique"] == 1 )
  return md[ filter ]


def columns_drop( cols, df ):
  '''
  Given a list of columns to delete from a data frame, deletes the columns in-place
  '''
  
  df.drop( cols, axis = 1, inplace = True )
  return None

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





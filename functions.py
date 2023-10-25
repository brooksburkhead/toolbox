def get_metadata(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
  ''' Given a dataframe, returns new dataframe containing metadata for given dataframe.

  '''
  metadata_df = pd.DataFrame()
  metadata_df['Nulls'] = df.isnull().sum()
  metadata_df['Null %'] = metadata_df['Nulls'] / df.shape[0] * 100
  metadata_df['Data Types'] = df.dtypes
  metadata_df['Memory'] = df.memory_usage(deep = True)
  metadata_df = pd.concat([metadata_df, df.describe(include = 'all').transpose()], axis = 'columns')

  return metadata_df

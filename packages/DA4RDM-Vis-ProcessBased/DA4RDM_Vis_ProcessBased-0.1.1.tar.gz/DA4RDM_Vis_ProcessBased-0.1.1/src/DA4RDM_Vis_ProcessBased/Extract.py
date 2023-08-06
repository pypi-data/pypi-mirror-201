"""
This function returns the dataframe extracted from the log files(specifically message part)
"""


def extract_data(data_path):
    import pandas as pd
    import json
    import sys
    try:
        chunk_size = 100000

        # Create an empty dataframe to hold the data
        df = pd.DataFrame()

        # Iterate over the chunks
        for chunk in pd.read_csv(data_path, chunksize=chunk_size, delimiter=";"):
            # Process the chunk
            # ...

            # Append the processed chunk to the dataframe
            df = pd.concat([df, chunk])

        # df = pd.read_csv(data_path, sep=";")
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Please verify the path provided for the data")
    try:
        res = df.Message.apply(json.loads) \
            .apply(pd.json_normalize) \
            .pipe(lambda x: pd.concat(x.values))
        key_column_list = ['Type', 'Operation', 'Timestamp', 'UserId', 'ProjectId']
        dataframe = res[key_column_list]
        dataframe = dataframe[dataframe.Type == 'Action']
        dataframe = dataframe[dataframe.ProjectId != '']
        # dataframe['FileId'] = dataframe['FileId'].str.extract(r'([^/]+$)')
    except Exception as e:
        sys.exit("Oops! " + str(e.__class__) + " occurred. Please verify the data format")
    return dataframe

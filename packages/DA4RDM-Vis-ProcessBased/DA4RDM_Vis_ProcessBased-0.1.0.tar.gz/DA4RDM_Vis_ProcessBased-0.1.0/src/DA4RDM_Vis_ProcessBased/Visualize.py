import pandas as pd
import pm4py
from dateutil.relativedelta import relativedelta
from DA4RDM_Vis_ProcessBased.Evaluate_Fitness import evaluate_fitness
import plotly_express as px
from DA4RDM_Vis_ProcessBased.Extract import extract_data
from datetime import datetime
import os


def visualize(fitness_list):
    filename = "Radarchart.png"
    fitness_values = fitness_list[1:]
    categories = ['Planning', 'Production', 'Analysis', 'Archival', 'Access', 'Reuse']
    df1 = pd.DataFrame(dict(
        r=fitness_values,
        theta=categories))
    fig = px.line_polar(df1, r='r', theta='theta', line_close=True, range_r=[0, 1], )
    fig.update_traces(fill='toself')
    fig.write_image(filename, format="png")
    absolute_path = os.path.dirname(__file__)
    relative_path = filename
    full_path = os.path.join(absolute_path, relative_path)
    return full_path
    


def process_vis(dataset_user_interactions, project_id, earliest_timestamp, last_timestamp):
    data_extracted = extract_data(dataset_user_interactions)
    index = pd.Index(range(0, len(data_extracted), 1))
    data_extracted = data_extracted.set_index(index)
    data_extracted = data_extracted[["UserId", "ProjectId", "Operation", "Timestamp"]]
    data_project_filtered = data_extracted[data_extracted.ProjectId == project_id]
    data_project_filtered = data_project_filtered[["UserId", "Operation", "Timestamp"]]
    data_project_filtered["SessionId"] = ""
    data_project_filtered = data_project_filtered.sort_values(['Timestamp'], ascending=True)
    data_project_time_filtered = data_project_filtered.loc[
        (data_project_filtered['Timestamp'] >= earliest_timestamp) & (
                data_project_filtered['Timestamp'] <= last_timestamp)]
    userid_list = data_project_time_filtered["UserId"].unique()
    data_project_time_filtered["SessionId"] = ""
    for user_id in userid_list:
        data_user = data_project_time_filtered[data_project_time_filtered.UserId == user_id]
        while len(data_user.Operation.value_counts()) > 0:
            trace_length = 0
            date_time = data_user['Timestamp'].iloc[0]
            date = pd.to_datetime(date_time).date()
            time_adjustment = datetime.min.time()
            start_time = datetime.combine(date, time_adjustment)
            added_time_window = start_time + relativedelta(hours=+24)
            end_time = added_time_window.strftime('%Y-%m-%d %H:%M:%S.%f')
            start_time = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')
            data_time_filtered = data_user.loc[(data_user['Timestamp'] >= start_time) &
                                               (data_user['Timestamp'] < end_time)]
            index = list(data_time_filtered.index.values)
            sessionId = str(data_time_filtered["UserId"].iloc[0]) + data_time_filtered['Timestamp'].iloc[0]
            for idx in index:
                data_project_time_filtered.loc[idx, 'SessionId'] = sessionId
            trace = data_time_filtered["Operation"].to_list()
            trace_length = trace_length + len(trace)
            row_length = len(data_user.index)
            data_user = data_user.iloc[trace_length:row_length]

    data_to_mine = pm4py.format_dataframe(data_project_time_filtered, case_id='SessionId',
                                          activity_key='Operation', timestamp_key='Timestamp')
    event_log_from_data = pm4py.convert_to_event_log(data_to_mine)
    fitness_list = [project_id]
    fitness_list = fitness_list + evaluate_fitness(event_log_from_data)
    image_path = visualize(fitness_list)
    return image_path

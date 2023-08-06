import pandas as pd
import pm4py
import pkg_resources


def calculate_fitness(phase_data, log):
    phase_to_mine = pm4py.format_dataframe(phase_data, case_id='case:concept:name',
                                           activity_key='concept:name', timestamp_key='time:timestamp')
    phase_log = pm4py.convert_to_event_log(phase_to_mine)
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(phase_log)
    alignment_based_fitness = pm4py.fitness_alignments(log, net, initial_marking, final_marking)
    return alignment_based_fitness['averageFitness']


def evaluate_fitness(log_to_confirm):
    phase_data_planning = pd.read_csv(pkg_resources.resource_filename('DA4RDM_Vis_ProcessBased', 'PhaseData/Planning.csv'), sep=",")
    phase_data_production = pd.read_csv(pkg_resources.resource_filename('DA4RDM_Vis_ProcessBased', 'PhaseData/Production.csv'), sep=",")
    phase_data_analysis = pd.read_csv(pkg_resources.resource_filename('DA4RDM_Vis_ProcessBased', 'PhaseData/Analysis.csv'), sep=",")
    phase_data_archival = pd.read_csv(pkg_resources.resource_filename('DA4RDM_Vis_ProcessBased', 'PhaseData/Archival.csv'), sep=",")
    phase_data_access = pd.read_csv(pkg_resources.resource_filename('DA4RDM_Vis_ProcessBased', 'PhaseData/Access.csv'), sep=",")
    phase_data_reuse = pd.read_csv(pkg_resources.resource_filename('DA4RDM_Vis_ProcessBased', 'PhaseData/Reuse.csv'), sep=",")

    fitness_list = list()
    phase_list = [phase_data_planning, phase_data_production, phase_data_analysis, phase_data_archival,
                  phase_data_access, phase_data_reuse]

    for idx, phase in enumerate(phase_list):
        fitness = calculate_fitness(phase, log_to_confirm)
        fitness_list.append(fitness)
    return fitness_list

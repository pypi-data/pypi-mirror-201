from time import perf_counter

from numpy import fill_diagonal, int64
from pandas import DataFrame, Series, concat, unique

from sberpm._holder import DataHolder
from sberpm.miners._abstract_miner import AbstractMiner
from sberpm.miners._simple_miner import SimpleMiner
from sberpm.visual import NodeType
from sberpm.visual._graph import Graph


def get_parallelism_table(data_holder, unique_activities):
    def intersected(activity_to_timedelta: DataFrame, activity: str, adjacent_activity: str):
        # ? TODO return null for equal right here
        count = 0

        # ? TODO from groupby

        for timestamp_pair in activity_to_timedelta[activity]:
            for adjacent_timestamp_pair in activity_to_timedelta[adjacent_activity]:
                if timestamp_pair[0] == adjacent_timestamp_pair[0]:
                    if (
                        timestamp_pair[0] == timestamp_pair[1]
                        or adjacent_timestamp_pair[0] == adjacent_timestamp_pair[1]
                    ):  # a == c and (a == b or a == d)
                        count += 1
                else:
                    if (
                        timestamp_pair[0] < adjacent_timestamp_pair[0]
                        and timestamp_pair[1] > adjacent_timestamp_pair[0]
                    ) or (
                        timestamp_pair[0] > adjacent_timestamp_pair[0]
                        and adjacent_timestamp_pair[1] > timestamp_pair[0]
                    ):  # a < c and b > c
                        count += 1

        return count

    start_timestamps = (
        data_holder.data[data_holder.start_timestamp_column].fillna(0.0).map(lambda datetime: datetime.timestamp())
    ).astype(int64)
    duration_seconds = (data_holder.data[data_holder.duration_column].fillna(0.0)).astype(int64)
    after_duration_timestamps = Series(start_timestamps + duration_seconds, name="end_timestamp")

    activity_timestamp_data = concat(
        [data_holder.data[data_holder.activity_column], start_timestamps, after_duration_timestamps], axis=1
    )
    timedelta_grouped_by_activity = activity_timestamp_data.groupby(data_holder.activity_column)

    activity_timedelta_mapping = timedelta_grouped_by_activity[
        data_holder.start_timestamp_column, "end_timestamp"
    ].apply(
        lambda timestamps_frame: tuple(
            zip(
                tuple(timestamps_frame[data_holder.start_timestamp_column]),
                tuple(timestamps_frame["end_timestamp"]),
            )
        )
    )
    # ? dict()
    activity_timedelta_mapping = dict(activity_timedelta_mapping)

    adjacency_table = DataFrame(0.0, unique_activities, unique_activities)
    activity_amount = timedelta_grouped_by_activity.size()

    for activity in unique_activities:
        paired_activity_amount = activity_amount[activity] + activity_amount
        activity_intersections = tuple(
            intersected(activity_timedelta_mapping, activity, adjacent_activity)
            for adjacent_activity in unique_activities
        )

        adjacency_table[activity] = (activity_intersections / paired_activity_amount * 2).values

    fill_diagonal(adjacency_table.values, 0.0)  # null diagonal intersections

    return adjacency_table


def get_parallel_groups(linked_table):
    table = linked_table.copy()  # ? TODO rm
    min_bound = table.mean().mean()

    parallel_groups = []

    while table.max().max() > min_bound:
        parallel_node = table.max().idxmax()
        parallel_group = [parallel_node]

        parallel_group.extend(iter(table.loc[table[parallel_node] > min_bound].index))
        parallel_groups.append(parallel_group)

        table.drop(index=parallel_group, columns=parallel_group, inplace=True)

    return parallel_groups


def _update_parallel_edges(
    graph: Graph,
    groups: list,
) -> Graph:
    graph_edges = graph.get_edges()
    for idx, group in enumerate(groups):
        parallel_node_id = f"parallel_{str(idx)}"
        graph.add_node(
            node_id=parallel_node_id,
            label="||",
            node_type=NodeType.PARALLEL_GATEWAY_BLUE,
        )
        for node in group:
            graph.add_edge(parallel_node_id, node)

        for edge in graph_edges:
            if edge.target_node.label in group:
                try:
                    graph.add_edge(edge.source_node.id, parallel_node_id)
                except Exception:  # FIXME
                    pass
                graph.remove_edge_by_src_trg_id(edge.source_node.id, edge.target_node.id)
    return graph


class ParallelMiner(AbstractMiner):
    """
    Miner to analyze parallel activities.
    Counts intersections on timestamps of the activities.
    Parallel stages are those with such instances of processes that their start and 
    end times overlap.
	A node `parallel_metric` is added, which shows the number of intersections of time by 
    this stage and other stages.

    Parameters:
        data_holder: DataHolder
            Object that contains the event log and the names of its necessary columns.

    Args:
        graph: mined graph of the process to draw

    Examples:
    >>> from sberpm.miners import ParallelMiner
    >>> miner = ParallelMiner(data_holder=data_holder)
    >>> miner.apply()
    >>> from sberpm import DataHolder
    >>> import pandas as pd
    >>>
    >>> df = pd.DataFrame({'id_column': [1, 1, 2, 2, 3, 3],
    >>>                    'activity_column': ['st1', 'st2', 'st1', 'st3', 'st1',
    >>>                                        'st2'],
    >>>                    'start_timestamp_column': ['10.05.2020', '10.09.2020',
    >>>                                               '10.03.2020', '10.04.2020',
    >>>                                               '10.05.2020', '10.05.2020']})
    >>>
    >>> data_holder = DataHolder(data=df,
    >>>                          id_column='id_column',
    >>>                          activity_column='activity_column',
    >>>                          start_timestamp_column='start_timestamp_column',
    >>>                          time_format='%d.%m.%Y')
    """

    def __init__(self, data_holder: DataHolder):
        super().__init__(data_holder)

        self.graph = None
        self._data_holder.check_or_calc_duration()  # ? TODO rm

    def apply(self):
        # Create graph
        simple_miner = SimpleMiner(self._data_holder)
        simple_miner.apply()
        graph = simple_miner.graph

        unique_activities = unique(self._data_holder.data[self._data_holder.activity_column])

        parallelism_table = get_parallelism_table(self._data_holder, unique_activities)
        parallel_groups = get_parallel_groups(parallelism_table)
        # Create parallel edges
        self.graph = _update_parallel_edges(graph, parallel_groups)

        node_metric_dict = parallelism_table.max().to_dict()
        flatten_parallel_groups = sum(parallel_groups, [])

        for node in node_metric_dict.keys():
            if node not in flatten_parallel_groups:
                node_metric_dict[node] = 0.0

        self.graph.add_node_metric("parallel_metric", node_metric_dict)

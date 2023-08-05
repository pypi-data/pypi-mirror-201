import teradataml as tdml
from tdsense.utils import create_table, insert_into
from scipy.cluster.hierarchy import dendrogram, linkage,cut_tree
from scipy.spatial.distance import squareform
from matplotlib import pyplot as plt
from matplotlib import rcParams
import numpy as np
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from sklearn.cluster import DBSCAN
import tqdm
from scipy.cluster.hierarchy import set_link_color_palette

from matplotlib.pyplot import cm
import matplotlib as mpl


def dtw(df, curveid_reference, field='calculated_resistance', row_axis='time_no_unit', series_id='curve_id',radius=100, distance='Manhattan'):

    query = f"""
    SELECT
		{curveid_reference} AS CURVE_ID_1
	,	A.{series_id} AS CURVE_ID_2
	,	A.WARPDISTANCE AS DISTANCE
	FROM (EXECUTE FUNCTION TD_DTW
	(
		SERIES_SPEC(TABLE_NAME({df._table_name}),ROW_AXIS(SEQUENCE({row_axis})), SERIES_ID({series_id}),
		PAYLOAD(FIELDS({field}), CONTENT(REAL))),
		SERIES_SPEC(TABLE_NAME({df._table_name}),ROW_AXIS(SEQUENCE({row_axis})), SERIES_ID({series_id}),
		PAYLOAD(FIELDS({field}), CONTENT(REAL))) WHERE {series_id} = {curveid_reference},
		FUNC_PARAMS(
		    RADIUS({radius}),
		    DISTANCE('{distance}')
		),
		INPUT_FMT(INPUT_MODE(MANY2ONE))
		)
	) A

    """

    return tdml.DataFrame.from_query(query)


def query_dtw_triangle(df, curveids, no, field='calculated_resistance', row_axis='time_no_unit', series_id='curve_id',radius=100, distance='Manhattan',query_only=False):
    df._DataFrame__execute_node_and_set_table_name(df._nodeid, df._metaexpr)

    curveids.sort()

    query = f"""
    SELECT
        CAST({no} AS BIGINT) AS MATRIX_ROW
	,	CAST({curveids[no]} AS BIGINT) AS CURVE_ID_1
	,	CAST(A.{series_id} AS BIGINT) AS CURVE_ID_2
	,	A.ROW_I
	,	A.WARPDISTANCE AS DISTANCE
	FROM (EXECUTE FUNCTION TD_DTW
	(
		SERIES_SPEC(TABLE_NAME({df._table_name}),ROW_AXIS(SEQUENCE({row_axis})), SERIES_ID({series_id}),
		PAYLOAD(FIELDS({field}), CONTENT(REAL))) WHERE {series_id} < {curveids[no]} AND {series_id} IN ({','.join([str(x) for x in curveids])}),
		SERIES_SPEC(TABLE_NAME({df._table_name}),ROW_AXIS(SEQUENCE({row_axis})), SERIES_ID({series_id}),
		PAYLOAD(FIELDS({field}), CONTENT(REAL))) WHERE {series_id} = {curveids[no]},
		FUNC_PARAMS(
		    RADIUS({radius}),
		    DISTANCE('{distance}')
		),
		INPUT_FMT(INPUT_MODE(MANY2ONE))
		)
	) A

    """

    if query_only:
        return query

    return tdml.DataFrame.from_query(query)


def dtw_distance_matrix_computation(df, curveids, table_name, schema_name, field='calculated_resistance', row_axis='time_no_unit', series_id='curve_id',radius=100, distance='Manhattan'):

    for no in range(1, len(curveids)):
        dtw_query = query_dtw_triangle(df, curveids, no, field=field, row_axis=row_axis,
                               series_id=series_id, radius=radius, distance=distance, query_only=True)
        if no == 1:
            tdml.DataFrame.from_query(dtw_query).to_sql(table_name=table_name,schema_name=schema_name,if_exists='replace')
        else:
            tdml.get_context().execute(insert_into(dtw_query,table_name,schema_name))


    return tdml.DataFrame.from_table(tdml.in_schema(schema_name,table_name))

def dtw_distance_matrix_computation(df, table_name, schema_name, field='calculated_resistance', row_axis='time_no_unit', series_id='curve_id',radius=100, distance='Manhattan'):

    for no in range(1, len(curveids)):
        dtw_query = query_dtw_triangle(df, curveids, no, field=field, row_axis=row_axis,
                               series_id=series_id, radius=radius, distance=distance, query_only=True)
        if no == 1:
            tdml.DataFrame.from_query(dtw_query).to_sql(table_name=table_name,schema_name=schema_name,if_exists='replace')
        else:
            tdml.get_context().execute(insert_into(dtw_query,table_name,schema_name))


    return tdml.DataFrame.from_table(tdml.in_schema(schema_name,table_name))

def dtw_distance_matrix_computation(df, table_name, schema_name, field='calculated_resistance', row_axis='time_no_unit', series_id='curve_id',radius=100, distance='Manhattan'):

    for no in range(1, len(curveids)):
        dtw_query = query_dtw_triangle(df, curveids, no, field=field, row_axis=row_axis,
                               series_id=series_id, radius=radius, distance=distance, query_only=True)
        if no == 1:
            tdml.DataFrame.from_query(dtw_query).to_sql(table_name=table_name,schema_name=schema_name,if_exists='replace')
        else:
            tdml.get_context().execute(insert_into(dtw_query,table_name,schema_name))


    return tdml.DataFrame.from_table(tdml.in_schema(schema_name,table_name))
def get_dtw_distance_matrix_local(dtw_matrix_vantage):

    return dtw_matrix.sort(columns=['CURVE_ID_2','CURVE_ID_1']).to_pandas(all_rows=True)

def extractmatrixlabel(dtw_matrix_vantage_local):
    X = dtw_matrix_vantage_local.DISTANCE.values
    labelList = [dtw_matrix_vantage_local.iloc[0,2]] + list(dtw_matrix_vantage_local.iloc[0:int(np.floor(np.sqrt(len(X)*2))),1])
    return X, labelList

def hierarchy_dendrogram(dtw_matrix_vantage_local, cluster_distance = 'single'):

    X, labelList = extractmatrixlabel(dtw_matrix_vantage_local)

    rcParams.update({'font.size': 22})

    linked = linkage(X, cluster_distance)

    plt.figure(figsize=(25, 15))
    Z = dendrogram(linked,
                   orientation='top',
                   labels=labelList,
                   distance_sort='ascending',
                   show_leaf_counts=True)
    plt.rcParams.update({'font.size': 22})
    ax = plt.gca()
    ax.tick_params(axis='x', which='major', labelsize=15)

    return linked, labelList


from scipy.cluster.hierarchy import dendrogram, linkage, cut_tree, set_link_color_palette
import pandas as pd
from matplotlib.pyplot import cm
import matplotlib as mpl


def hierarchy_clustering(linked, labelList, n_clusters=None, height=None, plot_dendrogram=True):
    if n_clusters is not None:
        cutree_ = cut_tree(linked, n_clusters=n_clusters)
    if height is not None:
        cutree_ = cut_tree(linked, height=height)

    # Get the cluster labels for each data point
    cluster_labels = cutree_.flatten()

    cl = [x[0] for x in cutree_]
    n_clusters = len(set(cl))
    clusters = pd.DataFrame()
    clusters['CURVE_ID'] = labelList
    clusters['cluster'] = cl

    thresh = np.sort(-linked[:, 2])
    thresh = -thresh[n_clusters - 1] + 1e-10

    cmap = cm.rainbow(np.linspace(0, 1, n_clusters))
    set_link_color_palette([mpl.colors.rgb2hex(rgb[:3]) for rgb in cmap])

    if plot_dendrogram:
        # Create a figure and plot the dendrogram with the cluster colors
        fig, ax = plt.subplots(figsize=(15, 15))
        dn = dendrogram(linked, color_threshold=thresh)

        df = pd.DataFrame(columns=['leaves_color_list'])
        df['leaves_color_list'] = dn['leaves_color_list']
        df['cluster'] = [cl[x] for x in dn['leaves']]
        df['CURVE_ID'] = [labelList[x] for x in dn['leaves']]
        df.drop_duplicates(inplace=True)
        df_ = df.copy().drop('CURVE_ID',axis=1).drop_duplicates()
        # Create a list of labels for the clusters
        cluster_labels = ['Cluster ' + str(x['cluster']) for i, x in df_.iterrows()]
        plt.legend(cluster_labels)

        clusters = df[list(clusters.columns) + ['leaves_color_list']].sort_values('CURVE_ID')

    return clusters




def distance_elbow(dtw_matrix_vantage_local):
    X, labelList = extractmatrixlabel(dtw_matrix_vantage_local)
    neigh = NearestNeighbors(n_neighbors=2)
    nbrs = neigh.fit(squareform(X))
    distances, indices = nbrs.kneighbors(squareform(X))
    distances = np.sort(distances, axis=0)
    distances = distances[:, 1]
    plt.plot(distances)
    return

def densityscan(dtw_matrix_vantage_local, eps, min_samples):
    X, labelList = extractmatrixlabel(dtw_matrix_vantage_local)
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(squareform(X))
    clusters = pd.DataFrame()
    clusters['CURVE_ID'] = labelList
    clusters['cluster'] = db.labels_
    return clusters


def query_dtw_triangle2(df, curveids, no, field='calculated_resistance', row_axis='time_no_unit', series_id='curve_id',
                        radius=100, distance='Manhattan', query_only=False):
    df1 = df[df[series_id] < curveids[no]]
    df1._DataFrame__execute_node_and_set_table_name(df1._nodeid, df1._metaexpr)
    df2 = df[df[series_id] == curveids[no]]
    df2._DataFrame__execute_node_and_set_table_name(df2._nodeid, df2._metaexpr)

    query = f"""
    SELECT
        CAST({no} AS BIGINT) AS MATRIX_ROW
	,	CAST({curveids[no]} AS BIGINT) AS {series_id}_1
	,	CAST(A.{series_id} AS BIGINT) AS {series_id}_2
	,	A.ROW_I
	,	A.WARPDISTANCE AS DISTANCE
	FROM (EXECUTE FUNCTION TD_DTW
	(
		SERIES_SPEC(TABLE_NAME({df1._table_name}),ROW_AXIS(SEQUENCE({row_axis})), SERIES_ID({series_id}),
		PAYLOAD(FIELDS({field}), CONTENT(REAL))),
		SERIES_SPEC(TABLE_NAME({df2._table_name}),ROW_AXIS(SEQUENCE({row_axis})), SERIES_ID({series_id}),
		PAYLOAD(FIELDS({field}), CONTENT(REAL))) WHERE {series_id} = {curveids[no]},
		FUNC_PARAMS(
		    RADIUS({radius}),
		    DISTANCE('{distance}')
		),
		INPUT_FMT(INPUT_MODE(MANY2ONE))
		)
	) A

    """

    if query_only:
        return query

    return tdml.DataFrame.from_query(query)


def dtw_distance_matrix_computation2(df, table_name, schema_name, curveids=None, field='calculated_resistance',
                                     row_axis='time_no_unit', series_id='curve_id', radius=100, distance='Manhattan',
                                     restart=1):
    # get the list of curve ids
    if curveids == None:
        filter_curveid = {'drop_columns': True, series_id: df[series_id].distinct()}
        curveids = list(df.assign(**filter_curveid).sort(series_id).to_pandas()[series_id])

    # create the table to store the results
    if restart == 1:
        # only in this case we recreate the table from scratch
        res = pd.DataFrame(columns=['MATRIX_ROW', series_id + '_1', series_id + '_2', 'ROW_ID', 'DISTANCE'])
        tdml.copy_to_sql(res,
                         schema_name=schema_name,
                         table_name=table_name,
                         if_exists='replace',
                         types={
                             'MATRIX_ROW': tdml.BIGINT,
                             series_id + '_1': tdml.BIGINT,
                             series_id + '_2': tdml.BIGINT,
                             'ROW_ID': tdml.BIGINT,
                             'DISTANCE': tdml.FLOAT
                         })

    progress_bar = tqdm.tqdm(range(1, len(curveids)))
    for no in progress_bar:

        if no >= restart:
            progress_bar.set_description(f"Process curve {curveids[no]}")
            dtw_query = query_dtw_triangle2(df, curveids, no, field=field, row_axis=row_axis,
                                            series_id=series_id, radius=radius, distance=distance, query_only=True)
            query = f'''
                INSERT INTO {schema_name}.{table_name} (MATRIX_ROW, {series_id + '_1'}, {series_id + '_2'}, ROW_ID, DISTANCE)
                {dtw_query}
            '''
            tdml.get_context().execute(query)
        else:
            progress_bar.set_description(f"Skip curve {curveids[no]}")

    return tdml.DataFrame.from_table(tdml.in_schema(schema_name, table_name))

def resample(df, duration, field, series_id, row_axis, start_value=0, interpolate='LINEAR',query_only=False):
    df._DataFrame__execute_node_and_set_table_name(df._nodeid, df._metaexpr)

    query = f"""
    SELECT
        {series_id}
    ,   ROW_I AS {row_axis}
    ,   {field}
    FROM (
        EXECUTE FUNCTION
        TD_RESAMPLE
        (
            SERIES_SPEC (
                TABLE_NAME ({df._table_name}),
                SERIES_ID ({series_id}),
                ROW_AXIS (SEQUENCE ({row_axis})),
                PAYLOAD (
                    FIELDS ({field}),
                    CONTENT (REAL)
                )
            ),
            FUNC_PARAMS (
                SEQUENCE (START_VALUE ({start_value}), DURATION ({duration})),
                INTERPOLATE ('{interpolate}')
            )
            )
        ) A
    """

    if query_only:
        return query

    return tdml.DataFrame.from_query(query)
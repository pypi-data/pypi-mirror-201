import teradataml as tdml
import io
from IPython.display import Image
import imageio


def plotcurves(df, field='calculated_resistance', row_axis='time_no_unit', series_id='curve_id', select_id=None,
               width=1024, height=768, noplot=False, color=None, row_axis_type='SEQUENCE', plot_type='line'):
    df._DataFrame__execute_node_and_set_table_name(df._nodeid, df._metaexpr)

    if isinstance(select_id, list):
        if len(series_id) > 0:
            filter_ = f"WHERE {series_id} IN ({','.join([str(x) for x in select_id])}),"
        else:
            filter_ = ','
    else:
        if select_id is not None:
            filter_ = f"WHERE {series_id} = {select_id},"
        else:
            filter_ = ','



    nb_series = df[[series_id]+[row_axis]].groupby(series_id).count().shape[0]

    n = 1
    if type(series_id) == list:
        n = len(series_id)
        series_id = ','.join(series_id)

    if color == None:
        color = ''
    else:
        color = f",FORMAT('{color}')"


    if nb_series < 1025:
        query = f"""
        EXECUTE FUNCTION
            TD_PLOT(
                SERIES_SPEC(
                TABLE_NAME({df._table_name}),
                ROW_AXIS({row_axis_type}({row_axis})),
                SERIES_ID({series_id}),
                PAYLOAD (
                    FIELDS({field}),
                    CONTENT(REAL)
                )
            )
            {filter_}
            FUNC_PARAMS(
            TITLE('{field}'),
            PLOTS[(
            TYPE('{plot_type}')
            {color}
            )],
            WIDTH({width}),
            HEIGHT({height})
            )
            );
        """
    else:
        df_ = df.assign(**{series_id: 1})
        df_._DataFrame__execute_node_and_set_table_name(df_._nodeid, df_._metaexpr)
        query = f"""
        EXECUTE FUNCTION
            TD_PLOT(
                SERIES_SPEC(
                TABLE_NAME({df_._table_name}),
                ROW_AXIS({row_axis_type}({row_axis})),
                SERIES_ID({series_id}),
                PAYLOAD (
                    FIELDS({field}),
                    CONTENT(REAL)
                )
            )
            {filter_}
            FUNC_PARAMS(
            TITLE('{field}'),
            PLOTS[(
            TYPE('scatter')
            {color}
            )],
            WIDTH({width}),
            HEIGHT({height})
            )
            );
        """

    if tdml.display.print_sqlmr_query:
        print(query)

    res = tdml.get_context().execute(query).fetchall()

    stream_str = io.BytesIO(res[0][1 + n])

    if noplot:
        return imageio.imread(stream_str.getvalue())
    else:
        return Image(stream_str.getvalue())

def plotcurvescluster(df, cluster, no_cluster, schema, field='calculated_resistance', row_axis='time_no_unit', series_id='CURVE_ID', select_id=None):

    tdml.copy_to_sql(df=cluster,table_name='cluster_temp',if_exists='replace',schema_name=schema)

    df_cluster = tdml.DataFrame(tdml.in_schema(schema,'cluster_temp'))
    df_select = df.join(df_cluster[df_cluster.cluster == no_cluster],
                        how='inner',
                        on=f'{series_id}=CURVE_ID', rsuffix='r',
                        lsuffix='l')
    try:
        df_select = df_select.assign(**{series_id: df_select['l_' + series_id]}).drop(
            columns=[f'l_{series_id}', 'r_CURVE_ID'])
    except:
        1==1
    df_select.shape


    return plotcurves(df_select,field=field, row_axis=row_axis, series_id=series_id,select_id=select_id)

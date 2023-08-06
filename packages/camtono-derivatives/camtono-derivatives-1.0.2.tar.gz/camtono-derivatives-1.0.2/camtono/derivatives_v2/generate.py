def generate_multi_query_skeleton(input_query_sets, output_queries, grain, selects, group_by, table_prefix,
                                  dialect_name):
    from camtono.derivatives.generate import generate_table_query, generate_output_column_queries
    from camtono.derivatives.selects import extract_select_output
    from camtono.derivatives_v2.selects import get_final_policy_selects
    from camtono.derivatives_v2.union_query_formatting import remove_policy_uuid_columns_from_selects
    queries = generate_filters(input_query_sets=input_query_sets,
                               grain=grain, selects=selects,
                               group_by=group_by, table_prefix=table_prefix, dialect_name=dialect_name)
    output_queries = generate_output_column_queries(output_queries=output_queries, selects=selects,
                                                    table_prefix=table_prefix, dialect_name=dialect_name)
    if not queries:
        queries = [output_queries]
    base_table_name = list(queries[-1].keys())[0]
    queries[0].update(output_queries)

    final_select = remove_policy_uuid_columns_from_selects(selects['final']) + get_final_policy_selects(list(queries[-1].values())[0]['schema'])
    if len(final_select) == 1:
        final_select.append({'name': 't0_policy_uuids', 'value': 'policy_uuids', 'type': 'ARRAY'})
    final_query = {
        'select': extract_select_output(select=final_select),
        'from': [
            dict(value=base_table_name, name='base'),
            *[
                dict(
                    join=dict(
                        value=i['table_name'], name='sub_feature_{}'.format(idx)
                    ),
                    on={"eq": ["base.{}".format(grain), "sub_feature_{idx}.{grain}".format(idx=idx, grain=grain)]}
                ) for idx, i in enumerate(output_queries.values()) if i['table_name'] != base_table_name
            ]
        ]
    }
    table_name, query_body = generate_table_query(select=final_select, table_prefix=table_prefix, ast=final_query,
                                                  dialect_name=dialect_name)
    queries.append({table_name: query_body})
    return queries


def generate_filters(input_query_sets, grain, selects: dict, group_by, table_prefix, dialect_name):
    from camtono.derivatives.generate import generate_table_query
    from camtono.derivatives.selects import extract_select_output
    from camtono.derivatives_v2.union_query_formatting import remove_policy_uuid_columns_from_selects, get_list_policy_columns, create_select_for_unioned_query, create_union_filter, wrap_union_ast_in_subquery
    queries = [dict(), dict()]

    for idx, query_set in enumerate(input_query_sets):
        root_queries, combination_queries = generate_filter(input_idx=idx, input_query_set=query_set, grain=grain,
                                                            table_prefix=table_prefix, selects=selects,
                                                            group_by=group_by, dialect_name=dialect_name)
        queries[0].update(root_queries)
        queries[1].update(combination_queries)
    if len(queries[1]) > 1:
        union_ast = dict(union_all=[])
        base_select = remove_policy_uuid_columns_from_selects(extract_select_output(selects['filter']))
        all_policy_columns = get_list_policy_columns(queries[1])
        for query_info in queries[1].values():
            union_ast['union_all'].append(
                {
                    "select": create_select_for_unioned_query(base_select, all_policy_columns, query_info['schema']),
                    'from': dict(value=query_info['table_name'], name='t0')
                }
            )
        final_ast = wrap_union_ast_in_subquery(base_select, all_policy_columns, group_by.get('final'), union_ast)

        base_table_name, table_body = generate_table_query(
            select=create_union_filter(selects['filter'], all_policy_columns), ast=final_ast,
            table_prefix=table_prefix, dialect_name=dialect_name
        )
        queries.append({base_table_name: table_body})
    return [i for i in queries if i]



def generate_filter(input_idx, input_query_set, grain, table_prefix, selects, group_by, dialect_name):
    from camtono.derivatives.generate import generate_table_query
    from camtono.derivatives.selects import extract_select_output
    root_queries = dict()
    sub_ast = {'from': [], 'select': extract_select_output(select=selects['f{}'.format(input_idx)]),
               "groupby": group_by['f{}'.format(input_idx)]}

    for query_idx, query in enumerate(input_query_set):
        table_name, body = generate_table_query(ast=query['ast'], table_prefix=table_prefix,
                                                select=selects[query['feature_id']], dialect_name=dialect_name)
        root_queries[table_name] = body
        from_ = dict(
            value=table_name,
            name='t{}'.format(query_idx)
        )
        if sub_ast['from']:
            sub_ast['from'].append(dict(join=from_, on={
                'eq': ['t0.{}'.format(grain), 't{table_number}.{grain}'.format(table_number=query_idx, grain=grain)]}))
            sub_ast['from'].append({'cross join': {'name': f't{query_idx}_policy_uuid', 'value': {'unnest': f't{query_idx}.policy_uuids'}}})

        else:
            sub_ast['from'].append(from_)
            sub_ast['from'].append({'cross join': {'name': f't{query_idx}_policy_uuid', 'value': {'unnest': f't{query_idx}.policy_uuids'}}})
    # if len(root_queries) > 1:
    combination_table_name, combination_table_body = generate_table_query(
        select=selects['f{}'.format(input_idx)],
        ast=sub_ast,
        table_prefix=table_prefix,
        dialect_name=dialect_name
    )
    combination_tables = {combination_table_name: combination_table_body}
    # else:
    #     combination_tables = root_queries
    #     root_queries = dict()
    return root_queries, combination_tables
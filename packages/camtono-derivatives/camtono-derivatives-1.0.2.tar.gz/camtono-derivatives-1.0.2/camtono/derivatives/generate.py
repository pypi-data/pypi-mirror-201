def generate_table_name(data, prefix=None):
    import json
    import uuid
    import hashlib
    if prefix is None:
        prefix = ""
    hash_id = hashlib.md5(
        str(json.dumps(data, sort_keys=True)).encode('utf-8')
    ).hexdigest()
    return prefix + str(hash_id)


def generate_table_query(select, ast, table_prefix, dialect_name):
    from camtono.derivatives.selects import extract_select_schema
    from camtono.parser.clean import prune_ast
    ast = prune_ast(json=ast)
    if table_prefix is None:
        table_prefix = 'camtono_'
    table_name = generate_table_name(data=ast, prefix=table_prefix)
    body = dict(query_ast=ast, table_name=table_name,
                schema=extract_select_schema(select=select, dialect_name=dialect_name))
    return table_name, body


def generate_multi_query_skeleton(input_query_sets, output_queries, grain, selects, group_by, table_prefix,
                                  dialect_name):
    from camtono.derivatives.selects import extract_select_output
    queries = generate_filters(input_query_sets=input_query_sets,
                               grain=grain, selects=selects,
                               group_by=group_by, table_prefix=table_prefix, dialect_name=dialect_name)
    output_queries = generate_output_column_queries(output_queries=output_queries, selects=selects,
                                                    table_prefix=table_prefix, dialect_name=dialect_name)
    if not queries:
        queries = [output_queries]
    base_table_name = list(queries[-1].keys())[0]
    queries[0].update(output_queries)

    final_query = {
        'select': extract_select_output(select=selects['final']),
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
        ],
        'groupby': group_by.get('final')
    }
    table_name, query_body = generate_table_query(select=selects['final'], table_prefix=table_prefix, ast=final_query,
                                                  dialect_name=dialect_name)
    queries.append({table_name: query_body})
    return queries


def generate_filters(input_query_sets, grain, selects: dict, group_by, table_prefix, dialect_name):
    from camtono.derivatives.selects import extract_select_output
    queries = [dict(), dict()]

    for idx, query_set in enumerate(input_query_sets):
        root_queries, combination_queries = generate_filter(input_idx=idx, input_query_set=query_set, grain=grain,
                                                            table_prefix=table_prefix, selects=selects,
                                                            group_by=group_by, dialect_name=dialect_name)
        queries[0].update(root_queries)
        queries[1].update(combination_queries)
    if len(queries[1]) > 1:
        base_query = dict(
            union_all=[
                {
                    "select": extract_select_output(select=selects['filter']),
                    'from': dict(value=i['table_name'], name='t0')
                }
                for i in queries[1].values()
            ]
        )
        base_table_name, table_body = generate_table_query(
            select=selects['filter'], ast=base_query,
            table_prefix=table_prefix, dialect_name=dialect_name
        )
        queries.append({base_table_name: table_body})
    return [i for i in queries if i]


def generate_output_column_queries(output_queries, selects, table_prefix, dialect_name):
    queries = dict()
    for query in output_queries:
        table_name, query_body = generate_table_query(
            select=selects[query['feature_id']],
            ast=query['ast'],
            table_prefix=table_prefix,
            dialect_name=dialect_name
        )
        queries[table_name] = query_body
    return queries


def generate_filter(input_idx, input_query_set, grain, table_prefix, selects, group_by, dialect_name):
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
        else:
            sub_ast['from'].append(from_)
    if len(root_queries) > 1:
        combination_table_name, combination_table_body = generate_table_query(
            select=selects['f{}'.format(input_idx)],
            ast=sub_ast,
            table_prefix=table_prefix,
            dialect_name=dialect_name
        )
        combination_tables = {combination_table_name: combination_table_body}
    else:
        combination_tables = root_queries
        root_queries = dict()
    return root_queries, combination_tables
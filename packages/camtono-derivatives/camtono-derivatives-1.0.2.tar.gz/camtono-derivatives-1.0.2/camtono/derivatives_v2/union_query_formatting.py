def get_list_policy_columns(combination_queries):
    columns = []
    for value in combination_queries.values():
        for column in value['schema']:
            if column['name'].endswith('_policy_uuids'):
                columns.append(column['name'])
    # need to sort because selected columns in unioned queries have to have matching column orders
    columns = sorted(list(set(columns)))
    return columns

def remove_policy_uuid_columns_from_selects(selects):
    new_select = []
    for select in selects:
        if select['name'] == 'policy_uuids' or select['name'].endswith('_policy_uuids'):
            continue
        new_select.append(select)
    return new_select


def get_policy_selects_from_schema(schema):
    selects = []
    for column in schema:
        name = column['name']
        if name == 'policy_uuids' or name.endswith('_policy_uuids'):
            if name == 'policy_uuids':
                name = 't0_policy_uuids'
            selects.append({'value': f"t0.{column['name']}", 'name': name})
    return selects

def get_missing_policy_column(column_name):
    return {'value': {'split': {'literal': ' '}}, 'name': column_name}


def add_missing_policy_columns_to_policy_selects(selects, all_policy_columns):
    select_policy_columns = {}
    for column in selects:
        if column['name'] == 'policy_uuids' or column['name'].endswith('_policy_uuids'):
            select_policy_columns[column['name']] = True

    for column_name in all_policy_columns:
        if column_name not in select_policy_columns:
            selects.append(get_missing_policy_column(column_name))



def create_select_for_unioned_query(base_select, all_policy_columns, query_schema):

    policy_selects = get_policy_selects_from_schema(query_schema)

    add_missing_policy_columns_to_policy_selects(policy_selects, all_policy_columns)

    final_select = [value for value in base_select] + policy_selects
    return final_select

def create_union_filter(filters, all_policy_columns):
    final_filter = []
    for value in filters:
        if value['name'] != 'policy_uuids' and not value['name'].endswith('_policy_uuids'):
            final_filter.append(value)

    for column in all_policy_columns:
        final_filter.append({'name': column, 'value': f't0.{column}', 'type': 'ARRAY'})

    return final_filter



def wrap_union_ast_in_subquery(base_select, all_policy_columns, group_by, union_ast):
    from camtono.derivatives.transforms import apply_transforms
    from_ast = ['t0']
    select_ast = [value for value in base_select]
    for policy_name in all_policy_columns:
        policy_prefix = policy_name.split('_')[0]
        from_ast.append({'cross join': {'name': f'{policy_prefix}_policy_uuid', 'value': {'unnest': f'{policy_name}'}}})

        value, data_type = apply_transforms(value=f'{policy_prefix}_policy_uuid'
                                            , data_type='ARRAY'
                                            , transforms=[{'name':'array_agg_distinct'}] #output['transforms']
                                            )
        select_ast.append(
            dict(
                name=policy_name,
                value=value,
                type=data_type
            )
        )
    ast = {'select':select_ast
            , 'from':from_ast
            , 'groupby':[group.replace('base', 't0') for group in group_by]
            , 'with': {'name': 't0',
                       'value': union_ast
           }
        }
    return ast
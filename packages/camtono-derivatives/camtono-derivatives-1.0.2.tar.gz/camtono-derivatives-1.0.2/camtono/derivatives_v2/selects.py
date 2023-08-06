def generate_select_mapping(default_inputs, definition_outputs, input_query_sets, input_features, grain,
                            feature_map, output_queries, definition_groupings, definition_features) -> tuple:
    from camtono.derivatives.selects import generate_feature_select, generate_final_select

    filter_select, filter_group_by = generate_filter_selects(definition_outputs=definition_outputs, grain=grain,
                                                             feature_map=definition_features, input_query_sets=input_query_sets,
                                                             subquery_groupings=[i for i in definition_groupings if
                                                                                 i.get('aggregate_sub_queries')])
    feature_outputs = generate_feature_select(feature_map=feature_map, default_inputs=default_inputs)
    final_select, final_group_by = generate_final_select(filter_select=filter_select['filter'],
                                                         grain=grain,
                                                         feature_outputs=feature_outputs,
                                                         definition_outputs=definition_outputs,
                                                         input_features=input_features,
                                                         output_queries=output_queries,
                                                         definition_groupings=definition_groupings)

    select_mapping = dict(
        final=final_select,
        **filter_select,
        **feature_outputs
    )

    group_by = dict(
        final=final_group_by,
        **filter_group_by
    )
    return select_mapping, group_by


def generate_filter_selects(definition_outputs, grain, feature_map, input_query_sets, subquery_groupings):
    from camtono.derivatives.transforms import apply_transforms
    from camtono.derivatives.selects import generate_base_filter_select_mapping, generate_group_by
    filter_select, filter_groupings, common_output, shared_output = generate_base_filter_select_mapping(
        grain=grain,
        feature_map=feature_map,
        definition_outputs=definition_outputs, subquery_groupings=subquery_groupings
    )
    for idx, input_query_set in enumerate(input_query_sets):
        input_select = []
        base_values = dict()
        for output in shared_output:
            if 'value' in output.keys():
                continue
            elif output['column_name'] not in common_output.keys():
                raise ValueError("{} is not shared by all features".format(output['column_name']))
            elif output['column_name'] == 'policy_uuids' and output.get('transform_sub_queries'):
                name = output['column_name']
                value = 't0.{}'.format(output['column_name'])
                data_type = common_output[output['column_name']]['data_type']
                base_values[name] = value
                inputs = []
                for i in range(len(input_query_set)):
                    value, data_type = apply_transforms(value='t{idx}_policy_uuid'.format(idx=i)
                                                        , data_type=data_type
                                                        , transforms=[{'name':'array_agg_distinct'}] #output['transforms']
                                                    )
                    inputs.append(
                        dict(
                            name='t{idx}_policy_uuids'.format(idx=i),
                            value=value,
                            type=data_type
                        )
                    )
                input_select.extend(inputs)
            else:
                name = output['column_name']
                value = 't0.{}'.format(output['column_name'])
                data_type = common_output[output['column_name']]['data_type']
                base_values[name] = value

                if output.get('transform_sub_queries'):
                    value = [
                        't{idx}.{column_name}'.format(idx=i, column_name=output['column_name']) for i in
                        range(len(input_query_set))
                    ]
                    base_values[name] = value
                    value, data_type = apply_transforms(
                        value=value, data_type=data_type,
                        transforms=output['transforms']
                    )
                input_select.append(
                    dict(
                        name=name,
                        value=value,
                        type=data_type,
                    )
                )

        filter_select['f{idx}'.format(idx=idx)] = input_select
        filter_groupings['f{idx}'.format(idx=idx)] = generate_group_by(groupings=subquery_groupings,
                                                                       base_values=base_values)
    return filter_select, filter_groupings


def get_final_policy_selects(schema):
    columns = []
    for column in schema:
        if column['name'].endswith('_policy_uuids'):
            columns.append(column['name'])
    columns = sorted(list(set(columns)))
    return [{'name': column, 'value': f'{column}', 'type': 'ARRAY'} for column in columns]
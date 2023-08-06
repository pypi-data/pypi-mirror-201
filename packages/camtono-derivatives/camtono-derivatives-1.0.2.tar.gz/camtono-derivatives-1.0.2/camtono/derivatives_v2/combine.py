def generate_derivative(definition: dict, feature_map: dict, desired_dialect,
                        new_table_prefix: str = None):
    """Create a derived query ast based on a definition and map of all used features

    :param definition: camtono derivative definition
    :param feature_map: dictionary of feature_id: feature details that are referenced in the defintion
    :param single_query: generate a single query_ast or an ordered list of arrays that
    :param new_table_prefix: string used when referencing new tables in multiple
    :return:
    """
    from camtono.derivatives.combine import standardize_input_attributes, combine_query_lists
    from camtono.derivatives.filters import flatten_filters, generate_filters_query_sets
    from camtono.derivatives_v2.generate import generate_multi_query_skeleton
    from camtono.derivatives_v2.selects import generate_select_mapping
    from camtono.derivatives.outputs import generate_output_queries
    filters, default_inputs, feature_inputs = standardize_input_attributes(definition=definition)
    flattened_filters = flatten_filters(filters=filters)
    output_grain = definition['grain']
    mapping_features = [k for k, v in feature_map.items() if v.get('is_mapping_feature')]
    mapping_feature = feature_map[mapping_features[0]] if mapping_features else None
    input_query_sets, input_features, dependent_queries = generate_filters_query_sets(
        flattened_filters=flattened_filters, features=feature_map,
        default_inputs=default_inputs, feature_inputs=feature_inputs, table_prefix=new_table_prefix,
        feature_map=feature_map, dialect_name=desired_dialect, output_grain=output_grain,
        mapping_feature=mapping_feature
    )
    definition_outputs = definition.get('outputs', definition.get('output'))
    if not definition_outputs:
        definition_outputs = [dict(column_name=definition['grain'])]
    output_queries, output_dependencies, output_features = generate_output_queries(
        definition_outputs=definition_outputs,
        default_inputs=default_inputs,
        feature_map=feature_map,
        input_features=input_features,
        feature_inputs=feature_inputs,
        definition_features=[i['feature_id'] for i in definition['features']],
        table_prefix=new_table_prefix, dialect_name=desired_dialect,
        output_grain=output_grain,
        mapping_feature=mapping_feature
    )
    dependent_queries = combine_query_lists(existing_query_lists=dependent_queries, new_query_lists=output_dependencies,
                                            start_index=0)
    feature_map.update(input_features)
    feature_map.update(output_features)
    selects, group_by = generate_select_mapping(
        input_features=input_features,
        default_inputs=default_inputs,
        definition_outputs=definition_outputs,
        input_query_sets=input_query_sets,
        feature_map=feature_map,
        grain=definition['grain'],
        output_queries=output_queries, definition_groupings=definition.get('group_by', []),
        definition_features={k: v for k, v in feature_map.items() if
                             k in {i['feature_id'] for i in definition['features']}}
    )
    queries = generate_multi_query_skeleton(
        input_query_sets=input_query_sets, grain=definition['grain'],
        output_queries=output_queries, selects=selects,
        table_prefix=new_table_prefix, group_by=group_by, dialect_name=desired_dialect
    )
    return [list(i.values()) for i in
            combine_query_lists(existing_query_lists=dependent_queries, new_query_lists=queries,
                                start_index=len(dependent_queries))]



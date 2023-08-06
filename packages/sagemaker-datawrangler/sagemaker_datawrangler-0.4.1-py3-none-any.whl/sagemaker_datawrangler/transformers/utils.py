def get_rare_categories(input_df, input_column):
    rare_categories = []
    frequencies = input_df[input_column].value_counts(normalize=True, ascending=True)
    threshold = frequencies[(frequencies.cumsum() > 0.1).idxmax()]
    for value, frequency in frequencies.items():
        if frequency < threshold:
            rare_categories.append(value)
        else:
            break
    return rare_categories


def parse_and_retain_data_type(data: list, dtype: str) -> list:
    if "int" in dtype:
        data = [int(x) for x in data]
    if "float" in dtype:
        data = [float(x) for x in data]

    return data


def replace(from_values, to_value, input_col):
    code, regex = "", False
    to_value = f"'{to_value}'" if isinstance(to_value, str) else to_value
    for value in from_values:
        # replace empty string with regex
        if value == "":
            value = r"^\s*$"
            regex = True
        value = f"'{value}'" if isinstance(value, str) else value
        replace_dict = {value: to_value}
        code += f"output_df['{input_col}']=output_df['{input_col}'].replace({value}, {to_value}, regex={regex})\n"
    return code


def get_mode(input_df, input_column, values_to_ignore=None):
    impute_value = None
    top_frequent = input_df[input_column].value_counts().index.tolist()
    for val in top_frequent:
        if values_to_ignore == None or val not in values_to_ignore:
            impute_value = val
            break
    return impute_value


def replace_with_None(from_values, to_value, input_col):
    code, regex = "", False
    to_value = f"'{to_value}'" if isinstance(to_value, str) else to_value
    for value in from_values:
        # replace empty string with regex
        if value == "":
            value = r"^\s*$"
            regex = True
        replace_dict = {value: to_value}
        code += f"output_df['{input_col}']=output_df['{input_col}'].replace({replace_dict}, regex={regex})\n"
    return code

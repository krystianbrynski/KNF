def extract_from_pl_codes(pl_dict, codes_dict):
    unified = {}
    all_ids = set(pl_dict.keys()) | set(codes_dict.keys())
    for href_id in all_ids:
        pl_text = pl_dict.get(href_id)
        code_text = codes_dict.get(href_id)
        unified[href_id] = (pl_text, code_text)

    columns_ending_0 = {}
    columns_ending_9 = {}

    for href_id, (pl_text, code_text) in unified.items():
        if not href_id.startswith("uknf_c"):
            continue

        if code_text:
            if code_text.endswith("0"):
                columns_ending_0[href_id] = (pl_text, code_text)
            elif code_text.endswith("9"):
                columns_ending_9[href_id] = (pl_text, code_text)

    sorted_columns_0 = sorted(columns_ending_0.items(), key=lambda item: item[1][1])
    sorted_columns_9 = sorted(columns_ending_9.items(), key=lambda item: item[1][1])
    sorted_cols_0_list = [(href_id, text_pl, text_code) for href_id, (text_pl, text_code) in sorted_columns_0]
    sorted_cols_9_list = [(href_id, text_pl, text_code) for href_id, (text_pl, text_code) in sorted_columns_9]

    for href_id, (text_pl, text_code) in unified.items():
        if href_id.startswith("uknf_tN"):
            headers = text_pl

    columns0 = sorted_cols_0_list
    tabels9 = sorted_cols_9_list

    return columns0, tabels9, headers

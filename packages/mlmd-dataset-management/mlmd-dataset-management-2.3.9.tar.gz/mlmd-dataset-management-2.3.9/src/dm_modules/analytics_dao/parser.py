

def get_parser(parser_name):
    if parser_name == 'redis_cls_parser':
        return redis_cls_output_parser
    else:
        raise ValueError(f"Parser {parser_name} is not supported")
    return None

def redis_cls_output_parser(input_str):
    '''
        Parse output from redis format to list of list (Classifier format) to the groundtruth format
        groundtruth format: [[label, confident_score, xmin, ymin, xmax, ymax],...]
        
        input_str: "<timestamp>:[[index_label, confident_score],...]:[label_1, label_2]:{coords: [[xmin, ymin, xmax, ymax],...], ...}"
        output: [[label, confident_score, xmin, ymin, xmax, ymax],...]
    '''
    import json
    timestamp, prediction, labels, *meta = input_str.split(":")
    labels = json.loads(labels.replace("'", '"'))
    prediction = json.loads(prediction)
    meta = json.loads(":".join(meta).replace("'", '"'))

    output_str = []
    for idx, item in enumerate(prediction):
        label = item[0]
        prob = item[1]
        x1, y1, x2, y2 = meta['coords'][idx]
        output_str.append(f"['{labels[label]}', {prob}, {x1}, {y1}, {x2}, {y2}]")
    output_str = ", ".join(output_str)
    return f"[{output_str}]".replace("'", '"')



def is_detection(model_id):
    return "selectnet" not in model_id and "cls" not in model_id

def get_groundtruth_generator(dataset_id):
    """
    This function is used to get groundtruth generator from firestore
    @dataset_id: dataset_id
    @return: generator of groundtruth
    """
    import dataset_manager as dm
    dataset = dm.get_dataset(dataset_id)
    return dataset.get_filelist(get_annotation=True)

def get_prediction_generator(filepath):
    """
    This function is used to get prediction generator from file
    @filepath: path to prediction file
    @return: generator of prediction
    """
    import os
    if not os.path.isfile(filepath):
        raise Exception("prediction_generator: file {} not found".format(filepath))
    f = open(filepath, "r")
    for line in f:
        yield line.rstrip()

def get_document_map(model_id, gt_gen, prediction_gen):
    """
    This function is used to map groundtruth and prediction to document_id for evaluation
    @model_id: model_id
    @gt_gen: generator of groundtruth
    @prediction_gen: generator of prediction
    @return: document_map = {
        document_id: {
            "gt": [[label, confident_score, xmin, ymin, xmax, ymax],...],
            "pred": [[label, confident_score, xmin, ymin, xmax, ymax],...]
        }
    }

    """
    import json
    model_id = model_id.replace("-", "_")
    gt = next(gt_gen, None)
    prediction = next(prediction_gen, None)
    document_map = {}
    while gt and prediction:
        # convert to dict
        gt = gt.to_dict()
        prediction = prediction.to_dict()

        # get document_id from groundtruth and prediction
        document_id_gt = gt['document_id']
        document_id_pred = prediction['document_id']

        # insert groundtruth and prediction into document_map
        document_map.setdefault(document_id_gt, {})["gt"] = json.loads(gt.get("gt").strip('\"').replace('\\', '').replace("\'", '"'))
        prediction_output = prediction.get(f"{model_id}_output").strip('\"').replace('\\', '')
        document_map.setdefault(document_id_pred, {})["pred"] = json.loads(prediction_output)
        
        # assert that gth and prediction are in correct format [[label, confident_score, xmin, ymin, xmax, ymax],...] where label is a string or number and confident_score is a float 
        for prediction_res in document_map[document_id_pred]["pred"]:
            assert len(prediction_res) == 6, f"prediction doesn't have 6 elements: {prediction_res} for document {document_id_pred} - [[label, confident_score, xmin, ymin, xmax, ymax],...]"
            assert isinstance(prediction_res[0], int) or isinstance(prediction_res[0], str), f"prediction label is not in correct format: {prediction_res} for document {document_id_pred}"
        for gt_res in document_map[document_id_gt]["gt"]:
            assert len(gt_res) == 6, f"groundtruth doesn't have 6 elements: {gt_res} for document {document_id_gt} - [[label, confident_score, xmin, ymin, xmax, ymax],...]"
            assert isinstance(gt_res[0], int) or isinstance(gt_res[0], str), f"groundtruth label is not in correct format: {gt_res} for document {document_id_gt}"

        # get next item from generator
        gt = next(gt_gen, None)
        prediction = next(prediction_gen, None)

    # check if all groundtruth has prediction and vice versa
    for document_id, item in document_map.items():
        assert "gt" in item, f"groundtruth for document {document_id} not found"
        assert "pred" in item, f"prediction for document {document_id} not found"
    
    return document_map


def get_presion_recall(document_map, iou_threshold=0.5):
    """
    This function is used to calculate precision and recall
    @document_map: document_map = {
        document_id: {
            "gt": [[label, confident_score, xmin, ymin, xmax, ymax],...],
            "pred": [[label, confident_score, xmin, ymin, xmax, ymax],...]
        }
    }
    @iou_threshold: threshold for iou (default: 0.5)
    @return: precision, recall
    """
    from dm_modules.analytics_dao.utils.coord_utils import calculate_iou
    
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for document_id, item in document_map.items():

        # check if all groundtruth has prediction and vice versa
        assert "gt" in item, f"groundtruth for document {document_id} not found"
        assert "pred" in item, f"prediction for document {document_id} not found"

        predicted_boxes = item['pred']
        gt_boxes = item['gt']

        for pred_box in predicted_boxes:
            iou_max = 0
            match = None

            for gt_box in gt_boxes:
                iou = calculate_iou(pred_box, gt_box)
                if iou > iou_max:
                    iou_max = iou
                    match = gt_box

            if iou_max >= iou_threshold and match is not None:
                true_positives += 1
                gt_boxes.remove(match)
            else:
                false_positives += 1

        false_negatives += len(gt_boxes)

    print("TP, FP, FN: {} | {} | {}".format(true_positives, false_positives, false_negatives))
    precision = true_positives / (true_positives + false_positives + 0.00000001)
    recall = true_positives / (true_positives + false_negatives + 0.0000000001)

    return precision, recall
def calculate_iou(boxA, boxB):
    """
    Calculate Intersection over Union (IoU) of two bounding boxes
    @boxA: [xmin, ymin, xmax, ymax]
    @boxB: [xmin, ymin, xmax, ymax]
    @return: IoU
    """

    # Calculate the Intersection over Union (IoU) of two bounding boxes
    xA = max(boxA[2], boxB[2])
    yA = max(boxA[3], boxB[3])
    xB = min(boxA[4], boxB[4])
    yB = min(boxA[5], boxB[5])

    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    boxAArea = (boxA[4] - boxA[2] + 1) * (boxA[5] - boxA[3] + 1)
    boxBArea = (boxB[4] - boxB[2] + 1) * (boxB[5] - boxB[3] + 1)

    iou = interArea / float(boxAArea + boxBArea - interArea)

    return iou

def map_bbox_label(bbox_groundtruths, bbox_predictions, iou_threshold=0.5):
    """Map bbox btw groundtruths and preditions in one image one label
    
    Args:
        groundtruths: [[batch_index, label_index, confident_score, xmin, ymin, xmax, ymax],...]
        predictions: [[batch_index, label_index, confident_score, xmin, ymin, xmax, ymax],...]
        iou_threshold: Defaults to 0.5.

    Returns:
        bbox_mapper: [[groundtruth_idx, prediction_idx],...]
    """
    count_true_positives = 0
    bbox_mapper = []
    gt_idx_seen = set()
    for pr_idx, bbox in enumerate(bbox_predictions):
        # assign prediction-results to ground truth object if any
        # open ground-truth with that file_id
        max_iou = -1
        gt_match_idx = -1
        for gt_idx, bbox_gt in enumerate(bbox_groundtruths):
            iou = calculate_single_iou(bbox[-4:], bbox_gt[-4:])
            if iou > max_iou:
                max_iou = iou
                gt_match_idx = gt_idx
        
        if max_iou >= iou_threshold:
            if gt_match_idx not in gt_idx_seen:
                bbox_mapper.append([gt_match_idx, pr_idx])
                gt_idx_seen.add(gt_match_idx)
                count_true_positives += 1
            else:
                # multiple prediction
                bbox_mapper.append([None, pr_idx])
        else:
            # low IOU
            bbox_mapper.append([None, pr_idx])
    # predition missed
    for gt_idx in range(len(bbox_groundtruths)):
        if gt_idx not in gt_idx_seen:
            bbox_mapper.append([gt_idx, None])
    return bbox_mapper
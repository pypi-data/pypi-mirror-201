
def validate(model_id, dataset_id, execution_id):
    """
    @param model_id: model_id
    @param dataset_id: dataset_id
    @param execution_id: execution_id
    @return: precision, recall
    """
    from dm_modules.analytics_dao.prediction_dao import get_prediction_gen
    from dm_modules.analytics_dao.groundtruth_dao import get_groundtruth_gen
    from dm_modules.analytics_dao.utils.validator_utils import get_document_map
    from dm_modules.analytics_dao.utils.validator_utils import get_presion_recall

    prediction_gen = get_prediction_gen(execution_id)
    gt_gen = get_groundtruth_gen(dataset_id, model_id)
    
    document_map = get_document_map(model_id, gt_gen, prediction_gen)
    precision, recall = get_presion_recall(document_map)
    print("Precision/Recall: {}, {}".format(precision, recall))
    return precision, recall

# print(validate("moap_selectnet_2", "moap_selectnet2_intergration_test", "test_f9c98bfb11ba4e09a4d79dddbdc94f7f"))

if __name__ == "__main__":
    validate("moap_conductor_strand_damage_det", "ufd-moap-conductor-strand-test-data-groundtruth", "test_9b2865493b624a0298f087516189e4dc")
    #validate("moap_cabinet_cls", "test_moap_cabinet_cls_3", "test_88bd7dc9f2e44c71ba44e295b93ffc46")
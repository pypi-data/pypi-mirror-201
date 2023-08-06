from dm_modules.analytics_dao.groundtruth_dao import insert_groundtruth
import dataset_manager as dm

dataset_name = "test_moap_ir_hotspot_det_0"
model_id = "moap-ir-hotspot-det"
parser_name = ""


ds = dm.get_dataset(dataset_name)
gen = ds.get_filelist(get_annotation=True)

from dm_modules.analytics_dao.parser import get_parser

parser_func = get_parser(parser_name)

for item in gen:
    gt = parser_func(item[1])
    data = {
        "dataset_id": dataset_name,
        "document_id": item[0],
        "model_id": model_id,
        "gt": gt
    }
    insert_groundtruth(data)
    print(data)
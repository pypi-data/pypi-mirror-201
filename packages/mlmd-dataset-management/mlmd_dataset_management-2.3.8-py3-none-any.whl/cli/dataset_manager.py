import json

def print_prediction(execution_id):
    from dm_modules.analytics_dao.prediction_dao import get_prediction_gen
    gen = get_prediction_gen(execution_id)
    for doc in gen:
        print(doc.to_dict())

def parse_r_detection_label(label, dtype="array_of_objects", filtering_labels=None, filtering_indexes=None):
    try:
        if not label:
            return False
        data = label.split(":")
        if len(data) == 3:
            predictions = json.loads(data[1])
            labels = json.loads(data[2])
        else:
            predictions = json.loads(data[0])
            labels = None
        if len(predictions) <= 0:
            return False
        if dtype == "array_of_objects":
            ret = []
            for idx, prediction in enumerate(predictions):
                if (not filtering_labels or label in filtering_labels) and \
                    (not filtering_indexes or idx in filtering_indexes):
                    label = labels[int(prediction[1])] if labels is not None else str(prediction[1])
                    label = label + " - {}".format(prediction[2])
                    ret.append({
                        "parent_index": int(prediction[0]),
                        "label_index": prediction[1],
                        "label": label,
                        "score": prediction[2],
                        "coord": prediction[3:]
                    })
        else:
            ret = {"label_indexes":[],"scores":[],"coords":[], "parent_indexes":[], "label":[]}
            for idx, prediction in enumerate(predictions):
                label = labels[int(prediction[1])] if labels is not None else str(prediction[1])
                label = label + " - {}".format(prediction[2])
                if (not filtering_labels or label in filtering_labels) and \
                    (not filtering_indexes or idx in filtering_indexes):
                    ret["parent_indexes"].append(int(prediction[0]))
                    ret["label_indexes"].append(prediction[1])
                    ret["label"].append(label)
                    ret["scores"].append(prediction[2])
                    ret["coords"].append(prediction[3:])
        return ret
    except Exception as e:
        print(e)
        return False

def main():
    import sys
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd")
    parser.add_argument('-e', '--execution_id') 
    parser.add_argument('-m', '--model_id') 
    parser.add_argument('-d', '--dataset_id')
    parser.add_argument('-o', '--output_dir')
    parser.add_argument('-c', '--count')
    parser.add_argument('-f', '--filelist')
    args = parser.parse_args()

    arg1 = args.cmd
    if arg1 == "get-prediction":
        execution_id = args.execution_id
        print_prediction(execution_id)
        return
    if arg1 == "get-gt":
        dataset_id = args.dataset_id
        model_id = args.model_id
        from dm_modules.analytics_dao.groundtruth_dao import get_groundtruth_gen
        gen = get_groundtruth_gen(dataset_id, model_id)
        for doc in gen:
            print(doc.to_dict())
        return
    if arg1 == "get-metadata":
        dataset_id = args.dataset_id
        from dm_modules.analytics_dao.metadata_dao import get_metadata_gen
        gen = get_metadata_gen(dataset_id)
        for doc in gen:
            print(doc.to_dict())
        return
    if arg1 == "export-gt":
        dataset_id = args.dataset_id
        model_id = args.model_id
        from dataset_manager.dataset_manager import get_dataset
        from dm_modules.analytics_dao.groundtruth_dao import insert_groundtruth
        ds = get_dataset(dataset_id)
        gen = ds.get_filelist(get_annotation=True)
        for item in gen:
            data = {
                "dataset_id": dataset_id,
                "document_id": item[0],
                "model_id": model_id,
                "gt": item[1]
            }
            insert_groundtruth(data)
        print("OK!")
        return
    if arg1 == "validate":
        from dm_modules.analytics_dao.validator import validate
        execution_id = args.execution_id
        dataset_id = args.dataset_id
        model_id = args.model_id
        validate(model_id, dataset_id, execution_id)
        return
    if arg1 == "get-execution":
        from dm_modules.analytics_dao.moap_execution_dao import get_moap_execution
        execution_id = args.execution_id
        exe = get_moap_execution(execution_id)
        print(exe)
        return
    if arg1 == "get-dataset":
        dataset_name = args.dataset_id
        from dataset_manager.dataset_manager import get_dataset
        ds = get_dataset(dataset_name)
        pretty_json = json.dumps(str(ds), indent=4)
        print(pretty_json)
        return
    if arg1 == "get-samples":
        dataset_name = args.dataset_id
        number_of_samples = int(args.count)
        from dataset_manager.dataset_manager import get_dataset
        ds = get_dataset(dataset_name)
        filelist = ds.get_filelist(get_annotation=True)
        ret = []
        for sample in filelist:
            if len(ret) >= number_of_samples:
                break
            ret.append(sample)
        pretty_json = json.dumps(ret, indent=4)
        print(pretty_json)
        return
    if arg1 == "list-datasets":
        from dataset_manager.dataset_manager import list_datasets
        datasets =list_datasets()
        pretty_json = json.dumps(datasets, indent=4)
        print(pretty_json)
        return
    if arg1 == "download-dataset":
        dataset_name = args.dataset_id
        from dataset_manager.dataset_manager import get_dataset
        ds = get_dataset(dataset_name)
        ds.download_to_dir(".")
        return
    if arg1 == "download-images":
        dataset_name = args.dataset_id
        filelist = args.filelist.split(",")
        from dataset_manager.dataset_manager import get_dataset
        ds = get_dataset(dataset_name)
        ds.download_to_dir(".", filelist=filelist)
        return
    if arg1 == "decorate-with-gt":
        import os
        import numpy as np
        from dataset_management.utils import get_random_color
        from PIL import Image, ImageDraw
        dataset_name = args.dataset_id
        try:
            output_dir = args.output_dir
        except:
            output_dir = "."
        from dataset_manager.dataset_manager import get_dataset
        ds = get_dataset(dataset_name)
        print(f'Finding img files from {os.getcwd()}')
        curr_files = os.listdir(".")
        g = ds.get_filelist(get_annotation=True)
        os.makedirs(output_dir, exist_ok=True)
        color = get_random_color()
        for file_name, annotation in g:
            if file_name not in curr_files:
                continue
            source_img = Image.open(file_name).convert("RGB")
            draw = ImageDraw.Draw(source_img)
            parsed_annotations = json.loads(annotation)
            print(file_name, " => ",parsed_annotations)
            if not parsed_annotations:
                continue
            for ann in parsed_annotations:
                label = ann[0] if type(ann[0]) == str else str(ann[0])
                prob = ann[1]
                coord = np.asarray(ann[2:]) * [source_img.width, source_img.height, source_img.width, source_img.height]
                # coord = np.asarray(ann['coord']) * [source_img.width, source_img.height, source_img.width, source_img.height]
                draw.rectangle(((coord[0], coord[1]), (coord[2], coord[3])), width=3, outline="red")
                draw.text((coord[0] + 10, coord[1]), f'label: {label} - {round(prob, 2)}', fill="red")
            source_img.save(os.path.join(output_dir, file_name), "JPEG")
        return
    if arg1 == "decorate-with-execution":
        import os
        import numpy as np
        from dataset_management.utils import get_random_color
        from PIL import Image, ImageDraw
        execution_id = args.execution_id
        dataset_name = args.dataset_id
        try:
            output_dir = args.output_dir
        except:
            output_dir = "."
        
        print(f'Finding img files from {os.getcwd()}')
        curr_files = os.listdir(".")
        os.makedirs(output_dir, exist_ok=True)

        from dm_modules.analytics_dao.prediction_dao import get_prediction_gen
        g = get_prediction_gen(execution_id)
        for item in g:
            item = item.to_dict()
            file_name = item['document_id']
            if file_name not in curr_files:
                continue
            source_img = Image.open(file_name).convert("RGB")
            draw = ImageDraw.Draw(source_img)

            for k, annotation in item.items():
                if "_output" in k:
                    color = get_random_color()
                    parsed_annotations = eval(json.loads(annotation))
                    print(file_name, " => ",parsed_annotations)
                    if not parsed_annotations:
                        continue
                    for ann in parsed_annotations:
                        label = ann[0] if type(ann[0]) == str else str(ann[0])
                        prob = ann[1]
                        coord = np.asarray(ann[2:]) * [source_img.width, source_img.height, source_img.width, source_img.height]
                        # coord = np.asarray(ann['coord']) * [source_img.width, source_img.height, source_img.width, source_img.height]
                        draw.rectangle(((coord[0], coord[1]), (coord[2], coord[3])), width=3, outline=color)
                        draw.text((coord[0] + 10, coord[1]), f'label: {label} - {round(prob, 2)}', fill=color)
            source_img.save(os.path.join(output_dir, file_name), "JPEG")
        return
    print("Unsupport command: {}".format(arg1))

if __name__ == "__main__":
    main()
import pytest
import os
import shutil
import dataset_manager as dm

# test file for download_blob, download_folder, remove_exif_generator, and remove_exif_folder

# Authentication with key
key_authentication_blob = {"connection_string":"AccountName=296e1f6fa72f4160b2bd3aec;AccountKey=DgqJ7Hv4TBIwx8WKBbChmeq3Cj8iibyEup6Fx4umOc9UuEul2RlncRy4ygUJiN13vuRZkeJGEs3MYlM/jsh7OA==;EndpointSuffix=core.windows.net;DefaultEndpointsProtocol=https;",
                      "container_name":"documentserviceblobstorage",
                      "input_path":""}
correct_key_doc_id_list = ["000001ce-d64d-4ee8-a8db-40ce9a7f7932","00000ab9-d894-496e-aa5d-8891f6bfeab3","63e90dd8-6f78-46a6-9090-1dba1fd262da"]

# test download_blob sas gen and sas file
sas_authentication_blob = {"account_url":"https://droneinspectionsprod.blob.core.windows.net", 
                      "credential":"st=2021-10-01T10%3A49%3A34Z&se=2022-12-31T10%3A49%3A00Z&sp=racwl&sv=2018-03-28&sr=c&sig=H%2FN9nQ9%2Bv8GEP%2F0k1gMdDeS8V1gSVeVLctg3%2BH5tloE%3D",
                      "container_name":"equinor",
                      "input_path":"POC3/EQ21611_stills/20210515_02"
    }
correct_sas_doc_id_list = ["EQ21611_20210515020000327@CAM2.jpg","EQ21611_20210515020000661@CAM2.jpg","EQ21611_20210515020000994@CAM2.jpg"]

# test download_folder key 
key_authentication_folder = {"connection_string":"AccountName=296e1f6fa72f4160b2bd3aec;AccountKey=DgqJ7Hv4TBIwx8WKBbChmeq3Cj8iibyEup6Fx4umOc9UuEul2RlncRy4ygUJiN13vuRZkeJGEs3MYlM/jsh7OA==;EndpointSuffix=core.windows.net;DefaultEndpointsProtocol=https;",
                      "container_name":"documentserviceblobstorage",
                      "input_path":""
                      }
correct_folder_key_list = ["test1"]

# test download_folder sas
sas_authentication_folder = {"account_url":"https://droneinspectionsprod.blob.core.windows.net", 
                      "credential":"st=2021-10-01T10%3A49%3A34Z&se=2022-12-31T10%3A49%3A00Z&sp=racwl&sv=2018-03-28&sr=c&sig=H%2FN9nQ9%2Bv8GEP%2F0k1gMdDeS8V1gSVeVLctg3%2BH5tloE%3D",
                      "container_name":"equinor",
                      "input_path":""
    }
correct_folder_sas_list = ["POC3/EQ21611_stills/20210515_02","POC3/EQ21611_stills/20210515_03"]

missingfield_authentication_folder = {"account_url":"https://droneinspectionsprod.blob.core.windows.net", 
                      "credential":"st=2021-10-01T10%3A49%3A34Z&se=2022-12-31T10%3A49%3A00Z&sp=racwl&sv=2018-03-28&sr=c&sig=H%2FN9nQ9%2Bv8GEP%2F0k1gMdDeS8V1gSVeVLctg3%2BH5tloE%3D",
                      "input_path":""
    }

# test remove_exif_generator and remove_exif_folder
file_list = ["testinput/Fujifilm_FinePix6900ZOOM.jpg","testinput/Kodak_CX7530.jpg"]
folder_path = "./testinput"


# read write test folder
output_path = "./testoutput"
input_path = "./testinput"
file_not_exists = "file_not_exists.csv"

# download_blob for key
key_doc_id_file = "key_doc_id.csv"
key_doc_id_gen = [[f] for f in correct_key_doc_id_list[:2]]
key_authentication_doc_id = {"fields":key_authentication_blob, "type":"key"}

# download_blob for sas
sas_doc_id_file = "sas_doc_id.csv"
sas_doc_id_gen = [[f] for f in correct_sas_doc_id_list[:2]]
sas_authentication_doc_id =  {"fields":sas_authentication_blob, "type":"sas"}

# download_folder for key
key_folder_file = "key_folder.csv"
key_folder_gen = [[folder] for folder in correct_folder_key_list]
key_authentication_folder = {"fields":key_authentication_folder, "type":"key"}

# download_folder for sas 
sas_folder_file = "sas_folder.csv"
sas_folder_gen = [[folder] for folder in correct_folder_sas_list]
sas_authentication_folder = {"fields":sas_authentication_folder, "type":"sas"}

# remove_exif_generator
exif_gen = [[file] for file in file_list]

# # remove_exif_folder 
# exif_folder_gen = [[folder] for folder in folder_list]
# exif_folder_file = "exif_folder.csv"

# authentication problems
wrongtype_full_authentication_folder = {"fields":sas_authentication_folder, "type":"wrongtype"}
missingfield_full_authentication_folder = {"fields":missingfield_authentication_folder, "type":"sas"}

    
@pytest.fixture(scope='function')
def setup_and_teardown(request):
    #setup
    os.mkdir(output_path)

    def teardown():
        shutil.rmtree(output_path)
    request.addfinalizer(teardown)
         
def test_empty_inputs(setup_and_teardown):
    assert dm.download_blob() == 0
    assert dm.download_folder() == 0

def test_empty_authentication(setup_and_teardown):
    assert dm.download_blob(doc_id_file=key_doc_id_file) == 0
    assert dm.download_blob(doc_id_gen=key_doc_id_gen) == 0
    assert dm.download_folder(folder_gen=key_folder_gen) == 0
    assert dm.download_folder(folder_gen=sas_folder_gen)  == 0

# note: test download_folder works, need to define the correct file inside the folders
def test_both_inputs():
    assert dm.download_blob(doc_id_file=key_doc_id_file, 
                                        doc_id_gen=key_doc_id_gen, 
                                        authentication=key_authentication_doc_id,
                                        output_path=output_path) == 2
    
    assert dm.download_blob(doc_id_file=sas_doc_id_file,
                                        doc_id_gen=sas_doc_id_gen,
                                        authentication=sas_authentication_doc_id, 
                                        output_path=output_path) == 2
    
    assert dm.download_folder(folder_file=key_folder_file,
                                        folder_gen=key_folder_gen,
                                        authentication=key_authentication_folder,
                                        output_path=output_path) == 7
    
    assert dm.download_folder(folder_file=sas_folder_file,
                                        folder_gen=sas_folder_gen,
                                        authentication=sas_authentication_folder,
                                        output_path=output_path) == 20

# note: test download_folder works, need to define the correct file inside the folders
def test_file_input(setup_and_teardown):
    assert dm.download_blob(doc_id_file=key_doc_id_file,  
                                        authentication=key_authentication_doc_id,
                                        output_path=output_path) == 2
    
    assert dm.download_blob(doc_id_file=sas_doc_id_file,
                                        authentication=sas_authentication_doc_id, 
                                        output_path=output_path) == 2
    
    assert dm.download_folder(folder_file=key_folder_file,
                                        authentication=key_authentication_folder,
                                        output_path=output_path) == 7
    
    assert dm.download_folder(folder_file=sas_folder_file,
                                        authentication=sas_authentication_folder,
                                        output_path=output_path) == 20

def test_file_not_exists(setup_and_teardown):
    assert dm.download_blob(doc_id_file=file_not_exists,
                                        authentication=key_authentication_doc_id,
                                        output_path=output_path) == 0
    
    assert dm.download_blob(doc_id_file=file_not_exists,
                                        authentication=sas_authentication_doc_id, 
                                        output_path=output_path) == 0
    
    assert dm.download_folder(folder_file=file_not_exists,
                                        authentication=key_authentication_folder,
                                        output_path=output_path) == 0
    
    assert (dm.download_folder(folder_file=file_not_exists,
                                        authentication=sas_authentication_folder,
                                        output_path=output_path),0)
    
def test_wrong_authentication(setup_and_teardown):
    assert dm.download_folder(folder_gen=key_folder_gen,
                                        authentication=missingfield_full_authentication_folder,
                                        output_path=output_path) == 0
    
    assert dm.download_folder(folder_gen=key_folder_gen,
                                        authentication=wrongtype_full_authentication_folder,
                                        output_path=output_path) == 0
    
def test_remove_exif_generator(setup_and_teardown):
    assert dm.remove_exif_generator(image_dir_gen=exif_gen,output_path=output_path) == 2

def test_remove_exif_folder(setup_and_teardown):
    assert dm.remove_exif_folder(folder_path=folder_path, 
                                            output_path=output_path) == 2
    
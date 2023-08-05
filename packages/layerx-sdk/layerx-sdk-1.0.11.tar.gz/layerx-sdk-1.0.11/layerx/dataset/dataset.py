from typing import TYPE_CHECKING
from .logger import get_debug_logger

if TYPE_CHECKING:
    from . import DatasetClient



annotation_logger = get_debug_logger('Dataset')


class Dataset:
    def __init__(self, client: "DatasetClient"):
        self._client = client


    """
    create dataset from search objects
    """
    def create_dataset(self, dataset_name, selection_id, split_info, labels, export_types):
        if(dataset_name == "" or dataset_name == None):
            return {
                "isSuccess": False,
                "message": "dataset name not valid"
            }
        if(selection_id == "" or selection_id == None):
            return {
                "isSuccess": False,
                "message": "selection_id not valid"
            }
        if ("train" not in split_info) or ("test" not in split_info) or ("validation" not in split_info):
            return {
                "isSuccess": False,
                "message": "split info not valid"
            }

        split_info = {
            "train": split_info["train"],
            "test": split_info["test"],
            "validation": split_info["validation"]
        }
        payload_dataset_creation = {
            "name": dataset_name,
            "splitInfo": split_info,
            "labels": labels,
            "exportTypes": export_types
        }

        response = self._client.dataset_interface.create_dataset(selection_id, payload_dataset_creation)
        
        return response


    """
    update dataset from search objects
    """
    def update_dataset_version(self, version_id, selection_id, splitInfo, labels, export_types, is_new_version_requried):
        if(version_id == "" or version_id == None):
            return {
                "isSuccess": False,
                "message": "dataset name not valid"
            }
        if(selection_id == "" or selection_id == None):
            return {
                "isSuccess": False,
                "message": "selection_id not valid"
            }
        if ("train" not in splitInfo) or ("test" not in splitInfo) or ("validation" not in splitInfo):
            return {
                "isSuccess": False,
                "message": "split info not valid"
            }

        split_info = {
            "train": splitInfo["train"],
            "test": splitInfo["test"],
            "validation": splitInfo["validation"]
        }
        payload_dataset_update = {
            "splitInfo": split_info,
            "labels": labels,
            "exportTypes": export_types
        }
        if(is_new_version_requried == False):
            response = self._client.dataset_interface.update_existing_dataset_version(selection_id, payload_dataset_update, version_id)
        else:
            response = self._client.dataset_interface.create_new_dataset_version(selection_id, payload_dataset_update, version_id)
        return response


    
    """
    delete dataset version
    """
    def delete_dataset_version(self, version_id):
        response = self._client.dataset_interface.delete_dataset_version(version_id)
        
        return response
    
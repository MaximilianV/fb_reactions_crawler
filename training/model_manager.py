import hashlib
import time
import json
from training.models import Models
from training.feature.features import Features


class ModelManager:
    def __init__(self, base_path="data/models/"):
        self.base_path = base_path
        if not self.base_path.endswith("/"):
            self.base_path += "/"
        print("Started new model manager.")

    def save(self, model, descriptive_name=True, name_appendix=None):
        model_config = dict()
        model_config["base_path"] = self.base_path
        model_config["model_type"] = model.__class__.__name__
        if descriptive_name:
            model_id = ModelManager.truncate_model_name(model.__class__.__name__)
            for feature in model.feature_union.transformer_list:
                print(feature)
                model_id += "_" + ModelManager.truncate_feature_name(feature[0])
            if name_appendix:
                model_id += "__" + name_appendix
        else:
            hasher = hashlib.md5()
            hasher.update(model_config["model_type"].encode('utf-8'))
            hasher.update(str(time.time()).encode('utf-8'))
            model_id = hasher.hexdigest()
        model_config["id"] = model_id

        # Save model
        model.persist(self.base_path + str(model_id))

        with open(self.base_path + str(model_id) + '.model.json', 'w') as outfile:
            json.dump(model_config, outfile)

        return model_id

    @staticmethod
    def load(config_path):
        with open(config_path, 'r') as outfile:
            model_config = json.load(outfile)

        model_id = model_config["id"]
        base_path = model_config["base_path"]

        # Load model
        model = Models[model_config["model_type"]].value(base_path + str(model_id))

        return model

    @staticmethod
    def truncate_model_name(model_name):
        return model_name.replace("Model", "")

    @staticmethod
    def truncate_feature_name(feature_name):
        return feature_name.replace("Feature", "").replace("Vectorizer", "")

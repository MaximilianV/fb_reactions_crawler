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

    def save(self, model):
        model_config = dict()
        model_config["name"] = model.get_name()
        model_config["base_path"] = self.base_path
        hasher = hashlib.md5()
        hasher.update(model_config["name"].encode('utf-8'))
        hasher.update(str(time.time()).encode('utf-8'))
        model_id = hasher.hexdigest()
        model_config["id"] = model_id

        # Save model
        model_config["model_type"] = model.__class__.__name__
        model.persist(self.base_path + str(model_id) + ".model")

        # Save features
        model_config["features"] = []
        feature_count = 0
        for feature in model.feature_objects:
            feature_config = dict()
            feature_config["id"] = feature_count
            feature_config["type"] = feature.__class__.__name__
            model_config["features"].append(feature_config)
            feature.persist(self.base_path + str(model_id) + "." + str(feature_count) + ".feature")
            feature_count += 1

        with open(self.base_path + str(model_id) + '.model.json', 'w') as outfile:
            json.dump(model_config, outfile)

    @staticmethod
    def load(config_path):
        with open(config_path, 'r') as outfile:
            model_config = json.load(outfile)

        model_id = model_config["id"]
        base_path = model_config["base_path"]

        # Load model
        model = Models[model_config["model_type"]].value(base_path + str(model_id) + ".model")

        # Load features
        for feature in model_config["features"]:
            feature_object = Features[feature["type"]].value(base_path + str(model_id) + "." + str(feature["id"]) + ".feature")
            model.feature_objects.append(feature_object)

        return model

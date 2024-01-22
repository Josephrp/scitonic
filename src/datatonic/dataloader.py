# src/datatonic/dataloader.py

from datasets import load_dataset
import json

class DataLoader:
    def __init__(self):
        self.datasets = {
            "gpl-fiqa": self.load_gpl_fiqa,
            "msmarco": self.load_msmarco,
            "nfcorpus": self.load_nfcorpus,
            "covid19": self.load_covid19,
            "gpl-webis-touche2020": self.load_gpl_webis_touche2020,
            "gpl-hotpotqa": self.load_gpl_hotpotqa,
            "gpl-nq": self.load_gpl_nq,
            "gpl-fever": self.load_gpl_fever,
            "gpl-scidocs": self.load_gpl_scidocs,
            "gpl-scifact": self.load_gpl_scifact,
            "gpl-cqadupstack": self.load_gpl_cqadupstack,
            "gpl-arguana": self.load_gpl_arguana,
            "gpl-climate-fever": self.load_gpl_climate_fever,
            "gpl-dbpedia-entity": self.load_gpl_dbpedia_entity,
            "gpl-all-mix-450k": self.load_gpl_all_mix_450k,
        }

    def load_dataset_generic(self, dataset_name):
        dataset = load_dataset(dataset_name)
        return self.process_dataset(dataset)

    def load_gpl_fiqa(self):
        return self.load_dataset_generic("nthakur/gpl-fiqa")

    def load_msmarco(self):
        return self.load_dataset_generic("nthakur/msmarco-passage-sampled-100k")

    def load_nfcorpus(self):
        return self.load_dataset_generic("nthakur/gpl-nfcorpus")

    def load_covid19(self):
        return self.load_dataset_generic("nthakur/gpl-trec-covid")

    def load_gpl_webis_touche2020(self):
        return self.load_dataset_generic("nthakur/gpl-webis-touche2020")

    def load_gpl_hotpotqa(self):
        return self.load_dataset_generic("nthakur/gpl-hotpotqa")

    def load_gpl_nq(self):
        return self.load_dataset_generic("nthakur/gpl-nq")

    def load_gpl_fever(self):
        return self.load_dataset_generic("nthakur/gpl-fever")

    def load_gpl_scidocs(self):
        return self.load_dataset_generic("nthakur/gpl-scidocs")

    def load_gpl_scifact(self):
        return self.load_dataset_generic("nthakur/gpl-scifact")

    def load_gpl_cqadupstack(self):
        return self.load_dataset_generic("nthakur/gpl-cqadupstack")

    def load_gpl_arguana(self):
        return self.load_dataset_generic("nthakur/gpl-arguana")

    def load_gpl_climate_fever(self):
        return self.load_dataset_generic("nthakur/gpl-climate-fever")

    def load_gpl_dbpedia_entity(self):
        return self.load_dataset_generic("nthakur/gpl-dbpedia-entity")

    def load_gpl_all_mix_450k(self):
        return self.load_dataset_generic("nthakur/gpl-all-mix-450k")

    def process_dataset(self, dataset):
        # Process the dataset to fit the required JSON structure
        processed_data = []
        for entry in dataset['train']:
            # Adjust the processing based on the actual structure of each dataset
            processed_entry = {
                "query": entry.get("query", ""),
                "positive_passages": entry.get("positive_passages", []),
                "negative_passages": entry.get("negative_passages", [])
            }
            processed_data.append(processed_entry)
        return processed_data

    def load_and_process(self, dataset_name):
        if dataset_name in self.datasets:
            return self.datasets[dataset_name]()
        else:
            # Log or return an error message and default to "gpl-arguana"
            error_message = f"Dataset '{dataset_name}' not supported. Defaulting to 'gpl-arguana'."
            print(error_message)  # or handle this message as needed
            return self.load_gpl_arguana()  # Default to the 'gpl-arguana' dataset

    def save_to_json(self, data, file_name):
        with open(file_name, 'w') as f:
            json.dump(data, f, indent=4)
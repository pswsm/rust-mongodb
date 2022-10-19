# Loading script for the TeCla dataset.
import json
import datasets

logger = datasets.logging.get_logger(__name__)

_CITATION = """
               Carrino, Casimiro Pio, Rodriguez-Penagos, Carlos Gerardo, & Armentano-Oller, Carme. (2021). 
               TeCla: Text Classification Catalan dataset (Version 1.0) [Data set]. 
               Zenodo. http://doi.org/10.5281/zenodo.4627198
            """

_DESCRIPTION = """
                   TeCla: Text Classification Catalan dataset
                   Catalan News corpus for Text classification, crawled from ACN (Catalan News Agency) site: www.acn.cat
                   Corpus de notícies en català per a classificació textual, extret del web de l'Agència Catalana de Notícies - www.acn.cat
               """

_HOMEPAGE = """https://zenodo.org/record/4761505"""

# TODO: upload datasets to github
_URL = "./"
_TEST_FILE = "test.json"


class teclaConfig(datasets.BuilderConfig):
    """ Builder config for the TeCla dataset """

    def __init__(self, **kwargs):
        """BuilderConfig for TeCla.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(teclaConfig, self).__init__(**kwargs)


class tecla(datasets.GeneratorBasedBuilder):
    """ TeCla Dataset """

    BUILDER_CONFIGS = [
        teclaConfig(
            name="tecla",
            version=datasets.Version("1.0.1"),
            description="tecla dataset",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    "label": datasets.features.ClassLabel
                        (names=
                    [
                        "Medi ambient",
                        "Societat",
                        "Policial",
                        "Judicial",
                        "Empresa",
                        "Partits",
                        "Pol\u00edtica",
                        "Successos",
                        "Salut",
                        "Infraestructures",
                        "Parlament",
                        "M\u00fasica",
                        "Govern",
                        "Uni\u00f3 Europea",
                        "Economia",
                        "Mobilitat",
                        "Treball",
                        "Cultura",
                        "Educaci\u00f3"
                    ]
                    ),
                }
            ),
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
            "test": f"{_URL}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logger.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            acn_ca = json.load(f)
            for id_, article in enumerate(acn_ca["data"]):
                text = article["sentence"]
                label = article["label"]
                yield id_, {
                    "text": text,
                    "label": label,
                }

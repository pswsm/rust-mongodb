# Loading script for the Ancora NER dataset. 
import datasets

logger = datasets.logging.get_logger(__name__)

_CITATION = """ """

_DESCRIPTION = """AnCora Catalan NER.
                  This is a dataset for Named Eentity Reacognition (NER) from Ancora corpus adapted for 
                  Machine Learning and Language Model evaluation purposes.
                  Since multiwords (including Named Entites) in the original Ancora corpus are aggregated as 
                  a single lexical item using underscores (e.g. "Ajuntament_de_Barcelona") 
                  we splitted them to align with word-per-line format, and added conventional Begin-Inside-Outside (IOB)
                   tags to mark and classify Named Entites. 
                   We did not filter out the different categories of NEs from Ancora (weak and strong). 
                   We did 6 minor edits by hand.
                  AnCora corpus is used under [CC-by] (https://creativecommons.org/licenses/by/4.0/) licence.
                  This dataset was developed by BSC TeMU as part of the AINA project, and to enrich the Catalan Language Understanding Benchmark (CLUB).
               """

_HOMEPAGE = """https://zenodo.org/record/4762031"""

_URL = "./"
# _TRAINING_FILE = "train.conll"
# _DEV_FILE = "dev.conll"
_TEST_FILE = "test.conll"


class AncoraCaNerConfig(datasets.BuilderConfig):
    """ Builder config for the Ancora Ca NER dataset """

    def __init__(self, **kwargs):
        """BuilderConfig for AncoraCaNer.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(AncoraCaNerConfig, self).__init__(**kwargs)


class AncoraCaNer(datasets.GeneratorBasedBuilder):
    """ AncoraCaNer dataset."""

    BUILDER_CONFIGS = [
        AncoraCaNerConfig(
            name="AncoraCaNer",
            version=datasets.Version("2.0.0"),
            description="AncoraCaNer dataset"
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "tokens": datasets.Sequence(datasets.Value("string")),
                    "ner_tags": datasets.Sequence(
                        datasets.features.ClassLabel(
                            names=[
                                "B-LOC",
                                "B-MISC",
                                "B-ORG",
                                "B-PER",
                                "I-LOC",
                                "I-MISC",
                                "I-ORG",
                                "I-PER",
                                "O"
                            ]
                        )
                    ),
                }
            ),
            supervised_keys=None,
            homepage=_HOMEPAGE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        urls_to_download = {
#             "train": f"{_URL}{_TRAINING_FILE}",
#             "dev": f"{_URL}{_DEV_FILE}",
            "test": f"{_URL}{_TEST_FILE}",
        }
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
#             datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
#             datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            guid = 0
            tokens = []
            ner_tags = []
            for line in f:
                if line.startswith("-DOCSTART-") or line == "" or line == "\n":
                    if tokens:
                        yield guid, {
                            "id": str(guid),
                            "tokens": tokens,
                            "ner_tags": ner_tags,
                        }
                        guid += 1
                        tokens = []
                        ner_tags = []
                else:
                    # AncoraCaNer tokens are space separated
                    splits = line.split('\t')
                    tokens.append(splits[0])
                    ner_tags.append(splits[1].rstrip())
            # last example
            yield guid, {
                "id": str(guid),
                "tokens": tokens,
                "ner_tags": ner_tags,
            }

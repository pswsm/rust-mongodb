# Loading script for the Semantic Textual Similarity Ca dataset.
import datasets

logger = datasets.logging.get_logger(__name__)

_CITATION = """
               Rodriguez-Penagos, Carlos Gerardo, Armentano-Oller, Carme, Gonzalez-Agirre, Aitor, & Gibert Bonet, Ona. (2021). 
               Semantic Textual Similarity in Catalan (Version 1.0.1) [Data set]. 
               Zenodo. http://doi.org/10.5281/zenodo.4761434
            """

_DESCRIPTION = """
                  Semantic Textual Similarity in Catalan.
                  STS corpus is a benchmark for evaluating Semantic Text Similarity in Catalan.
                  It consists of more than 3000 sentence pairs, annotated with the semantic similarity between them, 
                  using a scale from 0 (no similarity at all) to 5 (semantic equivalence). 
                  It is done manually by 4 different annotators following our guidelines based on previous work from the SemEval challenges (https://www.aclweb.org/anthology/S13-1004.pdf).
                  The source data are scraped sentences from the Catalan Textual Corpus (https://doi.org/10.5281/zenodo.4519349), used under CC-by-SA-4.0 licence (https://creativecommons.org/licenses/by-sa/4.0/). The dataset is released under the same licence.
                  This dataset was developed by BSC TeMU as part of the AINA project, and to enrich the Catalan Language Understanding Benchmark (CLUB).
                  This is the version 1.0.2 of the dataset with the complete human and automatic annotations and the analysis scripts. It also has a more accurate license.
                  This dataset can be used to build and score semantic similiarity models.
               """

_HOMEPAGE = """https://zenodo.org/record/4761434"""

# TODO: upload datasets to github
_URL = "./"
_TEST_FILE = "test.tsv"


class StsCaConfig(datasets.BuilderConfig):
    """ Builder config for the Semantic Textual Similarity Ca dataset """

    def __init__(self, **kwargs):
        """BuilderConfig for StsCa.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(StsCaConfig, self).__init__(**kwargs)


class StsCa(datasets.GeneratorBasedBuilder):
    """Semantic Textual Similarity Ca dataset."""

    BUILDER_CONFIGS = [
        StsCaConfig(
            name="StsCa",
            version=datasets.Version("1.0.2"),
            description="Semantic Textual Similarity in catalan dataset"
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "sentence1": datasets.Value("string"),
                    "sentence2": datasets.Value("string"),
                    "label": datasets.Value("float"),
                }
            ),
            supervised_keys=None,
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
        """ Returns the examples in the raw text form """
        logger.info("⏳ Generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            for id_, row in enumerate(f):
                ref, sentence1, sentence2, score = row.split('\t')
                yield id_, {
                    "sentence1": sentence1,
                    "sentence2": sentence2,
                    "label": score,
                }

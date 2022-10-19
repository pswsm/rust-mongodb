# Loading script for the XQuAD-ca dataset.
import json
import datasets

logger = datasets.logging.get_logger(__name__)

_CITATION = """
               Carlos Gerardo Rodriguez-Penagos, & Carme Armentano-Oller. (2021). XQuAD-ca [Data set].
                Zenodo. http://doi.org/10.5281/zenodo.4757559
            """

_DESCRIPTION = """
                  Professional translation into Catalan of XQuAD dataset (https://github.com/deepmind/xquad).
                  XQuAD (Cross-lingual Question Answering Dataset) is a benchmark dataset for evaluating 
                  cross-lingual question answering performance. 
                  The dataset consists of a subset of 240 paragraphs and 1190 question-answer pairs from 
                  the development set of SQuAD v1.1 (Rajpurkar et al., 2016) together with 
                  their professional translations into ten languages: 
                  Spanish, German, Greek, Russian, Turkish, Arabic, Vietnamese, Thai, Chinese, and Hindi. 
                  Rumanian was added later.
                  We added the 13th language to the corpus using also professional native catalan translators.
                  XQuAD and XQuAD-Ca datasets are released under CC-by-sa licence.
               """

_HOMEPAGE = """https://zenodo.org/record/4757559"""

_URL = "./"
_TEST_FILE = "test.json"


class XQuADcaConfig(datasets.BuilderConfig):
    """ Builder config for the XQuAD-ca dataset """

    def __init__(self, **kwargs):
        """BuilderConfig for XQuAD-ca.
        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(XQuADcaConfig, self).__init__(**kwargs)


class XQuADca(datasets.GeneratorBasedBuilder):
    """XQuAD-ca Dataset."""

    BUILDER_CONFIGS = [
        XQuADcaConfig(
            name="XQuAD-ca",
            version=datasets.Version("2.0.0"),
            description="XQuAD-ca dataset",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers":  datasets.features.Sequence(

                        {

                            "text": datasets.Value("string"),

                            "answer_start": datasets.Value("int32"),

                        }

                    ),
                }
            ),
            # No default supervised_keys (as we have to pass both question
            # and context as input).
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
        """This function returns the examples in the raw (text) form."""
        logger.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            xquad = json.load(f)
            for article in xquad["data"]:
                title = article.get("title", "").strip()
                for paragraph in article["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        id_ = qa["id"]
                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]
#                         text = qa["answers"][0]["text"]
#                         answer_start = qa["answers"][0]["answer_start"]

                        # Features currently used are "context", "question", and "answers".
                        # Others are extracted here for the ease of future expansions.
                        yield id_, {
                            "title": title,
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {"text": answers, "answer_start": answer_starts}
                        }

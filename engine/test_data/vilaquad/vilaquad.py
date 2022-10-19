"""ViquiQuAD Dataset."""
# Loading script for the ViquiQuAD dataset.
import json
import os
import datasets

logger = datasets.logging.get_logger(__name__)

_CITATION = """\
Rodriguez-Penagos, Carlos Gerardo, & Armentano-Oller, Carme. (2021).
VilaQuAD: an extractive QA dataset for catalan, from Vilaweb newswire text
[Data set]. Zenodo. https://doi.org/10.5281/zenodo.4562337
"""

_DESCRIPTION = """\
This dataset contains 2095 of Catalan language news articles along with 1 to 5 questions referring to each fragment (or context).

VilaQuad articles are extracted from the daily Vilaweb (www.vilaweb.cat) and used under CC-by-nc-sa-nd (https://creativecommons.org/licenses/by-nc-nd/3.0/deed.ca) licence. 

This dataset can be used to build extractive-QA and Language Models.

Funded by the Generalitat de Catalunya, Departament de Polítiques Digitals i Administració Pública (AINA),

MT4ALL and Plan de Impulso de las Tecnologías del Lenguaje (Plan TL).
"""

_HOMEPAGE = "https://doi.org/10.5281/zenodo.4562337"

_URL = "./"
_TEST_FILE = "test.json"


class VilaQuAD(datasets.GeneratorBasedBuilder):
    """VilaQuAD Dataset."""

    VERSION = datasets.Version("1.0.1")

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": 
                        {
                            "text": datasets.Sequence(datasets.Value("string")),
                            "answer_start": datasets.Sequence(datasets.Value("int32")),
                        }
                    ,
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
            "test": f"{os.path.join(_URL,_TEST_FILE)}",
        }
        downloaded_files = dl_manager.download(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        logger.info("generating examples from = %s", filepath)
        with open(filepath, encoding="utf-8") as f:
            vilaquad = json.load(f)
            id_ = 0
            for article in vilaquad["data"]:
                title = article.get("title", "").strip()
                for paragraph in article["paragraphs"]:
                    context = paragraph["context"].strip()
                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()
                        qid = qa["id"]
                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        # Features currently used are "context", "question", and "answers".
                        # Others are extracted here for the ease of future expansions.
                        yield id_, {
                            "title": title,
                            "context": context,
                            "question": question,
                            "id": qid,
                            "answers": {"text": answers, "answer_start": answer_starts},
                        }
                        id_ += 1

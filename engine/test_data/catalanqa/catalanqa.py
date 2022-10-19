"""ViquiQuAD Dataset."""
# Loading script for the ViquiQuAD dataset.
import json
import os
import datasets

logger = datasets.logging.get_logger(__name__)

_CITATION = """\
None 
"""

_DESCRIPTION = """\
CatalanQA: an extractive QA dataset from Catalan Sources: Wikipedia, VilaWeb, XQUAD.
 It is an aggregation and balancing of 3 previous datasets: VilaQUAD, ViquiQUAD and XQUAD_ca
This dataset can be used to build extractive-QA and Language Models.
Funded by the Generalitat de Catalunya, Departament de Polítiques Digitals i Administració Pública (AINA),
MT4ALL and Plan de Impulso de las Tecnologías del Lenguaje (Plan TL).
"""

_HOMEPAGE = ""#"https://zenodo.org/record/4562345#.YK41aqGxWUk"

_URL = "./"
_TEST_FILE = "test.json"


class CatalanQA(datasets.GeneratorBasedBuilder):
    """CatalanQA Dataset."""

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
            catalanqa = json.load(f)
            id_ = 0
            for article in catalanqa["data"]:
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

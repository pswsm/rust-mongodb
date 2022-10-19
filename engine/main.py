import argparse
import json
from datasets import load_dataset, load_metric
# from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, classification_report
from seqeval.metrics import f1_score
import numpy as np
from scipy.stats import pearsonr, spearmanr
import string
import re
import collections
import warnings
warnings.filterwarnings("ignore")
# from sklearn.preprocessing import MultiLabelBinarizer

def pearson_and_spearman(preds, labels):
    pearson_corr = pearsonr(preds, labels)[0]
    spearman_corr = spearmanr(preds, labels)[0]
    return {
        "pearson": pearson_corr,
        "spearmanr": spearman_corr,
    }

def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""

    def remove_articles(text):
        regex = re.compile(r"\b(a|an|the)\b", re.UNICODE)
        return re.sub(regex, " ", text)

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))

def compute_exact(a_gold, a_pred):
    return int(normalize_answer(a_gold) == normalize_answer(a_pred))

def get_tokens(s):
    if not s:
        return []
    return normalize_answer(s).split()

def compute_f1(a_gold, a_pred):
    gold_toks = get_tokens(a_gold)
    pred_toks = get_tokens(a_pred)
    common = collections.Counter(gold_toks) & collections.Counter(pred_toks)
    num_same = sum(common.values())
    if len(gold_toks) == 0 or len(pred_toks) == 0:
        # If either is no-answer, then F1 is 1 if they agree, 0 otherwise
        return int(gold_toks == pred_toks)
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(pred_toks)
    recall = 1.0 * num_same / len(gold_toks)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1

def make_eval_dict(exact_scores, f1_scores, qid_list=None):
    if not qid_list:
        total = len(exact_scores)
        return collections.OrderedDict(
            [
                ("exact", 100.0 * sum(exact_scores.values()) / total),
                ("f1", 100.0 * sum(f1_scores.values()) / total),
                ("total", total),
            ]
        )
    else:
        total = len(qid_list)
        return collections.OrderedDict(
            [
                ("exact", 100.0 * sum(exact_scores[k] for k in qid_list) / total),
                ("f1", 100.0 * sum(f1_scores[k] for k in qid_list) / total),
                ("total", total),
            ]
        )


def merge_eval(main_eval, new_eval, prefix):
    for k in new_eval:
        main_eval["%s_%s" % (prefix, k)] = new_eval[k]


def compute_metrics_AnCora_ca(predictions_file, test_data_loader="engine/test_data/ancora-ca-ner/ancora-ca-ner.py"):
    # Load gs data
    test_dataset = load_dataset(test_data_loader)

    # get the true labels
    y_true = []
    label_list = test_dataset["test"].features["ner_tags"].feature.names
    for example in test_dataset["test"]:
        label = [label_list[tag] for tag in example["ner_tags"]]
        y_true.append(label)

    # get the true predictions
    with open(predictions_file) as f:
        y_pred = [x[:-1].strip().split(" ") if x[:-1] != "" else [] for x in f.readlines()]

    return {"F1": 100 * f1_score(y_true, y_pred, average='weighted')}

#     for idx, pred in enumerate(y_pred):
#         for label in pred:
#             if label == "":
#                 print(idx, pred)

#     y_true = sum(y_true, [])
#     y_pred = sum(y_pred, [])
    # binarize the results
#     mlb_true = MultiLabelBinarizer()
#     y_true = mlb_true.fit_transform(y_true)
#     mlb_pred = MultiLabelBinarizer()
#     y_pred = mlb_pred.fit_transform(y_pred)
#     print(mlb_true.classes_)
#     print(mlb_pred.classes_)






#     results = metric.compute(predictions=true_predictions, references=true_labels)
#     if data_args.return_entity_level_metrics:
#         # Unpack nested dictionaries
#         final_results = {}
#         for key, value in results.items():
#             if isinstance(value, dict):
#                 for n, v in value.items():
#                     final_results[f"{key}_{n}"] = v
#             else:
#                 final_results[key] = value
#         return final_results
#     else:
#     results = {}
#     results["overall_precision"] = precision_score(y_true, y_pred, average='weighted')
#     results["overall_recall"] = recall_score(y_true, y_pred, average='weighted')
#     results["overall_f1"] = f1_score(y_true, y_pred, average='weighted')
#     results["overall_accuracy"] = accuracy_score(y_true, y_pred)
#     return {
#         "precision": results["overall_precision"],
#         "recall": results["overall_recall"],
#         "f1": results["overall_f1"],
#         "accuracy": results["overall_accuracy"],
#     }

def compute_metrics_TECa(predictions_file, test_data_loader="engine/test_data/teca/teca.py"):
    # Load gs data
    test_dataset = load_dataset(test_data_loader)

    # get the true labels
    y_true = []
    label_list = test_dataset["test"].features["label"].names
    for example in test_dataset["test"]:
        label = label_list[example["label"]]
        y_true.append(label)

    # get the true predictions
    with open(predictions_file) as f:
        lines = f.readlines()[1:]
        y_pred = [x[:-1].strip().split("\t")[-1] if x[:-1] != "" else [] for x in lines]

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    return {"Accuracy": 100 * (y_pred == y_true).mean()}

def compute_metrics_TeCla(predictions_file, test_data_loader="engine/test_data/tecla/tecla.py"):
    # Load gs data
    test_dataset = load_dataset(test_data_loader)

    # get the true labels
    y_true = []
    label_list = test_dataset["test"].features["label"].names
    for example in test_dataset["test"]:
        label = label_list[example["label"]]
        y_true.append(label)

    # get the true predictions
    with open(predictions_file) as f:
        lines = f.readlines()[1:]
        y_pred = [x[:-1].strip().split("\t")[-1] if x[:-1] != "" else [] for x in lines]

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    return {"Accuracy": 100 * (y_pred == y_true).mean()}

def compute_metrics_XQuAD_Ca(predictions_file, test_data_loader="engine/test_data/xquad-ca/xquad-ca.py"):
    # Load gs data
    test_dataset = load_dataset(test_data_loader)

    # load predictions
    with open(predictions_file) as f:
        prediction_json = json.load(f)

    # calculate raw scores
    exact_scores = {}
    f1_scores = {}
    for example in test_dataset["test"]:
        qid = example['id']
        gold_answers = [t for t in example["answers"]["text"] if normalize_answer(t)]
        if not gold_answers:
            # For unanswerable questions, only correct answer is empty string
            gold_answers = [""]
        a_pred = prediction_json[qid]
        exact_scores[qid] = max(compute_exact(a_gold, a_pred) for a_gold in gold_answers)
        f1_scores[qid] = max(compute_f1(a_gold, a_pred) for a_gold in gold_answers)

    out_eval = make_eval_dict(exact_scores, f1_scores)
    return dict(out_eval)


# def compute_metrics_ViquiQuAD(predictions_file, test_data_loader="engine/test_data/viquiquad/viquiquad.py"):
#     # Load gs data
#     test_dataset = load_dataset(test_data_loader)
# 
#     # load predictions
#     with open(predictions_file) as f:
#         prediction_json = json.load(f)
# 
#     # calculate raw scores
#     exact_scores = {}
#     f1_scores = {}
#     for example in test_dataset["test"]:
#         qid = example['id']
#         gold_answers = [t for t in example["answers"]["text"] if normalize_answer(t)]
#         if not gold_answers:
#             # For unanswerable questions, only correct answer is empty string
#             gold_answers = [""]
#         a_pred = prediction_json[qid]
#         exact_scores[qid] = max(compute_exact(a_gold, a_pred) for a_gold in gold_answers)
#         f1_scores[qid] = max(compute_f1(a_gold, a_pred) for a_gold in gold_answers)
# 
#     out_eval = make_eval_dict(exact_scores, f1_scores)
#     return dict(out_eval)
# 
# def compute_metrics_VilaQuAD(predictions_file, test_data_loader="engine/test_data/vilaquad/vilaquad.py"):
#     # Load gs data
#     test_dataset = load_dataset(test_data_loader)
# 
#     # load predictions
#     with open(predictions_file) as f:
#         prediction_json = json.load(f)
# 
#     # calculate raw scores
#     exact_scores = {}
#     f1_scores = {}
#     for example in test_dataset["test"]:
#         qid = example['id']
#         gold_answers = [t for t in example["answers"]["text"] if normalize_answer(t)]
#         if not gold_answers:
#             # For unanswerable questions, only correct answer is empty string
#             gold_answers = [""]
#         a_pred = prediction_json[qid]
#         exact_scores[qid] = max(compute_exact(a_gold, a_pred) for a_gold in gold_answers)
#         f1_scores[qid] = max(compute_f1(a_gold, a_pred) for a_gold in gold_answers)
# 
#     out_eval = make_eval_dict(exact_scores, f1_scores)
#     return dict(out_eval)

def compute_metrics_CatalanQA(predictions_file, test_data_loader="engine/test_data/catalanqa/catalanqa.py"):
    # Load gs data
    test_dataset = load_dataset(test_data_loader)

    # load predictions
    with open(predictions_file) as f:
        prediction_json = json.load(f)

    # calculate raw scores
    exact_scores = {}
    f1_scores = {}
    for example in test_dataset["test"]:
        qid = example['id']
        gold_answers = [t for t in example["answers"]["text"] if normalize_answer(t)]
        if not gold_answers:
            # For unanswerable questions, only correct answer is empty string
            gold_answers = [""]
        a_pred = prediction_json[qid]
        exact_scores[qid] = max(compute_exact(a_gold, a_pred) for a_gold in gold_answers)
        f1_scores[qid] = max(compute_f1(a_gold, a_pred) for a_gold in gold_answers)

    out_eval = make_eval_dict(exact_scores, f1_scores)
    return dict(out_eval)

def compute_metrics_POS(predictions_file, test_data_loader="engine/test_data/pos/universal-dependencies-ca.py"):
    # Load gs data
    test_dataset = load_dataset(test_data_loader)

    # get the true labels
    y_true = []
    label_list = test_dataset["test"].features["upos_tags"].feature.names
    for example in test_dataset["test"]:
        label = [label_list[tag] for tag in example["upos_tags"]]
        y_true.append(label)

    # get the true predictions
    with open(predictions_file) as f:
        y_pred = [x[:-1].strip().split(" ") if x[:-1] != "" else [] for x in f.readlines()]

    return {"F1": 100 * f1_score(y_true, y_pred, average='weighted')}

def compute_metrics_STS_ca(predictions_file, test_data_loader="engine/test_data/sts-ca/sts-ca.py"):
    # Load gs data
    test_dataset = load_dataset(test_data_loader)

    # get the true labels
    y_true = []
    for example in test_dataset["test"]:
        label = example["label"]
        y_true.append(label)

    # get the true predictions
    with open(predictions_file) as f:
        lines = f.readlines()[1:]
        y_pred = [float(x[:-1].strip().split("\t")[-1]) for x in lines]

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    results = pearson_and_spearman(y_true, y_pred)

    return {"combined_score": 100 * np.mean(list(results.values())).item()}


# def evaluate(STS_ca, POS, VilaQuAD, ViquiQuAD, XQuAD_Ca, TeCla, TECa, AnCora_ca):
def evaluate(STS_ca, POS, CatalanQA, XQuAD_Ca, TeCla, TECa, AnCora_ca):
    """(Placeholder) Evaluates the tests"""
    AnCora_ca_results = compute_metrics_AnCora_ca(AnCora_ca)
    TECa_results = compute_metrics_TECa(TECa)
    TeCla_results = compute_metrics_TeCla(TeCla)
    XQuAD_Ca_results = compute_metrics_XQuAD_Ca(XQuAD_Ca)
    CatalanQA_results = compute_metrics_CatalanQA(CatalanQA)
#     ViquiQuAD_results = compute_metrics_ViquiQuAD(ViquiQuAD)
#     VilaQuAD_results = compute_metrics_VilaQuAD(VilaQuAD)
    POS_results = compute_metrics_POS(POS)
    STS_ca_results = compute_metrics_STS_ca(STS_ca)

    suma =  AnCora_ca_results["F1"] + \
            TECa_results["Accuracy"] + \
            TeCla_results["Accuracy"] + \
            XQuAD_Ca_results["exact"] + XQuAD_Ca_results["f1"] + \
            CatalanQA_results["exact"] + CatalanQA_results["f1"] + \
            POS_results["F1"] + \
            STS_ca_results["combined_score"]

#             ViquiQuAD_results["exact"] + ViquiQuAD_results["f1"] + \
#             VilaQuAD_results["exact"] + VilaQuAD_results["f1"] + \

#     print(json.dumps({'STS_ca': STS_ca_results, 'POS': POS_results, 'VilaQuAD': VilaQuAD_results, 'ViquiQuAD': ViquiQuAD_results, 'XQuAD_Ca': XQuAD_Ca_results, 'TeCla': TeCla_results, 'TECa': TECa_results, 'AnCora_ca': AnCora_ca_results, 'sum': suma}))
    print(json.dumps({'STS_ca': STS_ca_results, 'POS': POS_results, 'CatalanQA_results': CatalanQA_results, 'XQuAD_Ca': XQuAD_Ca_results, 'TeCla': TeCla_results, 'TECa': TECa_results, 'AnCora_ca': AnCora_ca_results, 'sum': suma}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('STS_ca', type=str)
    parser.add_argument('POS', type=str)
    parser.add_argument('CatalanQA', type=str)
#     parser.add_argument('VilaQuAD', type=str)
#     parser.add_argument('ViquiQuAD', type=str)
    parser.add_argument('XQuAD_Ca', type=str)
    parser.add_argument('TeCla', type=str)
    parser.add_argument('TECa', type=str)
    parser.add_argument('AnCora_ca', type=str)
    args = parser.parse_args()
#     evaluate(args.STS_ca, args.POS, args.VilaQuAD, args.ViquiQuAD, args.XQuAD_Ca, args.TeCla, args.TECa, args.AnCora_ca)
    evaluate(args.STS_ca, args.POS, args.CatalanQA, args.XQuAD_Ca, args.TeCla, args.TECa, args.AnCora_ca)

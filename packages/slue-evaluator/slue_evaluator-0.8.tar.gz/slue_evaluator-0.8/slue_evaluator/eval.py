#@title Eval Code
"""
Evaluate the output of wav2vec finetuned on NER using CTC loss
"""

#import fire
import numpy as np
import os
import sys
import importlib

sys.path.insert(0, "../")

import slue_evaluator.slue_toolkit_eval_utils as eval_utils
from slue_evaluator.slue_toolkit_generic_utils import (
    read_lst,
    save_dct,
    spl_char_to_entity,
    raw_to_combined_tag_map,
)


def make_distinct(label_lst):
    """
    Make the label_lst distinct
    """
    tag2cnt, new_tag_lst = {}, []
    if len(label_lst) > 0:
        for tag_item in label_lst:
            _ = tag2cnt.setdefault(tag_item, 0)
            tag2cnt[tag_item] += 1
            tag, wrd = tag_item
            new_tag_lst.append((tag, wrd, tag2cnt[tag_item]))
        assert len(new_tag_lst) == len(set(new_tag_lst))
    return new_tag_lst


def get_gt_pred(score_type, hypo, ref, eval_label):
    """
    Read the GT and predicted utterances in the entity format [(word1, tag1), (word2, tag2), ...]
    """
    entity_end_char = "]"
    entity_to_spl_char = {}
    for spl_char, entity in spl_char_to_entity.items():
        entity_to_spl_char[entity] = spl_char

    def update_label_lst(lst, phrase, label):
        if eval_label == "combined":
            label = raw_to_combined_tag_map[label]
        if label != "DISCARD":
            if score_type == "label":
                lst.append((label, "phrase"))
            else:
                lst.append((label, phrase))

    sent_lst_dct = {"hypo": [], "ref": []}
    label_lst_dct = {"hypo": [], "ref": []}

    for pfx in ["hypo", "ref"]:
        if pfx == "hypo":
          all_text = read_lst(hypo)
        else:
          all_text = read_lst(ref)
        all_text = [line.split(" (None")[0] for line in all_text]
        #print(pfx,all_text)
        for line in all_text:
            label_lst = []
            line = line.replace("  ", " ")
            wrd_lst = line.split(" ")
            sent_lst_dct[pfx].append(line)
            phrase_lst, is_entity, num_illegal_assigments = [], False, 0
            for idx, wrd in enumerate(wrd_lst):
                if wrd in spl_char_to_entity:
                    if (
                        is_entity
                    ):  # a new entity began before completion of the previous entity
                        phrase_lst = []  # discard the ongoing entity
                        num_illegal_assigments += 1
                    is_entity = True
                    entity_tag = spl_char_to_entity[wrd]
                elif wrd == entity_end_char:
                    if is_entity:
                        if len(phrase_lst) > 0:
                            update_label_lst(
                                label_lst, " ".join(phrase_lst), entity_tag
                            )
                        else:  # entity end without entity start
                            num_illegal_assigments += 1
                        phrase_lst = []
                        is_entity = False
                    else:
                        num_illegal_assigments += 1
                else:
                    if is_entity:
                        phrase_lst.append(wrd)
            label_lst_dct[pfx].append(make_distinct(label_lst))

    return label_lst_dct, sent_lst_dct


def eval_ner(hypo, ref, save_as=None, eval_label="combined"):
    metrics = {}
    for score_type in ["standard", "label"]:
      labels_dct, text_dct = get_gt_pred(score_type, hypo, ref, eval_label)
      metrics[score_type] = eval_utils.get_ner_scores(labels_dct["ref"], labels_dct["hypo"])
      print(score_type+" fscore: ", 100 * metrics[score_type]["overall_micro"]["fscore"])
      print(metrics[score_type])
    if save_as:
      save_dct(save_as, metrics) # save as json

def e2e_ner_score(file, save_as=None, split="dev", label="combined"):
    with importlib.resources.path('slue_evaluator','data') as data_path:
        ref = os.path.join(data_path, f"{split}.raw.wrd")
    eval_ner(file,ref,save_as,label)
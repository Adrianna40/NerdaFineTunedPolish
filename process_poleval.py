# credit to https://github.com/CLARIN-PL/PolDeepNer
import codecs
from annotation import Annotation


def wrap_annotations(sentences):
    annotations = []
    tid = 0
    for sid, labels in enumerate(sentences):
        for idx, label in enumerate(labels):
            for ann in label.split('#'):
                type = ann[2:]
                if 'B-' in ann:
                    annotations.append(Annotation(type, sid, tid))
                elif 'I-' in ann:
                    for _ann in reversed(annotations):
                        if type == _ann.annotation:
                            _ann.add_id(tid)
                            break
            tid += 1
    return annotations


def get_id(ini_file):
    for line in codecs.open(ini_file, "r", "utf8"):
        if 'id = ' in line:
            return line.replace('id = ', '')


def align_tokens_to_text(sentences, text):
    offsets = []
    tid = 0
    for s in sentences:
        for t in s:
            start = text.find(t, tid)
            if start == -1:
                raise Exception("Could not align tokens to text")
            end = start + len(t)
            offsets.append((start, end))
            tid = end
    return offsets


def get_poleval_dict(doc_id, text, sentences, labels):
    ''' Returns PolEval dict
    {
        text:
        id:
        answers:
    }
    Note that arguments it takes is FILE, PATH, FILE as utils.load_data_and_labels opens file itself
    '''
    annotations = wrap_annotations(labels)
    offsets = align_tokens_to_text(sentences, text)
    answers = []
    for an in annotations:
        begin = offsets[an.token_ids[0]][0]
        end = offsets[an.token_ids[-1]][1]
        orth = text[begin:end]
        answers.append("%s %d %d\t%s" % (an.annotation.replace("-", "_"), begin, end, orth))
    return ({
        'text': text,
        'id': doc_id,
        'answers': "\n".join(answers)
    })
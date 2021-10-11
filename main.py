import nltk
from NERDA.precooked import Precooked
from process_poleval import get_poleval_dict


if __name__ == '__main__':
    nltk.download('punkt')

    loaded_model = Precooked(
        tag_scheme=['B-geogName', 'I-orgName', 'B-time', 'I-placeName', 'I-geogName', 'B-persName', 'I-persName',
                    'I-date', 'B-date', 'B-placeName', 'I-time', 'B-orgName'],
        tag_outside='O',
        transformer='allegro/herbert-base-cased',
        max_len=128)
    loaded_model.load_network_from_file('nermodel.bin')
    text = 'Panie Janie, panie Janie, pora wstać!'
    sentences, labels = loaded_model.predict_text(text)
    print(get_poleval_dict('123', text, sentences, labels))

import re
from nltk.tokenize import sent_tokenize



def split_text(text, source_lang, input_length=64):
    """
    Splits the input text into sentences and creates batches of sentences to be fed into the model.

    Args:
        text (str): The input text to be split into sentences.
        source_lang (str): The language of the input text.
        language_codes (dict): A dictionary mapping language names to their corresponding language codes.
        input_length (int): The maximum number of tokens in a batch.

    Returns:
        A list of lists, where each inner list contains a batch of sentences. Each batch is represented as a list of strings.
    """        

    language_codes = {
        "en": "english",
        "de": "german",
        "fr": "french",
        "es": "spanish",
        "it": "italian",
        "nl": "dutch",
        "pl": "polish",
        "pt": "portuguese",
        "tr": "turkish",
        "ru": "russian",
        "ar": "arabic",
        "zh": "chinese",
        "ja": "japanese",
        "ko": "korean",
        "vi": "vietnamese",
        "th": "thai",
        "hi": "hindi",
        "bn": "bengali",
                     }
    
    paragraphs = text.split("\n")
    if source_lang == "zh":
        sentenced_paragraphs = [re.split(r'[。！？]', paragraph) if paragraph else ['<p>'] for paragraph in paragraphs]
        return sentenced_paragraphs

    else:    
        sentenced_paragraphs = [sent_tokenize(paragraph, language=language_codes[source_lang]) if paragraph else ['<p>--</p>'] for paragraph in paragraphs]
    input_paragraphs = [" ".join([sentence + " end_of_sentence" for sentence in sentences]) for sentences in sentenced_paragraphs]

    input_sentences = []
    for input_paragraph in input_paragraphs:
        temp = []
        text_tokens = input_paragraph.split()
        start_idx = 0

        while start_idx < len(text_tokens):
            end_idx = start_idx + input_length
            if end_idx > len(text_tokens):
                end_idx = len(text_tokens)
            chunk = " ".join(text_tokens[start_idx:end_idx])
            if chunk.endswith("end_of_sentence"):
                temp.append(chunk.replace(" end_of_sentence", "").replace("end_of_sentence", ""))
                start_idx = end_idx
            else:
                for i in range(end_idx, len(text_tokens)):
                    chunk += " " + text_tokens[i]
                    if text_tokens[i].endswith("end_of_sentence"):
                        temp.append(chunk.replace("end_of_sentence", ""))
                        start_idx = i + 1
                        break
        input_sentences.append(temp)
    return input_sentences

def translate_text(input_texts_list,pipeline):
    """
    Translates a list of texts into the target language using a given pipeline function and split text function.

    Args:
        text (list of str): A list of texts to be translated.
        split_text_fn (function): A function that splits the input text into sentences and creates batches of sentences to be fed into the model.
        pipeline_fn (function): A function that takes a list of input texts and returns a list of dictionaries containing the translations.

    Returns:
        translated_texts (list of str): A list of translated texts in the target language. 
        The order of the texts in the output list corresponds to the order of the input texts in the text parameter.
    """
    
    translated_texts = []
    for input_texts in input_texts_list:
        # Translate each input chunk and combine the translated chunks into the final translated text
        output_texts = []
        for texts in input_texts:
            translation_result = pipeline(texts)
            translated_result = [result["translation_text"] for result in translation_result]
            output_texts.append(" ".join(translated_result))
        translated_texts.append("\n".join(output_texts).replace("<p>--</p>", "").replace("<p>", ""))
    return translated_texts

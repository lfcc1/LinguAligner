# LinguAligner
We developed a Python package called [LinguAligner](https://pypi.org/project/LinguAligner/), a comprehensive corpus translation and alignment pipeline designed to facilitate the translation of corpora across different languages. It translates corpora using machine translation and aligns the translated annotations with their corresponding translated text. Initially developed for the automatic translation of [ACE-2005 into Portuguese](https://catalog.ldc.upenn.edu/LDC2024T05) , LinguAligner has since been adapted into a versatile package for effortless translation of other corpora.

It is composed of two main components: 

- Text translation: We support DeepL Translator, Google Translator and Microsoft Translators APIs. 
- Annotations alignments: We developed an annotation alignment pipeline that uses several alignment techniques to align the translated annotations within the translated text.

You can access the LinguAligner Python package [here](https://pypi.org/project/LinguAligner/).

The ACE-2005-PT corpus (Portuguese translation produced with LinguAligner), was published by the Linguistic Data Consortium. For more details, visit the [LDC catalog](https://catalog.ldc.upenn.edu/LDC2024T05). 

## Annotation Alignment Modules
Our pipeline is composed of a total of five annotation alignment components:

    - Lemmatization
    - Multiple word translation
    - BERT-based word aligner
    - Gestalt Patter Matching
    - Levenstein distance

The pipeline operates sequentially, meaning that annotations aligned by earlier methods are not addressed by subsequent pipeline elements. According to our experiments, the list above corresponds to the best order sequence.


## Usage



1. **Translate Corpora**
    You can use the Translation APIs or can translate your corpus with an external tool
    An API key is needed to use some of the Translation APIs.
    
```python
from LinguAligner import translation

# Google Translator
translator = translation.GoogleTranslator(source_lang="en", target_lang="pt")
translated_text = translator.translate("The soldiers were ordered to fire their weapons")

# DeepL Translator
translator = translation.DeepLTranslator(source_lang="en", target_lang="pt", key="DEEPL_KEY")
translated_text = translator.translate("The soldiers were ordered to fire their weapons")

# Microsoft Translator
translator = translation.MicrosoftTranslator(source_lang="en", target_lang="pt", key="MICROSOFT_TRANSLATOR_KEY")
translated_text = translator.translate("The soldiers were ordered to fire their weapons")
print(translated_text)

```


2. **Run the Annotation Alignment Pipeline**
    Users can select the aligners they intend to use and specify the order in which they should be utilized. To find the best component order in the pipeline
we experimented with all the permutations between the components and calculated the corresponding alignment results using a manually aligned corpus. 
According to our findings, the best sequence order is the ones presented in the example below, however, we encourage you to experiment with different orders for your specific use case.
    
    Certain alignment methods, like multiple translations (M_Trans), necessitate the prior calculation of multiple translations for each annotation (as explained at the end of this section).

```python
from LinguAligner import AlignmentPipeline

"""
(By default, the first method used is string matching. If unsuccessful, the alignment pipeline is employed.)
Methods:
- lemma: Lemmatization
- M_Trans: Multiple Translations of a word
- word_aligner: mBERT-based word aligner
- gestalt: Gestalt pattern matching (character-based)
- levenshtein: Levenshtein distance (character-based)
"""

config= {
    "pipeline": [ "lemma", "M_Trans", "word_aligner","gestalt","leveinstein"], # can be changed according to the desired pipeline
    "spacy_model": "pt_core_news_lg", # change according to the target language
    "WAligner_model": "bert-base-multilingual-uncased", # needed for word_aligner
}

aligner = AlignmentPipeline(config)

src_sentence = "The soldiers were ordered to fire their weapons."
src_annotation = "fire"
translated_sentence = "Os soldados receberam ordens para disparar as suas armas."
translated_annotation = "incêndio"

target_annotation = aligner.align_annotation(src_sentence, src_annotation, translated_sentence, translated_annotation)
print(target_annotation)

>>> ('disparar', (34, 41))

```
For example, in the sentence 'The soldiers were ordered to fire their weapons,' the word 'fire' was annotated in the source corpus. However, when this sentence is translated to 'Os soldados receberam ordens para disparar as suas armas,' the word 'fire' is translated to 'incêndio' (fire as a noun) in isolation, and to 'disparar' (as a verb) in the translated sentence.

*Spacy models must be pre-installed corresponding to the target language.


### Specify source annotation start index to find the closest target annotation
```python

src_sentence = "he was a good man because he had a kind heart"
src_annotation = "he"
translated_sentence = "ele era um bom homem porque ele tinha um bom coração" # there are multiple tokens "ele" (he)
translated_annotation = "ele"

#add src_ann_start argument
target_annotation = aligner.align_annotation(src_sentence, src_annotation, translated_sentence, translated_annotation, src_ann_start=29)
print(target_annotation)

>>> ('ele', (28, 30))

```
**Note** 

To use the M_trans method, multiple translations of the annotations must be computed beforehand and passed as an argument to the align_annotation function. These translations should contained in a Python dictionary, where the source annotation serves as the key, and the corresponding value is a list of alternative translations. You can generate this dictionary using the following code (need a MICROSOFT_TRANSLATOR_KEY):


```python

from LinguAligner import translation
translator = translation.MicrosoftTranslator(source_lang="en", target_lang="pt", auth_key="MICROSOFT_TRANSLATOR_KEY")
lookupTable = {}
annotations_list = ["war","land","fire"]
for word in annotations_list:
    lookupTable[word] = translator.getMultipleTranslations(word) # change the language codes according to the desired languages

# Then, pass the lookupTable to the align_annotation method
x = aligner.align_annotation("The soldiers were ordered to fire their weapons","fire", "Os soldados receberam ordens para disparar as suas armas","incêndio",lookupTable)
```

The lookup table should resemble the following example:

```
{
    'fire': 
        [
            'fogo',
            'incêndio',
            'demitir',
            'despedir',
            'fogueira',
            'disparar',
            'chamas',
            'dispare',
            'lareira',
            'atirar',
            'atire'
        ],
    ...
}
  ```

## Evaluation
To measure the effectiveness of the alignment pipeline we tested it on ACE-2005 corpus. Manual alignments were conducted on the entire ACE-2005-PT test set, which includes 1,310 annotations. These alignments were performed by a linguist expert to ensure high-quality annotations, following the same annotation [guidelines](https://www.ldc.upenn.edu/sites/www.ldc.upenn.edu/files/english-events-guidelines-v5.4.3.pdf) of the original ACE-2005 corpus. Then we compare the manual alignments against the ones generated by our pipeline.

The evaluation results are presented in Table 1:

<p>
    <img src="https://github.com/lfcc1/LinguAligner/blob/main/img/eval_by_comp.png?raw=true" alt="Results" width="500"/>
    <br>
    <em>Table 1: Evaluation Results by pipeline component</em>
</p>



## License

This project is licensed under the [MIT License](LICENSE).

## Citation

Coming Soon.



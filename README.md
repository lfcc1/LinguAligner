<p align="center">
  <img src="https://github.com/lfcc1/LinguAligner/blob/main/img/lingualigner.png" alt="LinguAligner Logo" width="300"/>
</p>


**LinguAligner** is a Python package for automatically translating annotated corpora while preserving their annotations. It supports multiple translation APIs and alignment strategies, making it a valuable tool for NLP researchers building multilingual datasets, particularly for low-resource languages.

Natural Language Processing (NLP) research remains heavily centered on English, creating a language imbalance in AI. One way to improve linguistic diversity is by adapting annotated corpora from high-resource languages to others.  However, preserving span-based annotation quality after translation requires precise alignment of annotations between the source and translated texts, a challenging task due to lexical, syntactic and semantic divergences between languages. **LinguAligner** provides an automated pipeline to align annotations within translated texts using a several annotation alignment strategies.

## 🚀 Features

- 🌐 **Translation Module**:  
  Supports external translation services:  
  - Google Translate  
  - Microsoft Translator  
  - DeepL  

- 🧠 **Annotation Alignment Module**:  
  Implements multiple techniques:  
  - **Exact / Fuzzy Matching**: Levenshtein, Gestalt  
  - **Lemmatization-based Matching** using [spaCy](https://spacy.io/)  
  - **Pre-compiled Translation Dictionaries** via Microsoft Lookup API  
  - **Multilingual Contextual Embeddings** using [BERT-multilingual](https://huggingface.co/bert-base-multilingual-uncased)  

The pipeline operates sequentially, meaning that annotations aligned by earlier methods are not addressed by subsequent pipeline elements. According to our experiments, the list above corresponds to the best order sequence.

## 📦 Installation

Install via [PyPI](https://pypi.org/project/LinguAligner/):

```bash
pip install LinguAligner
```

## 🧪 Example Usage
### 1. Translate Corpora
You can use the Translation APIs or can translate your corpus with an external tool (an API key is needed).
```python
from LinguAligner import translation

# Google Translate
translator = translation.GoogleTranslator(source_lang="en", target_lang="pt", key="Google_KEY")
translated_text = translator.translate("The soldiers were ordered to fire their weapons")

# DeepL
translator = translation.DeepLTranslator(source_lang="en", target_lang="pt", key="DEEPL_KEY")
translated_text = translator.translate("The soldiers were ordered to fire their weapons")

# Microsoft
translator = translation.MicrosoftTranslator(source_lang="en", target_lang="pt", key="MICROSOFT_KEY")
translated_text = translator.translate("The soldiers were ordered to fire their weapons")

print(translated_text)

```

### 2. Align Annotations

Users can select the aligner strategies they intend to use and specify the order in which they should be utilized. According to our findings, the best sequence order is the ones presented in the example below, however, we encourage you to experiment with different orders for your specific use case.
    
```python
from LinguAligner import AlignmentPipeline

# Define pipeline and model configuration
config = {
    "pipeline": ["lemma", "M_trans", "word_aligner", "gestalt", "levenshtein"],
    "spacy_model": "pt_core_news_lg",
    "WAligner_model": "bert-base-multilingual-uncased"
}

aligner = AlignmentPipeline(config)

# Source and translated data
src_sent = "The soldiers land on the shore..."
src_ann = "land"
trans_sent = "Os soldados aterraram na costa."
trans_ann = "terra"  # Expected direct translation

# Perform annotation alignment
target_annotation = aligner.align_annotation(
    src_sent, src_ann, trans_sent, trans_ann
)

print(target_annotation)
# Output: ('aterraram', (12, 21))
```

In this example, the word `land` is translated to `terra` (land as a noun) when considered in isolation, but as `aterraram` (land as a verb) when translated in context. Although `terra` is a valid translation of the annotation, it does not occur in the translated sentence and therefore cannot be aligned. Such misalignments highlight the need for additional processing to determine the correct annotation offsets in the translated text, in this case, mapping the word `terra` to `aterraram` .


## 🔧 Configuration

You can customize the alignment behavior in the `config` variable:

```python
config = {
    "pipeline": ["lemma", "word_aligner", "levenshtein"], # change pipeline elements and order
    "spacy_model": "fr_core_news_md", # change spacy model
    "WAligner_model": "bert-base-multilingual-uncased" # change multilingual model
}
```

## 🔧 Advanced Options

### Specify source annotation index to resolve ambiguity (Multiple Source Matches)
```python
src_sent = "he was a good man because he had a kind heart"
src_ann = "he"
trans_sent = "ele era um bom homem porque ele tinha um bom coração"
trans_ann = "ele"

target_annotation = aligner.align_annotation(
    src_sent, src_ann, trans_sent, trans_ann, src_ann_start=29
)

print(target_annotation)
# Output: ('ele', (28, 30))
```

### Using the M_trans Method
The `M_trans` method relies on having multiple possible translations for each annotation. These must be prepared in advance and stored in a Python dictionary, where each key is a source annotation and the value is a list of alternative translations.

You can generate this translation dictionary using the Microsoft Translator API (requires a MICROSOFT_TRANSLATOR_KEY):


```python
from LinguAligner import translation

translator = translation.MicrosoftTranslator(
    source_lang="en", target_lang="pt", auth_key="MICROSOFT_TRANSLATOR_KEY"
)

annotations_list = ["war", "land", "fire"]
lookup_table = {}

for word in annotations_list:
    lookup_table[word] = translator.getMultipleTranslations(word)

# Use the lookup table in align_annotation
aligner.align_annotation(
    "The soldiers were ordered to fire their weapons",
    "fire",
    "Os soldados receberam ordens para disparar as suas armas",
    "incêndio",
    M_trans_dict=lookup_table
)
```


#### 🔎 Example output of a lookup table:

```python
{
  "fire": [
    "fogo",
    "incêndio",
    "demitir",
    "despedir",
    "fogueira",
    "disparar",
    "chamas",
    "dispare",
    "lareira",
    "atirar",
    "atire"
  ]
}

```
## 📚 Use Cases

LinguAligner was used to create translated versions of the following annotated corpora:

- **ACE-2005** (EN → PT): Event extraction benchmark, now available in Portuguese via the [LDC](https://catalog.ldc.upenn.edu/LDC2024T05)  
- **T2S LUSA** (PT → EN): Portuguese news event corpus adapted to English [10.25747/ESFS-1P16](https://doi.org/10.25747/ESFS-1P16)  
- **MAVEN**: (EN → PT) High-coverage event trigger corpus from Wikipedia translated to Portuguese (available in this repository)
- **WikiEvents**: (EN → PT) Document-level event extraction dataset translated to Portuguese (available in this repository)


## 🧩 Citation

### Coming soon...


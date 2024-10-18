"""LinguAligner is a Python library for aligning annotations in parallel corpora. It is designed to be used in the context of parallel corpora annotation alignment, where the goal is to align annotations in the source language with annotations in the target language. """
__version__ = "0.35"


from . import aligners
import spacy
from . import translation
from transformers import BertTokenizer, BertModel, logging
import logging
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)


config_default = config= {
    "pipeline": [ "lemma", "M_Trans", "word_aligner","gestalt","leveinstein"], # can be changed according to the desired pipeline
    "spacy_model": "pt_core_news_lg", # change according to the language
    "WAligner_model": "bert-base-multilingual-uncased", # needed for word_aligner
}
 
class AlignmentPipeline:
    def __init__(self, config=config_default):
        self.config = config
        print("Loading spacy model: " + config["spacy_model"])
        self.nlp = spacy.load(config["spacy_model"])
        print("Model loaded")
        if "word_aligner" in config["pipeline"]:
            print("Loading WAligner model: " + config["WAligner_model"])
            self.tokenizer = BertTokenizer.from_pretrained(config["WAligner_model"])
            self.model = BertModel.from_pretrained(config["WAligner_model"])
            print("Model loaded")

    def align_annotation(self, src_sent, src_ann, tgt_sent, trans_ann, src_ann_start=0, lookupTable=None):
        pipeline = self.config["pipeline"]
        
        #if "M_Trans" in pipeline and lookupTable == None:              
            #pipeline.remove("M_Trans")
            #print("Lookup table not provided for M_Trans method. (skipped)")
        nlp = self.nlp
        res = aligners.regex_string_match(tgt_sent,trans_ann) 
        span = (-1,-1)
        if not res:
            i = 0
            while i < len(pipeline) and not res:
                method = pipeline[i]
                #print(method)
                if method == 'lemma':
                    res = aligners.lemma_match(tgt_sent,trans_ann,nlp)
                elif method == 'M_Trans': # Mtrans is combined with lemma method since we also calculate the lemma of the translations
                    if lookupTable != None: 
                        res = aligners.resource_match(tgt_sent,src_ann,nlp,lookupTable)
                elif method == 'word_aligner':
                    res = aligners.wordAligner(src_sent,tgt_sent,src_ann,nlp, self.tokenizer, self.model)
                elif method == 'gestalt':
                    res = aligners.gestalt_match(tgt_sent,trans_ann,nlp)
                elif method == 'leveinstein':
                    res = aligners.leveinstein_match(tgt_sent,trans_ann,nlp)
                else:
                    print(f"Invalid alignment method: {method}")
                i += 1
        
        if res:
            span = aligners.closest_occurrence(tgt_sent,res,src_ann_start)
            
        return res, span
    


#res = align_annotation("The ship land on the shore","O barco desembarcou na costa","land","terra",nlp) # Expected output: "teste
#print(res)

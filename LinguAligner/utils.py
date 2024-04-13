
def contains(scope,trigger,nlp):
    
    offsets, offsets2 = [], []
    new_scope, new_trigger = [], []

    for ind, lemma in enumerate(scope):
        for t in nlp(lemma):
            offsets.append(ind)
            new_scope.append(t.text)

    for ind, lemma in enumerate(trigger):
        for t in nlp(lemma):
            offsets2.append(ind)
            new_trigger.append(t.text)
            
    Nscope, Ntrigger = len(new_scope), len(new_trigger)
    i, LAST = 0, Nscope-Ntrigger+1
    while True:
        try:
            found = new_scope.index(new_trigger[0], i, LAST) # find first elem in sub
        except ValueError:
            return False
        if new_scope[found:found+Ntrigger] == new_trigger:
            found = offsets[found]
            return (found, found+len(trigger)-1)
        else:
            i = found+1


def normalizeTokens(tokens):
    return [token.lower().strip() for token in tokens]


def clean(entries):
    out =  []
    for entry in entries:
        #print(entry)
        new_entry = {}
        new_entry["sentence"] = entry["sentence_pt"]
        new_entry["sentence_en"] = entry["sentence"]
        new_entry["event-mentions"] = []
        for mention in entry["golden-event-mentions"]:
            
            new_mention = {}
            new_mention["id"] = mention["id"]
            new_mention["event_type"] = mention["event_type"]
            
            new_trigger = {}
            new_trigger["start"] = mention["trigger"]["start"]
            new_trigger["end"] = mention["trigger"]["end"]
            new_trigger["text"] = mention["trigger"]["text_pt"]
            new_trigger["text_en"] = mention["trigger"]["text"]
            new_mention["trigger"] = new_trigger

            new_mention["arguments"] = []
            for argument in mention["arguments"]:
                new_arg = {}
                new_arg["id"] = argument["entity-id"]
                new_arg["role"] = argument["role"]
                new_arg["text"] = argument["text_pt"]
                new_arg["start"] = argument["start"]
                new_arg["end"] = argument["end"]
                new_arg["text_en"] = argument["text"]
                new_mention["arguments"].append(new_arg)
            new_entry["event-mentions"].append(new_mention)
        out.append(new_entry)
    return out
    
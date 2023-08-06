import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


checkpoint = "aomar85/fine-tuned-arabert-random-negative"
model = AutoModelForSequenceClassification.from_pretrained(checkpoint) 
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

def get_prediction(example, glosses):
    contexts = np.repeat(example, len(glosses)).tolist()
    list_of_glosses = list(glosses.values())



    tokenized_texts = tokenizer(contexts,
                                list_of_glosses,
                                padding=True,
                                truncation=True ,
                                add_special_tokens =True,
                                max_length=512,
                                return_tensors='pt')


    model.eval()
    pt_inputs = {k: torch.tensor(v) for k, v in tokenized_texts.items()}
    with torch.no_grad():
        output = model(**pt_inputs)

    output.logits.cpu().numpy()

    logits = output.logits


    probs = torch.nn.functional.softmax(logits, dim=-1)

    MAX_PREDICTION= np.argmax(logits, axis=0).flatten()[1]
    MAX_PROBABLILITY =np.argmax(probs,axis=0).flatten()[1]


    res =dict()
    res = {
        'Pred_Wikidata_IQ' :list(glosses.keys())[MAX_PREDICTION] ,
        'Pred_Wikidata_Desc':list(glosses.values())[MAX_PREDICTION],
        'score':probs[MAX_PROBABLILITY][1].detach().item(),        
    }

    return res

def disambiguate(sentence, glosses):

        result = get_prediction(sentence, glosses)
        content = {"resp": result, "statusText":"OK","statusCode":0}
        return content



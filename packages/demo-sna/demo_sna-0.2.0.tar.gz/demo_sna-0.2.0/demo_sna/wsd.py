import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


checkpoint = "aomar85/M5"
model = AutoModelForSequenceClassification.from_pretrained(checkpoint) 
tokenizer = AutoTokenizer.from_pretrained(checkpoint)



def tsv(example, glosses):
    
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
    return probs



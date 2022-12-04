'''Items prediction module using the trained model'''
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


class Predictor:  # pylint: disable=too-few-public-methods
    '''Class used to predict input items.'''
    def __init__(self):
        model_path = '/main/gpt-j-6B-vietnamese-news'
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path,
                                                          torch_dtype=torch.float16,
                                                          low_cpu_mem_usage=True)
        self.model.parallelize()

    def predict(self, text, top_k, top_p, n_samples):
        input_ids = self.tokenizer.encode(text, return_tensors='pt').to('cuda:0')

        outputs = self.model.generate(
            input_ids,
            max_length=256,
            do_sample=True,
            top_k=top_k,
            top_p=top_p,
            num_return_sequences=n_samples,
        )

        return [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

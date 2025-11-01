#
# lineclip.py 2025/03/16
# https://huggingface.co/line-corporation/clip-japanese-base
#
import torch
from transformers import AutoImageProcessor, AutoModel, AutoTokenizer

class Association:
    def __init__(self):
        HF_MODEL_PATH = 'line-corporation/clip-japanese-base'
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(HF_MODEL_PATH, trust_remote_code=True)
        self.processor = AutoImageProcessor.from_pretrained(HF_MODEL_PATH, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(HF_MODEL_PATH, trust_remote_code=True).to(self.device)

    def assoc_img_txts(self, img, txt, scale=1.0):
        image = self.processor(img, return_tensors="pt").to(self.device)
        text = self.tokenizer(txt).to(self.device)
        with torch.no_grad():
            image_features = self.model.get_image_features(**image)
            text_features = self.model.get_text_features(**text)
            text_probs = (scale*image_features @ text_features.T).softmax(dim=-1)
        probs = [float(x) for x in text_probs[0]]
        return probs

if __name__=='__main__':
    import io
    import requests
    from PIL import Image
    association = Association()
    img = Image.open(io.BytesIO(requests.get('https://images.pexels.com/photos/2253275/pexels-photo-2253275.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=750&w=1260').content))
    txt = ["狼", "犬", "猫", "象"]
    probs = association.assoc_img_texts(img, txt, scale=0.1)
    print(txt, ':', probs)

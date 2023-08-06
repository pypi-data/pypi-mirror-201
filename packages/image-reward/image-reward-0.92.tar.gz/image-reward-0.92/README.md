# ImageReward-Pypi

ImageReward is the first general-purpose text-to-image human preference RM which is trained on in total 137k pairs of expert comparisons, based on text prompts and corresponding model outputs from DiffusionDB. We demonstrate that ImageReward outperforms existing text-image scoring methods, such as CLIP, Aesthetic, and BLIP, in terms of understanding human preference in text-to-image synthesis through extensive analysis and experiments.

## Approach

![ImageReward](ImageReward.png)

## Setup

* Environment: install dependencies via `pip install -r requirements.txt`. 

## Usage

```python
import os
import torch
import ImageReward as reward

if __name__ == "__main__":
    prompt = "a painting of an ocean with clouds and birds, day time, low depth field effect"
    img_prefix = "assets/images"
    generations = [f"{pic_id}.webp" for pic_id in range(1, 5)]
    img_list = [os.path.join(img_prefix, img) for img in generations]
    model = reward.load()
    with torch.no_grad():
        ranking, rewards = model.inference_rank(prompt, img_list)
        # Print the result
        print("\nPreference predictions:\n")
        print(f"ranking = {ranking}")
        print(f"rewards = {rewards}")
        for index in range(len(img_list)):
            score = model.score(prompt, img_list[index])
            print(f"{generations[index]:>16s}: {score:.2f}")

```

The output will look like the following (the exact numbers may be slightly different depending on the compute device):

```
Preference predictions:

ranking = [1, 2, 3, 4]
rewards = [[0.5811622738838196], [0.2745276093482971], [-1.4131819009780884], [-2.029569625854492]]
          1.webp: 0.58
          2.webp: 0.27
          3.webp: -1.41
          4.webp: -2.03
```

## Test

### Setup for baselines

#### Environment

```bash
$ pip install git+https://github.com/openai/CLIP.git
```

#### Checkpoint

Models | File Paths | Download Links
--- | :---: | :---: 
ImageReward | checkpoint/ | <a href="https://huggingface.co/THUDM/ImageReward/blob/main/ImageReward.pt">Download</a>
CLIP Score | checkpoint/clip/ | <a href="https://openaipublic.azureedge.net/clip/models/b8cca3fd41ae0c99ba7e8951adf17d267cdb84cd88be6f7c2e0eca1737a03836/ViT-L-14.pt">Download</a>
BLIP Score | checkpoint/blip/ | <a href="https://storage.googleapis.com/sfr-vision-language-research/BLIP/models/model_large.pth">Download</a>
Aesthetic | checkpoint/aesthetic/ | <a href="https://github.com/christophschuhmann/improved-aesthetic-predictor/raw/main/sac%2Blogos%2Bava1-l14-linearMSE.pth">Download</a>

#### Data

Data | File Paths | Download Links
--- | :---: | :---: 
test_images | data/ | <a href="https://huggingface.co/THUDM/ImageReward/blob/main/test_images.zip">Download</a>

Download `test_images.zip` and unzip it to `data/test_images/`

### One step for test

```bash
$ python test.py
```

The test result is:

Models | Preference Acc.
--- | :---:
CLIP Score | 54.82
Aesthetic Score | 57.35
BLIP Score | 57.76
ImageReward (Ours) | **65.14**
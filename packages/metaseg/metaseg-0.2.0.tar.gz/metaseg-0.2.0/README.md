<div align="center">
<h2>
     MetaSeg: Packaged version of the Segment Anything repository
</h2>
<div>
    <img width="1000" alt="teaser" src="https://github.com/kadirnar/segment-anything-pip/releases/download/v0.1.2/metaseg_demo.png">
</div>
    <a href="https://badge.fury.io/py/metaseg"><img src="https://badge.fury.io/py/metaseg.svg" alt="pypi version"></a>

</div>

This repo is a packaged version of the [segment-anything](https://github.com/facebookresearch/segment-anything) model.


### Installation
```bash
pip install metaseg
```

### Usage
```python
from metaseg import SegAutoMaskGenerator

SegAutoMaskGenerator(
        model_type="vit_h", # "vit_l", "vit_b"
        source= "test.png", # test.mp4
        device="cuda", # "cpu" or "cuda"
        show=True, 
)
```

# invisible-watermark by dwt+dct
[![PyPI](https://img.shields.io/pypi/v/invisible-watermark)](https://pypi.org/project/invisible-watermark/)
[![License](https://img.shields.io/pypi/l/invisible-watermark.svg)](https://github.com/ShieldMnt/invisible-watermark/blob/main/LICENSE)

invisible-watermark is a **python** library and command line tool for creating invisible watermark over image (a.k.a. **blink image watermark**, **digital image watermark**). The algorithm doesn't rely on the original image.

**Note that** this library is still experimental and it doesn't support GPU acceleration, carefully deploy it on the production environment. The default method **dwtDCT**(one variant of frequency methods) is ready for on-the-fly embedding, the other methods are too slow on a CPU only environment.


[supported algorithms](https://github.com/ShieldMnt/invisible-watermark#supported-algorithms)
* [Discrete wavelet transform](https://en.wikipedia.org/wiki/Discrete_wavelet_transform) + [Discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform) frequency embedding algorithm variants.

[speed](https://github.com/Pakkamat/stealth_watermark/tree/main?tab=readme-ov-file#running-speed-cpu-only)
* default embedding method ```dwtDct``` is fast and suitable for on-the-fly embedding

accuracy
* The algorithm **cannot guarantee** to decode the original watermarks 100% accurately even though we don't apply any attack.
* Known defects: Test shows all algorithms do not perform well for web page screenshots or posters with homogenous background color

## Supported Algorithms
* [**frequency methods**](https://github.com/ShieldMnt/invisible-watermark/wiki/Frequency-Methods)
 
> * **dwtDct**: DWT + DCT transform, embed watermark bit into max non-trivial coefficient of block dct coefficents

> background:
> * [Discrete wavelet transform](https://en.wikipedia.org/wiki/Discrete_wavelet_transform)
> * [Discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform).

## How to install
`pip install invisible-watermark`
`pip install Flask`
`pip install opencv-python`
`pip install pyrebase`

## [Library API](https://github.com/ShieldMnt/invisible-watermark/wiki/API)
### How to use
1. Open app.py

2. Input your data from your [Google Firebase](https://firebase.google.com/)
```python
config = {
  "apiKey":"Your api key",
  "authDomain": "Your authDomain",
  "databaseURL": "Your databaseURL",
  "storageBucket": "Your storageBucke"
}
```
3. Run app.py
```python
python app.py
```

4. Open http://127.0.0.1:5888/ on your browser

## CLI Usage

```
embed watermark:  python ./invisible-watermark -v -a encode -t bytes -m dwtDct -w 'test' -o ./uploads/wm.png ./test/images/British_Shorthair_156.jpg

decode watermark: python ./invisible-watermark -v -a decode -t bytes -m dwtDct -l 48 ./uploads/wm.png

positional arguments:
  input                 The path of input

optional arguments:
  -h, --help            show this help message and exit
  -a ACTION, --action ACTION
                        encode|decode (default: None)
  -t TYPE, --type TYPE  bytes (default: None)
  -m METHOD, --method METHOD
                        dwtDct (default: None)
  -w WATERMARK, --watermark WATERMARK
                        embedded string (default: None)
  -l LENGTH, --length LENGTH
                        watermark bits length, required for bytes
                        watermark (default: 0)
  -o OUTPUT, --output OUTPUT
                        The path of output (default: None)
  -v, --verbose         print info (default: False)
```

## Test Result
 
For better doc reading, we compress all images in this page, but the test is taken on 1920x1080 original image.

Methods are not robust to **resize** or aspect ratio changed **crop** but robust to **noise**, **color filter**, **brightness** and **jpg compress.**

**only default method is ready for on-the-fly embedding.**

### Input
> * Input Image: 1960x1080 Image
> * Watermark: 
>   - For freq method, we use 64bits, string expression "qingquan"
>   - For RivaGan method, we use 32bits, string expression "qing"
> * Parameters: only take U frame to keep image quality, ```scale=36```

### Attack Performance


**Test embed watermark in 100 images**
*Showing 1 image out of 100 images*

| Number | Attacks | Example Image | Detected |
| --- | --- | --- | --- |
| 1 | Re-download | ![wm_redownload](https://raw.githubusercontent.com/Pakkamat/stealth_watermark/main/Test/image_downloads/1_wm.png) | 80% |
| 2 | Crop 1/4 | ![wm_crop](https://raw.githubusercontent.com/Pakkamat/stealth_watermark/main/Test/image_crop/1_wm.png) | Fail |
| 3 | Brightness | ![wm_rotate](https://raw.githubusercontent.com/Pakkamat/stealth_watermark/main/Test/image_rotate/1_wm.png) | Fail |
| 4 | Noise | ![wm_noise](https://raw.githubusercontent.com/Pakkamat/stealth_watermark/main/Test/image_noise/1_wm.png) | 55% |
| 5 | brightness | ![wm_brightness](https://raw.githubusercontent.com/Pakkamat/stealth_watermark/main/Test/image_bright/bright_1.png) | 64% |
| 6 | Add text watermark | ![wm_addtextwm](https://raw.githubusercontent.com/Pakkamat/stealth_watermark/main/Test/image_text/1_wm.png) | 80% |



### Running Speed (CPU Only)
| Image | Method | Encoding | Decoding |
| --- | --- | --- | --- |
| 1920x1080 | dwtDct | 300-350ms | 150ms-200ms |
| 600x600 | dwtDct | 70ms | 60ms |

### Reference
Detail : [https://github.com/shieldmnt/invisible-watermark](https://github.com/shieldmnt/invisible-watermark)

Dataset : [https://www.kaggle.com/datasets/zippyz/cats-and-dogs-breeds-classification-oxford-dataset](https://www.kaggle.com/datasets/zippyz/cats-and-dogs-breeds-classification-oxford-dataset)

# invisible-watermark
[![PyPI](https://img.shields.io/pypi/v/invisible-watermark)](https://pypi.org/project/invisible-watermark/)
[![License](https://img.shields.io/pypi/l/invisible-watermark.svg)](https://github.com/ShieldMnt/invisible-watermark/blob/main/LICENSE)
![Python](https://img.shields.io/badge/python->=3.6-green.svg)
![Platform](https://img.shields.io/badge/platform-%20linux%20-green.svg)
[![Downloads](https://static.pepy.tech/badge/invisible-watermark)](https://pepy.tech/project/invisible-watermark) 

invisible-watermark is a **python** library and command line tool for creating invisible watermark over image (a.k.a. **blink image watermark**, **digital image watermark**). The algorithm doesn't rely on the original image.

**Note that** this library is still experimental and it doesn't support GPU acceleration, carefully deploy it on the production environment. The default method **dwtDCT**(one variant of frequency methods) is ready for on-the-fly embedding, the other methods are too slow on a CPU only environment.


[supported algorithms](https://github.com/ShieldMnt/invisible-watermark#supported-algorithms)
* [Discrete wavelet transform](https://en.wikipedia.org/wiki/Discrete_wavelet_transform) + [Discrete cosine transform](https://en.wikipedia.org/wiki/Discrete_cosine_transform) frequency embedding algorithm variants.

[speed](https://github.com/ShieldMnt/invisible-watermark#running-speed-cpu-only)
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
How To Use
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
3. Run App.py

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


**Watermarked Image**

![wm](https://user-images.githubusercontent.com/1647036/106387712-03c17400-6416-11eb-9490-e5e860b025ad.png)

| Attacks | Image | Freq Method | RivaGan |
| --- | --- | --- | --- |
| JPG Compress | ![wm_jpg](https://user-images.githubusercontent.com/1647036/106387721-0e7c0900-6416-11eb-840c-8eab1cb9d748.jpg) | Pass | Pass |
| Noise | ![wm_noise](https://user-images.githubusercontent.com/1647036/106387874-c90c0b80-6416-11eb-99f3-1716f01f2211.png) | Pass | Pass |
| Brightness | ![wm_darken](https://user-images.githubusercontent.com/1647036/106387718-0cb24580-6416-11eb-83af-7f9e94f13cae.png) | Pass | Pass |
| Overlay | ![wm_overlay](https://user-images.githubusercontent.com/1647036/106387733-13d95380-6416-11eb-8aa4-b3d2acfa8637.png) | Pass | Pass |
| Mask | ![wm_mask_large](https://user-images.githubusercontent.com/1647036/106387726-10de6300-6416-11eb-99c3-4a0f70f99224.png) | Pass | Pass |
| crop 7x5 | ![wm_crop_7x5](https://user-images.githubusercontent.com/1647036/106387713-06bc6480-6416-11eb-8ae0-f64289642450.png) | Fail | Pass |
| Resize 50% | ![wm_resize_half](https://user-images.githubusercontent.com/1647036/106387735-15a31700-6416-11eb-8589-2ffa38df2a9a.png) | Fail | Fail |
| Rotate 30 degress | ![wm_rotate](https://user-images.githubusercontent.com/1647036/106387737-19369e00-6416-11eb-8417-05e53e11b77f.png) | Fail | Fail|



### Running Speed (CPU Only)
| Image | Method | Encoding | Decoding |
| --- | --- | --- | --- |
| 1920x1080 | dwtDct | 300-350ms | 150ms-200ms |
| 600x600 | dwtDct | 70ms | 60ms |

### Reference
Detail : [https://github.com/shieldmnt/invisible-watermark](https://github.com/shieldmnt/invisible-watermark)

Dataset : [https://www.kaggle.com/datasets/zippyz/cats-and-dogs-breeds-classification-oxford-dataset](https://www.kaggle.com/datasets/zippyz/cats-and-dogs-breeds-classification-oxford-dataset)

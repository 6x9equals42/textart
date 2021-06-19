# textart

Render images using text. Given a source text and a reference image, recreate the image using the source text by varying the thickness and color of strokes. Currently only produces grayscale output. 

## Usage

You can run from a command line like:
```
python textart.py path_to_text.txt path_to_image.png
```

Other parameters can be modified (like font, text size, text spacing), but not through command line arguments.

## Examples

A bird made from the text of the wikipedia article on birds: (click to expand, right image is very large)

<img src="https://user-images.githubusercontent.com/25068498/122625360-a3943d00-d059-11eb-9b29-d6a27ce9ee28.jpg" width="400"><img src="https://user-images.githubusercontent.com/25068498/122625363-a7c05a80-d059-11eb-891f-385fdf3963ae.png" width="400">

The famous painting of Shakespeare from the text of Hamlet: (generated image is half the original size due to github upload size limits)

<img src="https://user-images.githubusercontent.com/25068498/122625525-68463e00-d05a-11eb-846a-1d376904e4ee.png" width="400"><img src="https://user-images.githubusercontent.com/25068498/122625560-b1968d80-d05a-11eb-9e01-484464d99020.png" width="400">

import csv
from PIL import Image


def preprocess(imgpath, tRGB, processed_img):
	tR = tRGB
	tG = tRGB
	tB = tRGB
	img = Image.open(imgpath)
	img = img.convert('RGBA')
	# img = img.filter(ImageFilter.SHARPEN)
	pix = img.load()

	# Convert to black and white
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			if pix[x, y][0] < tR or pix[x, y][1] < tG or pix[x, y][2] < tB:
				pix[x, y] = (0, 0, 0, 255)
			else:
				pix[x, y] = (255, 255, 255, 255)

	img.save(processed_img)

def parse_tsv_with_nonzero_confidence(file, confidence):
    with open(file) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        first_list = True
        result_list = []
        for row in rd:
            if first_list:
                first_list = False
                continue
            if len(row) >= 11 and int(row[10]) > 0 and int(row[10]) >= confidence and len(row[11].strip()) > 0:
                entry = {
                    # "level": row[0],
                    # "page_num": row[1],
                    "block_num": row[2],
                    "par_num": row[3],
                    "line_num": row[4],
                    "word_num": row[5],
                    # "left": row[6],
                    # "top": row[7],
                    # "width": row[8],
                    # "height": row[9],
                    "conf": row[10],
                    "text": row[11]
                }
                result_list.append(entry)
    return result_list

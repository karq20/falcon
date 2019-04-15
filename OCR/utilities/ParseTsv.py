import csv

class Entries:
  def __init__(self, level, page_num, block_num, par_num, line_num, word_num, left, top, width, height, conf, text):
    self.level = level
    self.page_num = page_num
    self.block_num = block_num
    self.par_num = par_num
    self.line_num = line_num
    self.word_num = word_num
    self.left = left
    self.top = top
    self.width = width
    self.height = height
    self.conf = conf
    self.text = text

def my_function(fname):
    with open("../aadhar/src/processed_text.tsv") as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        firstline = True
        list = []
        for row in rd:
            if firstline:
                firstline = False
                continue
            if int(row[10]) > fname:
                print[row]
                list.append(Entries(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                    row[10], row[11]))
    return list



list1 = my_function(90)
for entry in list1:
    print(entry.text)
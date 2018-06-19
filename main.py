from PIL import Image, ImageDraw, ImageFont
import csv
import math
import time
import re

class Familia:
    def __init__(self, mGrandparents, fGrandparents, father, mother, child, childAge, childGender):
        self.mGrandparents = mGrandparents
        self.fGrandparents = fGrandparents
        self.father = father
        self.mother = mother
        self.child = child
        self.childAge = childAge
        self.childGender = childGender

def point_to_pixel(a):
  return 1.333334 * a

def half_text(arg):
    return math.ceil((arg/2) - 2)

def common_data(list1, list2):
    result = False
    for x in list1:
        for y in list2:
            if x == y:
                result = True
                return result

    return result

def prepare_array(arg):
    return '\n'.join(arg)

def text_size(arg):
    vec = arg.split('\n')
    return 8.5*len(max(vec))

def familiesArray():
    families = []
    f = open('Doenças Oculares.csv')
    csv_f = csv.reader(f)
    for row in csv_f:
        obj = Familia(row[8].split(';'), row[7].split(';'), row[5].split(';'), row[6].split(';'), row[4].split(';'), row[3], row[9])
        families.append(obj)
    return families

def draw(currentCounter, familia):
    im = Image.new('RGB', (1000, 350), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    FONT_SIZE_PX = point_to_pixel(15)
    font = ImageFont.truetype("cour.ttf", 15)
    #Age
    text_x = 450 - (text_size(familia.childAge+familia.childGender)+3)
    draw.text((text_x, 0), familia.childAge+' - '+familia.childGender, fill=16, font=font)
    # Maternal Grandparents
    fill = 154 if common_data(familia.mGrandparents, familia.mother) else 16
    draw.text((0,0), prepare_array(familia.mGrandparents), fill=fill, font=font, align="center")
    m_grandparents_initial_x = (text_size(prepare_array(familia.mGrandparents))/2)-2
    m_grandparents_initial_y = draw.textsize(prepare_array(familia.mGrandparents))[1]+10
    draw.line((m_grandparents_initial_x, m_grandparents_initial_y, m_grandparents_initial_x, m_grandparents_initial_y+50), fill=fill, width=4)
    # Mother
    mother_fill = 154 if common_data(familia.mother, familia.child) else 16
    draw.text((0, ((draw.textsize(prepare_array(familia.mGrandparents))[1]+10)+50)), prepare_array(familia.mother), fill=mother_fill, font=font, align="center")
    m_initial_x = (text_size(prepare_array(familia.mother))/2)-2
    m_initial_y = (draw.textsize(prepare_array(familia.mGrandparents))[1]+10) + (draw.textsize(prepare_array(familia.mother))[1]+10) + 50
    draw.line((m_initial_x, m_initial_y, m_initial_x, m_initial_y+50), fill=mother_fill, width=4)
    # Paternal Grandparents
    fill = 154 if common_data(familia.fGrandparents, familia.father) else 16
    draw.text(((900)-text_size(prepare_array(familia.fGrandparents)), 0), prepare_array(familia.fGrandparents), fill=fill, font=font, align="center")
    p_grandparents_initial_x = 900 - (text_size(prepare_array(familia.fGrandparents))/2)
    p_grandparents_initial_y = draw.textsize(prepare_array(familia.fGrandparents))[1]+10
    draw.line((p_grandparents_initial_x, p_grandparents_initial_y, p_grandparents_initial_x, p_grandparents_initial_y+50), fill=fill, width=4)
    # Father
    father_fill = 154 if common_data(familia.father, familia.child) else 16
    draw.text(((900)-text_size(prepare_array(familia.father)), (draw.textsize(prepare_array(familia.fGrandparents))[1]+10)+50), prepare_array(familia.father), fill=father_fill, font=font, align="center")
    print(prepare_array(familia.father))
    p_initial_x = 900 - (text_size(prepare_array(familia.father))/2)
    p_initial_y = (draw.textsize(prepare_array(familia.fGrandparents))[1]+10) + (draw.textsize(prepare_array(familia.father))[1]+10) + 50
    draw.line((p_initial_x, p_initial_y, p_initial_x, p_initial_y+50), fill=father_fill, width=4)
    # Culmination Point
    culmination_point = ((m_initial_y+50) + (p_initial_y+50))/2
    draw.line((m_initial_x, m_initial_y+50, 450, culmination_point), fill=mother_fill, width=4)
    draw.line((450, culmination_point, p_initial_x, p_initial_y+50), fill=father_fill, width=4)
    # Child disease
    child_x = 450 - (text_size(prepare_array(familia.child))/2)
    print(prepare_array(familia.child))
    print(prepare_array(familia.child) == "Nenhuma")
    if not (common_data(familia.father, familia.child)) and not (common_data(familia.mother, familia.child)):
        child_fill = "green"
        if prepare_array(familia.child) == "Nenhuma":
            child_fill = "black"
    else:
        child_fill = 154
    draw.text((child_x, culmination_point+60), prepare_array(familia.child), fill=child_fill, font=font, align="center")
    # Child line
    draw.line((450, culmination_point, 450, culmination_point+50), fill=child_fill, width=4)
    # Saves image
    im.save('img/'+str(currentCounter)+'.png')


miopia = {}
astigmatismo = {}
daltonismo = {}
estrabismo = {}
hipermetropia = {}

a = familiesArray()
i=0
start_time = time.time()
for x in a:
    draw(i,x)
    i+=1
print("--- %s seconds ---" % (time.time() - start_time))

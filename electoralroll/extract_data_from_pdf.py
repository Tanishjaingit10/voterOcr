
from pdf2image import convert_from_path
import cv2


import pytesseract
import math
import os
import re

import numpy as np
import fitz

class PdfExtraction:
    def pdf_to_img1(self, pdf_file_path, pdf_in_folder):
        doc = fitz.open(pdf_file_path)
        pdf_to_img_folder = pdf_in_folder + "/images"
        if not os.path.exists(pdf_to_img_folder):
            os.makedirs(pdf_to_img_folder)
        for i in range(len(doc)):
            for img in doc.getPageImageList(i):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:  # this is GRAY or RGB
                    pix.writePNG(f"{pdf_to_img_folder}/page_{i}.png")
                else:  # CMYK: convert to RGB first
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix.writePNG(f"{pdf_to_img_folder}/page_{i}.png")
                    pix1 = None
                pix = None
        return pdf_to_img_folder


    # def pdf_to_img(self, pdf_file_path, pdf_in_folder):
    #     print(pdf_file_path)
    #     images = convert_from_path(pdf_file_path)
    #     pdf_to_img_folder = pdf_in_folder + "/images"
    #     if not os.path.exists(pdf_to_img_folder):
    #         os.makedirs(pdf_to_img_folder)
    #     for i in range(len(images)):
    #         images[i].save(f'{pdf_to_img_folder}/page_{i}.jpg', 'JPEG')

    #     print("--> pdf_to_images done.....................")

    #     return pdf_to_img_folder

    # def img_crop_and_extract_data(self, img_location, assembly_id="", master_temp_list=[]):
    #     # print("-------------", img_location)
    #     file_name = img_location
    #     img = cv2.imread(file_name)
        
    #     temp_list = []
    #     text = pytesseract.image_to_string(img, lang='hin')
    #     data = self.get_data_from_string(text)

    #     if not os.path.exists('media'):
    #         os.makedirs('media')
    #     if not os.path.exists('media/cropped_img'):
    #         os.makedirs('media/cropped_img')
    #     if not os.path.exists('media/sample'):
    #         os.makedirs('media/sample')

    #     cv2.imwrite(f"media/cropped_img/{img_location.split('/')[2].split('.')[0]}_row_{i}_col_{k}.jpg", crop_img)
    #     # print(data)
    #     if data:
    #         data["assembly"] = assembly_id
    #         try:
    #             temp_list.append(data)
    #         except:
    #             pass

    #     master_temp_list.extend(temp_list)
    #     return temp_list

    def extract_data_from_first_page(self,img):
       
        w=img.shape[1]
        part_image=img[:,:math.ceil(w/2)+math.ceil(w/31)]
        part_image=cv2.cvtColor(part_image,cv2.COLOR_BGR2GRAY)
        txt = pytesseract.image_to_string(part_image, lang='hin')
        txt=self.split_and_filter(txt)
        txt = " ".join(txt)
        part_name='-';part_loc='-'
        if txt.find("संख्या एवं नाम")+1 and txt.find("मतदान केंद्र का पता")+1:
            part_name = txt[txt.find("संख्या एवं नाम")+len("संख्या एवं नाम"):txt.find("मतदान केंद्र का पता")]
        if txt.find("मतदान केंद्र का पता")+1 and txt.find("4. मतदाताओं की संख्या")+1:
            part_loc = txt[txt.find("मतदान केंद्र का पता")+len("मतदान केंद्र का पता"):txt.find("4. मतदाताओं की संख्या")]
        idx = part_name.index("-")
        part_name = part_name[idx+1:]
        Part = {"part_name":part_name,"part_location":part_loc,"voter_count":None}
        return Part

    def extract_data_from_image(self, img, serialNo, part_number_id=""):
        
        coord = self.get_cells_coordinate(img)
        coord.sort()
        wholeImageData = []

        # extract anubhag sankhya from page
        anubhagImage = img[ 38:86 , 0:616 ]
        anubhag_text = pytesseract.image_to_string(anubhagImage, lang='hin')
        anubhag_text = self.split_and_filter(anubhag_text)
        anubhag = "-"
        for string in anubhag_text:
            if re.search('अनुभाग',string):
                indx=string.find(":")+1
                if indx:
                    anubhag = string[indx+1:]
                    if anubhag.find('-'):
                        anubhag = anubhag[anubhag.find('-')+1:]
                    break
        
        # iterating over each cell (voter)
        for [y,x,w,h] in coord:
            cropped_image = img[ y:y+h , x:x+w ]
            voterDetails = self.get_voter_details_from_cropped_img(cropped_image)
            voterDetails["anubhag"] = anubhag
            voterDetails["part"] = part_number_id
            voterDetails["Serial_no"] = serialNo[0]
            serialNo[0]+=1
            try:
                wholeImageData.append(voterDetails)
            except:
                pass
        return wholeImageData

    def get_cells_coordinate(self, originalImage):
        # this function code is refrenced from below link (here it gives the coordinate of top left corner of cell and height & width of cell)
        # https://towardsdatascience.com/a-table-detection-cell-recognition-and-text-extraction-algorithm-to-convert-tables-to-excel-files-902edcf289ec

        # convert image to greayscale
        img = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
        # thresholding the image to a binary image
        thresh,img_bin = cv2.threshold(img,128,255,cv2.THRESH_BINARY |cv2.THRESH_OTSU)
        #inverting the image 
        img_bin = 255-img_bin

        # Length(width) of kernel
        kernel_len_ver = np.array(img).shape[1]//30
        kernel_len_hor = np.array(img).shape[1]//10
        # Defining a vertical kernel to detect all vertical lines of image 
        ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len_ver))
        # Defining a horizontal kernel to detect all horizontal lines of image
        hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len_hor, 1))
        # A kernel of 2x2
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            
        #Use vertical kernel to detect and save the vertical lines in a jpg
        image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
        vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
            
        #Use horizontal kernel to detect and save the horizontal lines in a jpg
        image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
        horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)
        
        # Combine horizontal and vertical lines in a new third image, with both having same weight.
        img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
        #Eroding and thesholding the image
        img_vh = cv2.erode(~img_vh, kernel, iterations=2)
        thresh, img_vh = cv2.threshold(img_vh,128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # Detect contours for following box detection
        contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        box = [] # to return
        # Get position (x,y), width and height for every cell
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if ( 368<w and w<378 ) and ( 137<h and h<147 ): # dimentions of voter cell
                x-=4;y-=4;w=379;h=148 # using width:379 and height:148 (as in general cell dimentions in input)
                box.append([y,x,w,h])
            elif ( 368<w and w<378 ) and ( 147<h and h<157 ): # dimentions of Additional voters cell (परिवर्धन सूचि)
                x-=4;y-=4;w=374;h=152 # using width:374 and height:152 (as in general "Additional Voters" cell dimentions in input)
                box.append([y,x,w,h])

        return box


    def get_voter_details_from_cropped_img(self, image):

        data = {} # to return
        IsAdditionalVoter = False # ( परिवर्धन सूचि ) voters at the end of pdf
        if image.shape[0]==152 : IsAdditionalVoter=True
        correction_dict = {"2": "21","3": "31","4": "41","5": "51","6": "61","7": "71","8": "81","9": "91","2।": "21","3।": "31","4।": "41","5।": "51","6।": "61","7।": "71","8।": "81","9।": "91","१9":"19"}

        UIDimage = image[ 0:27 , 91:379 ]
        if IsAdditionalVoter : UIDimage = image[ 0:27 , 175:379 ]
        UIDtext = pytesseract.image_to_string(UIDimage, lang='eng')
        UIDtext = self.split_and_filter(UIDtext)
        for line in UIDtext:
            for string in line.split(' '):
                if len(string)>3:
                    data["UID"] = string

        nameDataImage = image[ 17:145 , 0:270 ]
        if IsAdditionalVoter : nameDataImage = image[ 32:142 , 0:270 ]
        nameDataText = pytesseract.image_to_string(nameDataImage, lang='hin')
        nameDataText = self.split_and_filter(nameDataText)
        for string in nameDataText:
            if re.search("पिता",string):
                indx = string.find(":")+1 # returns 0 if not found
                if indx:
                    asd = string[ indx: ].strip()
                    data["father_name"] = asd
            elif re.search("पति",string):
                indx = string.find(":")+1
                if indx:
                    asd = string[ indx: ].strip()
                    data["husband_name"] = asd
            elif re.search("नाम",string):
                indx = string.find(":")+1
                if indx:
                    asd = string[ indx: ].strip()
                    data["name"] = asd
            elif re.search("मकान",string):
                indx = string.find(":")+1
                if indx:
                    asd = string[ string.find(":")+1: ].strip().split(' ')[0]
                    asd = asd.replace("॥","1")
                    data["house_no"] = asd
            elif re.search("आयु",string):
                if string.find("लिंग") == -1:
                    data["father_name"]=data["husband_name"]=data["house_no"]=data["age"]="DELETED"
                    return data
                indx = string.find(":")+1
                if indx:
                    asd = string[ indx: string.find("लिंग")].strip()
                    asd = asd.replace("॥","1");
                    if correction_dict.get(asd) == None :
                        data["age"] = asd
                    else:
                        data["age"] = correction_dict.get(asd)
        return data
        
    def split_and_filter(self,string):
            string = string.split("\n")
            for item in string[:]:
                if item == "":
                    string.remove("")
                if item == " ":
                    string.remove(" ")
            return string

    # def extractText(self, img, lang=None):
    #     if(lang):
    #         text = pytesseract.image_to_string(img, lang)
    #     else:
    #         text = pytesseract.image_to_string(img)
    #     text = text.split("\n")
    #     for item in text[:]:
    #         if item == "":
    #             text.remove("")
    #     return text


    # def get_user_name(self, str_t):
    #     str_t = str_t.split(":")
    #     user_name = ""
    #     if str_t.__len__() == 2:
    #         user_name = str_t[1].strip()
    #     return user_name

    # def get_data_from_string(self, text):
    #     text = text.split("\n")
    #     for item in text[:]:
    #         if item == "":
    #             text.remove("")

    #     name = ""
    #     age = ""
    #     father_name = ""
    #     husband_name = ""
    #     house_no = ""
    #     gender = ""
    #     temp_dict = {}
    #     for o in text:
    #         if re.search("नाम :", o) and not (re.search("पति का नाम :", o) or re.search("पिता का नाम :", o)):
    #             asd = o.split("नाम :")
    #             temp_dict["name"] = asd[1].strip()
    #         if re.search("पिता का नाम :", o):
    #             asd = o.split("पिता का नाम :")
    #             temp_dict["father_name"] = asd[1].strip()
    #             if "name" not in temp_dict.keys() and text.index(o) != 0:
    #                 temp_dict["name"] = self.get_user_name(text[text.index(o) - 1])

    #         if re.search("पति का नाम :", o):
    #             asd = o.split("पति का नाम :")
    #             temp_dict["husband_name"] = asd[1].strip()
    #             if "name" not in temp_dict.keys() and text.index(o) != 0:
    #                 temp_dict["name"] = self.get_user_name(text[text.index(o) - 1])

    #         if re.search("आयु :", o) or re.search("आयु:", o):
    #             asd = ""
    #             if re.search("आयु :", o):
    #                 asd = o.split("आयु :")
    #             else:
    #                 asd = o.split("आयु:")

    #             if re.search("लिंग:", asd[1]) or re.search("लिंग :", asd[1]):
    #                 if re.search("लिंग:", asd[1]):
    #                     asdd = asd[1].split("लिंग:")
    #                 else:
    #                     asdd = asd[1].split("लिंग :")
    #                 temp_dict["age"] = asdd[0].strip()
    #             if re.search("स्त्री", asdd[1]):
    #                 temp_dict["gender"] = "स्त्री"
    #             elif re.search("पुरुष", asdd[1]):
    #                 temp_dict["gender"] = "पुरुष"
    #         if re.search("मकान संख्या:", o):
    #             temp_dict["house_no"] = o.split("मकान संख्या:")[1].split(' ')[1]

    #     return temp_dict


# from django.test import TestCase
#
# # Create your tests here.
#
# a = """
#
#         नाम : सुगनाई
#         पति का नाम : गेपरराम
#         मकान संख्या: 262 शाणं० 8
#         आयु : 59 लिंग: स्त्री #ैएक800७
#
#         """
#
# a = """
# उमः +! : पुष्पा
#
# पिता का नाम : जितेन्द्र
# मकान संख्या: 83 शिण०8
# आयु : 33 लिंग: स्त्री #४80।॥9
#
# """
# """
# जा | : चन्द्रकान्ता
#
# पति का नाम : कमलेश
# मकान संख्या: 83 शाण० 8
# आयु : 27 लिंग: स्त्री #४80॥9
#
# '३().])376943
#
# """
#
# """
# >>ीस्‍ि.) : सुगरी
#
# पति का नाम : जमालखां
# मकान संख्या: 8 शाण० 8
# आयु : 79 लिंग: स्त्री 0]
#
#
#
#
# """
# a = """
# दम. िड| : नीतू
#
# पिता का नाम : पुसाराम
# मकान संख्या: 322 शिीणं0 8
# आयु : 20 लिंग: पुरुष #एकॉ8009
#
#
#
#
#
# """
# import re
# a = a.split("\n")
#
# name = ""
# age = ""
# father_name = ""
# husband_name = ""
# gender = ""
# print(a)
# for item in a[:]:
#     if item=="":
#         a.remove("")
# print(a)
# def get_user_name(str_t, name):
#     str_t = str_t.split(":")
#     if str_t.__len__()==2:
#         name = str_t[1].strip()
#     print(name)
#     return name
# for o in a:
#     if re.search("नाम :", o) and not (re.search("पति का नाम :", o) or re.search("पिता का नाम :", o)):
#         asd = o.split("नाम :")
#         name = asd[1].strip()
#     if re.search("पिता का नाम :", o):
#         asd = o.split("पिता का नाम :")
#         father_name = asd[1].strip()
#         if not name and a.index(o) != 0:
#             name = get_user_name(a[a.index(o)-1], name)
#
#     if re.search("पति का नाम :", o):
#         asd = o.split("पति का नाम :")
#         husband_name = asd[1].strip()
#         if not name and a.index(o) != 0:
#             name = get_user_name(a[a.index(o)-1], name)
#
#     if re.search("आयु :", o) or re.search("आयु:", o):
#         asdd = ["", ""]
#         asd = ""
#         if re.search("आयु :", o):
#             asd = o.split("आयु :")
#         else:
#             asd = o.split("आयु:")
#
#         if re.search("लिंग:", asd[1]) or re.search("लिंग :", asd[1]):
#             if re.search("लिंग:", asd[1]):
#                 asdd = asd[1].split("लिंग:")
#             else:
#                 asdd = asd[1].split("लिंग :")
#             age = asdd[0]
#         if re.search("स्त्री", asdd[1]):
#             gender = "स्त्री"
#         elif re.search("पुरुष", asdd[1]):
#             gender = "पुरुष"
#
# print(name, father_name, husband_name, age, gender)
# print("---")

import multiprocessing


def worker(procnum, return_li):
    print(str(procnum) + " represent!")
    # return_dict[procnum] = procnum
    return_li.extend([1])
    return {"ok"}


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    return_li = manager.list()
    li = []
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i, return_li))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()
    print(return_li)
    print(li)
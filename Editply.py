import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '~/PycharmProjects/morse/')
import random
import  Functions as f

filename = 'monkey'
comparingValue=2
workWithColor= True
colorPosition=0
readX=False
file = open ("/home/yaser/Desktop/"+filename+".ply",'r')
toWrite = open("/home/yaser/Desktop/rr_edited.ply",'w')
toWrite2 = open("/home/yaser/Desktop/rrrrr_edited.ply",'w')
numberOfVertices=0
beginVertex=0

faces={}

indicesWithZAxis = []

scalingValue=200
count = 1
colors= "property uchar red\nproperty uchar green\nproperty uchar blue\n"
a = True
lines3=[]
for line in file:
    lines3.append(line)
    beginVertex+=1
    l = line.split()
    if l[0] == 'element' and l[1]=='vertex':
        numberOfVertices= int(l[2])
    if readX:
        if len(word) > 2:
            if word[2] == 'red':
                readX=False
            else:
                colorPosition += 1
    toWrite.write(line)
    toWrite2.write(line)
    word = line.split()
    if len(word)>2:
        if word[2]=='x':
            readX=True

    if word[0] == 'end_header':
        break
# color the points
print("colorposition: {}".format(colorPosition))

indices =[]
c = 0
x,y ,z = [],[],[]

points = []
lines =[]
lines2 =[]
lines4=[]
lines5=[]
polygons ={}
count = 0


for line in file:
    lines.append(line)
    lines2.append(line)
    word = line.split()
    if (len(word) == 4):
        word1,word2,word3 = int(word[1]),int(word[2]),int(word[3])
        lines5.append(line)
        # value1, value2, value3 = polygons[word1]['value'],polygons[word2]['value'],polygons[word3]['value']
        first = polygons[word1]
        second = polygons[word2]
        third = polygons[word3]
        value1, value2, value3=first['value'],second['value'],third['value']
        if value1 > value2:
            first["edges"].add(((word1,word2),value2))

        else:
            second["edges"].add(((word2,word1),value1))

        if value1 > value3:
            first['edges'].add(((word1,word3),value3))
        else:
            third['edges'].add(((word3, word1), value1))
        if value2 > value3:
            second['edges'].add(((word2, word3), value3))
        else:
            third['edges'].add(((word3, word2), value2))

        x,y,z = [value1,value2,value3],[first,second,third],[word1,word2,word3]
        # print(" 0hh {} - {} ".format(x, z))
        v2,v0 = max(x),min(x)
        v1 = [i for i in x if (i != v2 and i != v0)][0]

        indx0,indx1,indx2= x.index(v0),x.index(v1),x.index(v2)
        # print("v0: {}, v1: {},v2: {},indx0: {},indx1: {},indx2: {}".format(v0,v1,v2,indx0,indx1,indx2))

        y[indx2]["triangles"].append([(z[indx2],z[indx1],z[indx0]),v1+v0])
        count += 1
    else:
        lines4.append(line)
        if len(word) >1:
            distinguished_filtration = ['0' for i in range(11)]
            s = str(count)
            for i in range(len(s)):
                distinguished_filtration[i] = s[i]
            distinguished_filtration = "".join(distinguished_filtration)
            r, g, b = word[colorPosition], word[colorPosition + 1], word[colorPosition + 2]
            gray = 0.21 * int(r) + 0.72 * int(g) + 0.07 * int(b)
            gray = "{:.2f}".format(gray)
            if len(word) > 0:
                if workWithColor:
                    word2 = str(gray) + distinguished_filtration
                else:
                    word2 = "{:.7f}".format(float(word[comparingValue]) + scalingValue) + distinguished_filtration

                # print(word2)
                r = word2.find('.')
                if not word2.startswith("-"):
                    if r == 1:
                        word2 = "00" + word2
                    elif r == 2:
                        word2 = "0" + word2
                    elif r == 3:
                        pass
                    else:
                        print(word2)
                        raise Exception("Index of dot can't be other")
                else:
                    print("why")
                    if r == 2:
                        word2 = word2[:1] + "00" + word2[1:]
                    elif r == 3:
                        word2 = word2[:1] + "0" + word2[1:]
                    elif r == 4:
                        pass
                    else:
                        raise Exception("Index of dot can't be other")
                polygons[count] = {"value": word2, "edges": set(), "triangles": []}
                count += 1
            else:
                print("len word: {}".format(word))




# c = 0
# for i in polygons:
#     c += 1
#     if c > 20:
#         break
#     print(polygons[i])
# c=0
# for i in polygons:
#     if len(polygons[i]['edges']) is 0:
#         c+=1
# print(c)
critical_cells = []
discrete_vector_field = {}



count = 0
while len (polygons) > 0:
    p = polygons[count]
    PQZero = p['edges']
    if not PQZero:
        critical_cells.append(count)
    else:
        local_paired_and_critical_cells=[]
        second_cells = p['triangles']
        PQZero = sorted(PQZero, key=lambda x:x[1])
        delta = PQZero.pop(0)
        discrete_vector_field[count] = delta[0]
        local_paired_and_critical_cells.append(delta[0])
        PQOne = []
        for triangle in second_cells:
            if delta[0][1] in triangle[0]:
                PQOne.append(triangle)
        PQOne.sort(key=lambda x:x[1])
        while PQZero or PQOne:
            while PQOne:

                alpha = PQOne.pop(0)
                num_unpaired, pair_alpha = f.num_unpaired_faces(alpha[0],local_paired_and_critical_cells)
                if num_unpaired == 0:
                    PQZero.append(alpha)
                    PQZero = sorted(PQZero, key=lambda x: x[1])
                else:
                    discrete_vector_field[pair_alpha]= alpha[0]

                    local_paired_and_critical_cells.append(alpha[0])
                    local_paired_and_critical_cells.append(pair_alpha)
                    for i in PQZero:
                        if i[0] == pair_alpha:
                            PQZero.remove(i)
                    for triangle in second_cells:
                        if pair_alpha[1] in triangle[0] :
                            num, pairs = f.num_unpaired_faces(triangle[0], local_paired_and_critical_cells)
                            if num == 1:
                                PQOne.append(triangle)
                    PQOne.sort(key=lambda x:x[1])

            if PQZero:
                gamma = PQZero.pop(0)
                critical_cells.append(gamma[0])
                local_paired_and_critical_cells.append(gamma[0])
                for triangle in second_cells:
                    if gamma[0][1] in triangle[0]:
                        num, pair = f.num_unpaired_faces(triangle[0], local_paired_and_critical_cells)
                        if num == 1:
                            PQOne.append(triangle)
                            second_cells.remove(triangle)
                        PQOne.sort(key=lambda x: x[1])
    del polygons[count]
    count += 1








# print("critical cells: {}".format(critical_cells))
print("length of critical cells is : {}".format(len(critical_cells)))
# print ("discrete vector field: {}".format(discrete_vector_field))
criticalColors ={}
for i in critical_cells:
    if isinstance(i,int):
        lines[i] = f.color(lines[i],'red',colorPosition)
        ## save the color of critical points in a dictionary to make the interpolation of easy
        ## use a for loop instead of list comprehension because it is more accurate
        # l = lines2[i].split()
        # s,a =[],0
        # for j in l:
        #     if a>2 and a <6:
        #         s.append(int(j))
        #     a +=1
        #
        # criticalColors[i]=s

    else:
        ## find the average of colors in critical points of dimension higher than 1 and assign the vertices the same average color
        # rgblist =[]
        # for j in i:
        #     l = lines2[j].split()
        #     s, a = [], 0
        #     for j in l:
        #         if a >= colorPosition and a < colorPosition+3\
        #                 :
        #             s.append(int(j))
        #         rgblist.append(s)
        #         a += 1
        # rgbdic={'r':[],'g':[],'b':[]}
        # for j in rgblist:
        #     rgbdic['r'].append(j[0])
        #     rgbdic['g'].append(j[1])
        #     rgbdic['b'].append(j[2])
        # l=[]
        # for j in rgbdic:
        #     l.append(int(sum(rgbdic[j])/len(rgbdic[j])))
        # for j in i:
        #     criticalColors[j]= l

        ## color the critical points the 2-critical cell is green the 3-critical cell is blue
        if len(i) == 2:
            lines[i[0]] = f.color(lines[i[0]],'green',colorPosition)
            lines[i[1]] = f.color(lines[i[1]],'green',colorPosition)
            # lines4[i[0]] = f.color(lines[i[0]], 'green', colorPosition)
            # lines4[i[1]] = f.color(lines[i[1]], 'green', colorPosition)
        else:
            for x in i:
                lines[x] = f.color(lines[x],'blue',colorPosition)
                # lines4[x] = f.color(lines[x], 'blue', colorPosition)
a = set()
for i in discrete_vector_field:
    if isinstance(i,int):
        a.add(i)
    else:
        for j in i :
            a.add(j)
# for i in a:
#     lines[i] = color(lines[i], 'white')

# print("critical cells: {}".format(critical_cells))
# (discrete_vector_field)
# print ("critical cells are: {}".format(critical_cells))
# print("vector field is: {}".format(discrete_vector_field))
#############################################


for line in lines:
    toWrite.write(line)
toWrite.close()
# for i in criticalColors:
#     lines2[i]=f.changeColorinLines(lines2[i],criticalColors[i])


# for i in range(0,numberOfVertices):
#     if i not in criticalColors:
#        lines2[i]= f.changeColorinLines(lines2[i],[255,255,255])

keys = discrete_vector_field.keys()

#
# h = f.homology(discrete_vector_field, critical_cells,criticalColors)[2]
#
# # count=0
# for i in h:
#     if h[i][0]=='notcritical' and len(h[i]) >1:
#         color = f.interpolateColor(h[i])
#         lines2[i]=f.changeColorinLines(lines2[i],color)

#
#
# for i in h:
#     if len(h[i])==1:
#         count+=1
# print("count: {}".format(count))
# v, f= f.morseComplex(discrete_vector_field,critical_cells,lines2)
f, fc = f.homology(discrete_vector_field,critical_cells)

toWrite3 = open("/home/yaser/Desktop/MorseComplex_edited.ply",'w')
v = set()
count={}
for i in fc:
    for j in i:
        v.add(j)
        count[j]= lines4[j]


for i in range(len(lines3)):
    if lines3[i].find("element vertex")>-1:
        lines3[i]= "element vertex "+str(len(v))+" \n"

        # lines3[i]= "element vertex "+str(len(v))+" \n"
    elif lines3[i].find("element face")>-1:
        # lines3[i] = "element face " + str(len(f)) + " \n"

        lines3[i] = "element face " + str(len(fc)) + " \n"

    toWrite3.write(lines3[i])
hh={}
h =0

print("we are first here")
for i in v:
    toWrite3.write(count[i])
    hh[count[i]]=h
    h+=1
faces =""
print("we are here")
for i in fc:
    l=[]
    for j in i:
        l.append(hh[count[j]])
    s = str(len(i)) + " "
    for j in l:
        s += str(j) + " "
    s += "\n"
    toWrite3.write(s)

toWrite3.close()
for line in lines2:
    toWrite2.write(line)
toWrite.close()
toWrite4 = open("/home/yaser/Desktop/rrrrrCritical_edited.ply",'w')
v = set()
for i in critical_cells:
    if isinstance(i,int):
        v.add(i)
    else:
        for j in i:
            v.add(j)

for i in range(len(lines3)):
    if lines3[i].find("element vertex")>-1:
        lines3[i]= "element vertex "+str(len(v))+" \n"

        # lines3[i]= "element vertex "+str(len(v))+" \n"
    elif lines3[i].find("element face")>-1:
        toWrite4.write("end_header \n")
        break
    toWrite4.write(lines3[i])
for i in v:
    toWrite4.write(lines4[i])
toWrite4.close()
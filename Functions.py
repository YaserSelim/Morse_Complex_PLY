def color(p,c,colorPosition):
    s = p.split()
    l=""
    i=0
    while i < len(s):
        if i <colorPosition or i >=colorPosition+3:
            l+=s[i]+" "
            i+=1
        else:
            if c == 'red':
                l += "255 0 0 "
                # l += "0 255 255 "
            elif c == 'green':
                l+= '0 255 0 '
            elif c == 'blue':
                l+= '0  0 255 '
            elif c== 'white':
                l+='255 255 255 '
            else:
                print("color must be entered as parameter")
            i +=3
    return l+" \n"

def create_2Cells(p0,p1,p2,v0,v1,v2):
    triangles = []
    count =0
    x = max(v0,v1,v2)
    p4=0
    if v1>v2:
        p4=2

    return triangles



def convert_RGB_to_gray(r,g,b):
    return r * 0.2126 + g * 0.7152 + b * 0.0722



def num_unpaired_faces(alpha,local_paired_and_critical_cells):
    count = 0
    pair =None
    if (alpha[0],alpha[1]) not in local_paired_and_critical_cells:
        pair = (alpha[0],alpha[1])
        count +=1
        if (count,alpha[1]) in local_paired_and_critical_cells:
            print("no more than one edge is allowed to be paired in the same lower star")
    else:
        if (alpha[0],alpha[2]) not in local_paired_and_critical_cells:
            pair = (alpha[0],alpha[2])
            count +=1
        # else:
        #     count =2
    return count, pair


def changeColorinLines(lin, l):
    s = [str(x) for x in l]
    l = lin.split()
    for i in range(len(s)):
        l[i + 3] = s[i]
    lin = ' '.join(l)
    return lin+"\n"


def getColorFromLine(l):
    l = l.split()
    s, a = [], 0
    for j in l:
        if a > 2 and a < 6:
            s.append(int(j))
        a += 1
    return s

def interpolateColor (x):
    x.pop(0)
    l=[]
    for i in x:
        t = i[0]/i[1]
        color = [int(i[2][0]+(i[3][0]-i[2][0])*t),int(i[2][1]+(i[3][1]-i[2][1])*t),int(i[2][2]+(i[3][2]-i[2][2])*t)]
        l.append(color)
    r,g,b=[],[],[]
    ln =len(l)
    for i in l:
        r.append(i[0])
        g.append(i[1])
        b.append(i[2])
    return [int(sum(r)/ln), int(sum(g)/ln),int(sum(b)/ln)]




def homology (v, C):
    keys = v.keys()
    values = v.values()
    m=[]
    Qbfs =[]
    facelist ={}
    tr ,sq = [],[]
    k={}
    for i in C:
        k[i]= "critical"

    for i in keys:
        k[i]='key'
    for i in values:
        k[i]='value'

    for c in C:
        # if count % 100 ==0:
        #     print("count: {}".format(count))
        if not isinstance(c,int):
            if len (c)==2:
                s=k[c[0]]
                if s=='key':
                    Qbfs.append(c[0])

                s = k[c[1]]
                if s=='key':
                    Qbfs.append(c[1])
            elif len (c)==3:
                s = k[(c[0],c[1])]
                if s=='key':
                    Qbfs.append((c[0],c[1]))

                s = k[(c[1], c[2])]
                if s=='key':
                    Qbfs.append((c[1], c[2]))

                s = k[(c[0], c[2])]
                if s=='key':
                    Qbfs.append((c[0], c[2]))
            if len(Qbfs) == 0:
                print("jiiii")

            while len(Qbfs) > 0:
                alpha = Qbfs.pop(0)
                beta = v[alpha]
                if len (beta)==2:
                    for sigma in beta:

                        if sigma != alpha:
                            s = k[sigma]
                            if s=='critical':
                                try:
                                    facelist[c].add(sigma)
                                    tr.append((sigma, beta[0],beta[1]))
                                except:
                                    facelist[c]= [sigma]
                                    tr.append((sigma, beta[0],beta[1]))

                            elif s=='key':
                                Qbfs.append(sigma)

                else:
                    f = [(beta[0],beta[1]),(beta[0],beta[2]),(beta[1],beta[2])]
                    for sigma in f:
                        if sigma != alpha:
                            s = k[sigma]
                            if s=='critical':
                                try:
                                    facelist[c].append(sigma)
                                    sq.append((sigma[0],sigma[1], beta[0], beta[1],beta[2]))
                                except:
                                    facelist[c] = [sigma]
                                    sq.append((sigma[0],sigma[1], beta[0], beta[1],beta[2]))


                            elif s=='key':
                                Qbfs.append(sigma)
    faces = []
    faces.extend(tr)
    faces.extend(sq)


    return facelist, faces



def morseComplex (v, C,lines):
    keys = v.keys()
    values = v.values()
    m=[]
    Qbfs =[]
    facelist ={}
    facelist2={}
    pointsColors={}
    k={}
    for i in C:
        k[i]= "critical"
        if isinstance(i,int):
            pointsColors[i] = ['critical']
        else:
            for j in i:
                pointsColors[j]=['critical']

    for i in keys:
        k[i]='key'
        if isinstance(i,int):
            pointsColors[i] = ['notcritical']
        else:
            for j in i:
                pointsColors[j]=['notcritical']
    for i in values:
        k[i]='value'
        if isinstance(i,int):
            pointsColors[i] = ['notcritical']
        else:
            for j in i:
                pointsColors[j]=['notcritical']
    verticies = set()
    faces = set()
    for c in C:
        if not isinstance(c, int):
            faces.add(c)
            for i in c:
                verticies.add(i)
    #



    return verticies, faces


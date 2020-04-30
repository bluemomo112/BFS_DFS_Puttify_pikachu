import msmc
mc=msmc.Connect(address="47.105.46.254")
mc=msmc.Connect(address="47.105.46.254")
name="momo"



def BFS(sx,sy,sz,tar_color=6):
    '''
    1、把起始点加入que，当que不为空的时候，从que中取出点p，染色
    2、把p的4周点都计算出来，并且进行检测，
    如果不为黑色（也就是皮卡丘的边缘），
    且不为ori和tar颜色，那么加入que
    3、当que为0时，则return
    '''
    ori_color=mc.getColor(sx,sy,sz)
    que=[(sx,sy,sz)]

    if ori_color==tar_color:
        return "fini"

    while len(que)>0:
        p=que.pop(0)
        print("现在正在处理{},等待处理队列为：{}".format(str(p),str(que)))
        mc.setBlock(p[0],p[1],p[2],35,tar_color)
        visit_point.append(p)
        sourding=[(p[0],p[1],p[2]+1),(p[0],p[1]+1,p[2]),(p[0],p[1],p[2]-1),(p[0],p[1]-1,p[2])]
        for s in sourding:
            if mc.getBlock(s[0], s[1], s[2])!=35 or s in visit_point:
                print("碰到边缘或，曾经遍历过的",s in visit_point)
                continue
            else:
                color=mc.getColor(s[0], s[1], s[2])
                if color!=15 and color!=tar_color and color==ori_color:
                    que.append(s)
    return 'fini'

def detect_startpoint():
    while True:
        hit_events = mc.hitEvents()

        if hit_events:
            print(str(hit_events[0]).split(","))
            x,y,z=str(hit_events[0]).split(",")[1:4]
            b=str(hit_events[0]).split(",")[5]

            x=int(x)
            y=int(y)
            z=int(z)
            break
    return x,y,z

def DFS(sx,sy,sz,ori_color=11,tar_color=6):
    '''
    1、使用递归：先检测自己，如果为黑色，或者是target颜色，return
    2、然后顺序前往，递归调用自己
    '''
    print("方块id",str((sx,sy,sz)),"方块：",mc.getBlock(sx, sy, sy),mc.getColor(sx, sy, sz))
    if mc.getColor(sx, sy, sz)==tar_color or mc.getColor(sx, sy, sz)==15 or (sx,sy,sz) in visit_point:
        print("遇到黑色边缘了","该点已经访问过了",(sx,sy,sz) in visit_point)
        return "fnni"
    else:
        if mc.getColor(sx, sy, sz)==ori_color:
            print("替换",sx, sy, sz)
            visit_point.append((sx,sy,sz))
            mc.setBlock(sx, sy, sz, 35, tar_color)
            DFS(sx,sy,sz + 1)
            DFS(sx, sy + 1, sz)
            DFS(sx, sy, sz - 1)
            DFS(sx, sy - 1, sz)
        return "fini"


#建造pikaqiu
mc.buildPixelArt("whale.csv", name)
visit_point=[]

x,y,z=detect_startpoint()
print('开始深度优先渲染')
DFS(x,y,z)
print("fini")


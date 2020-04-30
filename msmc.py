# -*- coding: utf-8 -*-
# @Time    : 2019-07-19 18:30
# @Author  : JeremyTsui
# @Software: PyCharm
"""
版本说明：
目前包含Connect和AIturtle这2个常用的类
Connect类里有常用的传送，建造，运动方块等函数
AITurtle类继承自mcpi.MinecraftTurtle，扩展了goto等函数

这个库目前是教师使用的版本
对建造立方体和球体没有做大小对限制
setPos函数y传送做了限制0-255可以使用，超出的都算作256
"""

import sys
import os
import logging
import text
import fonts
# import time
# import requests
import random
import mcpi.minecraftstuff as minecraftstuff
from mcpi import vec3, minecraft
from mcpi.minecraftstuff import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')  # %a, %d %b %Y %H:%M:%S
# <-----试听课专用以下
address = "101.200.42.193"
port = 4711
vec = vec3.Vec3()
mc = minecraft.Minecraft.create(address, port)
mcDrawing = minecraftstuff.MinecraftDrawing(mc)


def get_csv_size(filename):
    """
    读取csv文件的行数和列数
    :param filename:
    :return:
    """
    with open(sys.path[0] + '/' + 'csvFiles' + '/' + filename, mode='r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    sizex = 1
    sizey = len(lines)
    sizez = len(lines[0].split(","))
    return sizex, sizey, sizez


def buildArt(filename, player_name, air=False, t=0):
    """
    Build a pixel art below the player's position
    活动课专用函数，让学生在csv文件里设计自己的像素画
        csv里的数字代表的颜色：
            1-red
            2-green
            3-blue
            4-yellow
            5-purple
            6-white
            7-black
            8-orange
            9-pink
            0-gray
    :param string filename: .csv
    :param string playername: player's name
    :param bool air:  show the pixel art or not
    """
    player_id = mc.getPlayerEntityId(player_name)
    pos = mc.entity.getTilePos(player_id)
    with open(sys.path[0] + '/' + 'csvFiles' + '/' + filename, mode='r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    # coords = lines[0].split(",")
    sizex = get_csv_size(filename)[0]
    sizey = get_csv_size(filename)[1]
    sizez = get_csv_size(filename)[2]
    lineidx = 0
    for y in range(sizey):
        # lineidx = lineidx + 1 # 取消csv每行之间的空行
        for x in range(sizex):
            line = lines[lineidx]
            lineidx = lineidx + 1
            data = line.split(",")
            for z in range(sizez):
                try:
                    d = int(data[z])
                    if air:
                        blockID = 0
                        blockstyle = 0
                    else:
                        blockID = 35
                        if d == 1:
                            blockstyle = 14  # red
                        elif d == 2:
                            blockstyle = 13  # green
                        elif d == 3:
                            blockstyle = 11  # blue
                        elif d == 4:
                            blockstyle = 4  # yellow
                        elif d == 5:
                            blockstyle = 10  # purple
                        elif d == 6:
                            blockstyle = 0  # white
                        elif d == 7:
                            blockstyle = 15  # black
                        elif d == 8:
                            blockstyle = 1  # orange
                        elif d == 9:
                            blockstyle = 6  # pink
                        elif d == 0:
                            blockstyle = 7  # gray
                except:
                    blockID = 0
                    blockstyle = 0
                time.sleep(t)
                mc.setBlock(pos.x + x, pos.y - y, pos.z + z, blockID, blockstyle)
    logging.info('buildArt: {}'.format(filename))


def transferTo3d(strArt=""):
    piclist = strArt.split("\n")
    piclist.reverse()
    pic = []
    for i in piclist:
        if i:
            a = [j for j in i]
            pic.append(a)
    return pic


def buildMaze(strArt="", playername="", height=1, blockID=35, style=0, t=0):
    """
    根据字符画，在我的世界绘制迷宫
    :param strArt: 迷宫字符画
    :param playername: 玩家名
    :param height: 迷宫高度
    :param blockID: 迷宫方块材质
    :param style: 迷宫方块样式/颜色
    :param t: 建造时间间隔
    """
    pos = mc.entity.getPos(mc.getPlayerEntityId(playername))
    x, y, z = pos.x, pos.y, pos.z
    for i in range(height):
        buildArt3dByXYZHorizontal(strArt, x, y, z, blockID, t)
        y += 1
    logging.info('buildMaze')


def buildArt3d(strArt="", playername="", width=1, blockID=35, t=0):
    """
    根据字符画，在我的世界绘制垂直于地面的像素图
    :param strArt: 字符画
    :param playername: 玩家名
    :param width: 像素画厚度
    :param blockID: 像素画方块材质
    :param style: 像素画方块样式/颜色
    :param t: 建造时间间隔
    """
    pos = mc.entity.getPos(mc.getPlayerEntityId(playername))
    x, y, z = pos.x, pos.y, pos.z
    for i in range(width):
        buildArt3dByXYZVertical(strArt, x, y, z, blockID, t)
        x += 1
    logging.info('buildArt3d')


def buildArt3dByXYZHorizontal(strArt="", x=0, y=0, z=0, blockID=35, t=0):
    pic = transferTo3d(strArt)
    for i in pic:
        newz = z
        for j in i:
            if j == "w":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 0)
                newz -= 1
            elif j == "r":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 14)
                newz -= 1
            elif j == "g":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 13)
                newz -= 1
            elif j == "b":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 11)
                newz -= 1
            elif j == "y":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 4)
                newz -= 1
            elif j == "o":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 1)
                newz -= 1
            elif j == "k":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 15)
                newz -= 1
            elif j == "p":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 10)
                newz -= 1
            else:
                newz -= 1
        x -= 1


def buildArt3dByXYZVertical(strArt="", x=0, y=0, z=0, blockID=35, t=0):
    """
    在指定的坐标位置生成像素画
    :param strArt: 字符画变量
    :param x:
    :param y:
    :param z:
    :param blockID: 方块编号
    :param t: 建造间隔时间
    :return:
    """
    pic = transferTo3d(strArt)
    for i in pic:
        newz = z
        for j in i:
            if j == "w":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 0)
                newz -= 1
            elif j == "r":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 14)
                newz -= 1
            elif j == "g":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 13)
                newz -= 1
            elif j == "b":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 11)
                newz -= 1
            elif j == "y":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 4)
                newz -= 1
            elif j == "o":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 1)
                newz -= 1
            elif j == "k":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 15)
                newz -= 1
            elif j == "p":
                time.sleep(t)
                mc.setBlock(x, y, newz + 1, blockID, 10)
                newz -= 1
            else:
                newz -= 1
        y += 1


def buildPixelArt(filename, player_name, air=False, t=0):
    """
    Build a pixel art below the player's position

    :param string filename: .csv
    :param string playername: player's name
    :param bool air:  show the pixel art or not
    """
    player_id = mc.getPlayerEntityId(player_name)
    pos = mc.entity.getTilePos(player_id)
    with open(sys.path[0] + '/' + 'csvFiles' + '/' + filename, mode='r', encoding='utf-8-sig') as f:
        lines = f.readlines()
    coords = lines[0].split(",")
    sizex = int(coords[0])
    sizey = int(coords[1])
    sizez = int(coords[2])

    lineidx = 1

    for y in range(sizey):
        lineidx = lineidx + 1
        for x in range(sizex):
            line = lines[lineidx]
            lineidx = lineidx + 1
            data = line.split(",")
            for z in range(sizez):
                try:
                    d = int(data[z])
                    if air:
                        blockID = 0
                        blockstyle = 0
                    else:
                        blockID = d // 100
                        blockstyle = d % 100
                except:
                    blockID = 0
                    blockstyle = 0
                time.sleep(t)
                mc.setBlock(pos.x + x, pos.y - y, pos.z + z, blockID, blockstyle)
    logging.info('buildPixelArt: {}'.format(filename))


def say(*args):
    """
    Post a message to the game chat

    :param str msg: message to post
    """
    msg = ""
    for i in args:
        msg += str(i)
    gfw = DFAFilter()
    path = "sensitive_words.txt"
    gfw.parse(path)
    filtered_msg = gfw.filter(msg)
    mc.postToChat(filtered_msg)
    logging.info('You post message to the game: {}'.format(filtered_msg))


# 试听课专用代码以上 ----->
errart = '''
             ,-.
            /   `.
,--_.       \     \\
\    `-_     `.    \\
 ^-_    `.     `.   \\
    `.    `.     `.  \\ 
      `.    `.     \  \\
        `.    `-___/   |
          `.           '--.
            \      ,--.--.'
             \    |*  |* | 
              \    `--' --.
              |         --'\\
              |   .~T--____/
              /   `~|_/\_/
            ,'       |
          ,'     .--.|
        ,'  ,-   |   |
       /  ,'     |   |
    '''


class Connect():
    def __init__(self, address="101.200.42.193", port=4711):
        self.address = address
        self.mc = minecraft.Minecraft.create(address=address, port=port)
        self.vec = vec3.Vec3()
        self.mcDrawing = minecraftstuff.MinecraftDrawing(self.mc)
        logging.info('Connected to server: {}'.format(address))

    def postToChat(self, *args):
        """
        Post a message to the game chat

        :param str msg: message to post
        """
        msg = ""
        for i in args:
            msg += str(i)
        gfw = DFAFilter()
        path = "sensitive_words.txt"
        gfw.parse(path)
        filtered_msg = gfw.filter(msg)
        self.mc.postToChat(filtered_msg)
        logging.info('You post message to the game: {}'.format(filtered_msg))

    say = postToChat

    def getPlayerId(self, player_name):
        """
        Get the entity id of the named player

        :param string player_name: player's name
        :return: player's id
        """

        try:
            player_id = self.mc.getPlayerEntityId(player_name)
            return player_id
        except Exception as err:
            logging.info('{} is not on this server {}'.format(player_name, errart))
            sys.exit()

    getId = getPlayerId

    def getPlayerEntityIds(self):
        """
        Get the entity ids of the connected players

        :return: online players' list
        """
        player_ids = self.getPlayerIds()
        return player_ids

    getIds = getPlayerEntityIds

    def getName(self, id):
        """
        Get the list name of the player with entity id.
        Also can be used to find name of entity if entity is not a player.

        :param id: entity's id
        :return: String entity_name
        """
        name = self.mc.entity.getName(id)
        return name

    def getPlayerPosition(self, player_name):
        """
        Get entity tile position

        :param string player_name: player's name
        :return: Vec3
        """
        player_id = self.getPlayerId(player_name)
        player_pos = self.mc.entity.getTilePos(player_id)
        logging.info("{}'s position: ({}, {}, {})".format(player_name, player_pos.x, player_pos.y, player_pos.z))
        return player_pos

    getPos = getPlayerPosition

    def setPlayerPosition(self, player_name, posx, posy, posz):
        """
        Set player position

        :param string player_name: player's name
        :param int posx: The x coordinate
        :param int posy: The y coordinate
        :param int posz: The z coordinate
        """
        player_id = self.getPlayerId(player_name)
        if posy > 256 or posy < -1:
            posy = 256
            self.mc.entity.setPos(player_id, posx, posy, posz)
        else:
            self.mc.entity.setPos(player_id, posx, posy, posz)
        logging.info("set {}'s position to: ({}, {}, {})".format(player_name, posx, posy, posz))

    setPos = setPlayerPosition

    def getPoint(self, x, y, z):
        """
        Get a Point, capsulate coordinates to a Vec3 object

        :param int x: The x coordinate
        :param int y: The y coordinate
        :param int z: The z coordinate
        :return: Vec3
        """
        point = vec3.Vec3(x, y, z)
        logging.info("You packed a vector: {}".format(point))
        return point

    vec3 = getPoint

    def getRotation(self, player_name):
        """
        Get entity rotation

        :param string player_name: player's name
        :return: float (-360, 0]
        """
        player_entity_id = self.getPlayerId(player_name)
        player_direction = self.mc.entity.getRotation(player_entity_id)
        return player_direction

    def getRotationFacing(self, player_name):
        """
        Get player's rotation

        :param string player_name: player's name
        :return: one of them: 'E' 'W' 'S' 'N' 'SW' 'NW' 'NE' 'SE'
        """
        player_entity_id = self.getPlayerId(player_name)
        player_direction = self.mc.entity.getRotation(player_entity_id)
        if 30 < player_direction <= 60 or -330 < player_direction <= -300:
            return "WS"
        elif 60 < player_direction <= 120 or -300 < player_direction <= -240:
            return "W"
        elif 120 < player_direction <= 150 or -240 < player_direction <= -210:
            return "WN"
        elif 150 < player_direction <= 210 or -210 < player_direction <= -150:
            return "N"
        elif 210 < player_direction <= 240 or -150 < player_direction <= -120:
            return "EN"
        elif 240 < player_direction <= 300 or -120 < player_direction <= -60:
            return "E"
        elif 300 < player_direction <= 330 or -60 < player_direction <= -30:
            return "ES"
        else:
            return "S"

    def getDirection(self, player_name):
        """
        Get player's facing direction

        :param string player_name: player's name
        :return: vec3

        example:
            watch up: (x, 1, z)
            watch below: (x, -1, z)
            watch east: (1, y, 0)
            watch west: (-1, y, 0)
            watch north: (0, y, -1)
            watch south: (0, y, 1)
        """
        player_entity_id = self.getPlayerId(player_name)
        player_direction = self.mc.entity.getDirection(player_entity_id)
        return player_direction

    def getAltitude(self, player_name):
        """
        Get the height of the world (x,z)

        :param player_name: Player's name
        :return: the Y coordinate of the last block that isn't solid from top-down.
        """
        """
        

        :param int x: The x coordinate
        :param int z: The z coordinate
        :return: height(adventure or survival mode)
        """
        player_entity_id = self.getPlayerId(player_name)
        player_pos = self.mc.entity.getTilePos(player_entity_id)
        x, y, z = player_pos.x, player_pos.y, player_pos.z
        height = self.mc.getHeight(x, z)
        return height

    def getHeight(self, x, z):
        """
        Get the height of the world (x,z)
        Returns the Y coordinate of the last block that isn't solid from top-down.

        :param int x: The x coordinate
        :param int z: The z coordinate
        :return: height(adventure or survival mode)
        """
        height = self.mc.getHeight(x, z)
        return height

    def getPitch(self, player_name):
        """
        Get entity pitch

        :param str player_name: player's name
        :return: pitch
        """
        player_entity_id = self.getPlayerId(player_name)
        pitch = self.mc.entity.getPitch(player_entity_id)
        return pitch

    def setPitch(self, player_name, pitch):
        """
        Set entity pitch (entityId:int, pitch)

        :param str player_name: player's name
        :param float pitch: pitch degress
        """
        player_entity_id = self.getPlayerId(player_name)
        self.mc.entity.setPitch(player_entity_id, pitch)

    def spawnEntity(self, *args):
        """
        Spawn entity [check entity list, go to mcpi.entity]"

        :param int args:  (x, y, z, id, [data])
        """
        self.mc.spawnEntity(*args)
        logging.info("spawn a entity[{}] on ({}, {}, {})".format(args[3], args[0], args[1], args[2]))

    createEntity = spawnEntity

    def drawLine(self, *args):
        if len(args) > 4:
            self.drawLineByXYZ(*args)
        else:
            self.drawLineByPoints(*args)

    def drawLineByXYZ(self, x1, y1, z1, x2, y2, z2, blockID=35, style=0):
        """
        draws a line between 2 points

        :param int x1: The x1 coordinate
        :param int y1: The y1 coordinate
        :param int z1: The z1 coordinate
        :param int x2: The x2 coordinate
        :param int y2: The y2 coordinate
        :param int z2: The z2 coordinate
        :param int blockID: The block id, default to 35(WOOL_BLOCK)
        :param int style: The block data value, defaults to 0.
        :return: None
        """
        self.mcDrawing.drawLine(x1, y1, z1, x2, y2, z2, blockID, style)
        logging.info(
            "drawLine: ({}, {}, {}) -> ({}, {}, {}) blockID: {} style: {}".format(x1, y1, z1, x2, y2, z2, blockID,
                                                                                  style))

    def drawLineByPoints(self, point1, point2, blockID=35, style=0):
        """
        draws a line between 2 points

        :param mcpi.vec3.Vec3 point1: vec3
        :param mcpi.vec3.Vec3 point2: vec3
        :param int blockID: blockID
        :param int style: defaults to 0
        """
        self.mcDrawing.drawLine(point1.x, point1.y, point1.z, point2.x, point2.y, point2.z, blockID, style)
        logging.info(
            "drawLine: {} -> {} blockID: {} style: {}".format(point1, point2, blockID, style))

    def drawCircle(self, x0, y0, z0, radius, blockID, style=0):
        """
        draws a circle in the Y plane (i.e. vertically)

            :param int x0:
                The x position of the centre of the circle.

            :param int y0:
                The y position of the centre of the circle.

            :param int z0:
                The z position of the centre of the circle.

            :param int radius:
                The radius of the sphere.

            :param int blockID:
                The block id.

            :param int blockData:
                The block data value, defaults to ``0``.
        """

        self.mcDrawing.drawCircle(x0, y0, z0, radius, blockID, style)
        logging.info(
            "drawCircle: ({}, {}, {}) radius: {} blockID: {} style: {}".format(x0, y0, z0, radius, blockID, style))

    verticalCircle = drawCircle

    def drawHorizontalCircle(self, x0, y, z0, radius, blockID, style=0):
        """
        draws a circle in the X plane (i.e. horizontally)

            :param int x0:
                The x position of the centre of the circle.

            :param int y:
                The y position of the centre of the circle.

            :param int z0:
                The z position of the centre of the circle.

            :param int radius:
                The radius of the circle.

            :param int blockID:
                The block id.

            :param int style:
                The block data value, defaults to ``0``.
        """
        self.mcDrawing.drawHorizontalCircle(x0, y, z0, radius, blockID, style)

    flatCircle = drawHorizontalCircle

    def drawSphere(self, x, y, z, radius, blockID, style=0):
        """
            draws a sphere around a point to a radius

            :param int x:
                The x position of the centre of the sphere.

            :param int y:
                The y position of the centre of the sphere.

            :param int z:
                The z position of the centre of the sphere.

            :param int radius:
                The radius of the sphere.

            :param int blockID:
                The block id.

            :param int style:
                The block data value, defaults to ``0``.
            """
        self.mcDrawing.drawSphere(x, y, z, radius, blockID, style)

    ball = drawSphere

    def drawText(self, x, y, z, content='', gap=0, foreground=35, forestyle=0, background=0, backstyle=0):
        """
        draw text in Minecraft world.
        :param int x: x坐标
        :param int y: y坐标
        :param int z: z坐标
        :param content: 内容
        :param foreground: 字体材质
        :param forestyle: 字体样式
        :param background: 背景材质
        :param backstyle: 背景样式
        """
        pos = vec3.Vec3(x, y, z)
        gap = gap + 1
        forward = vec3.Vec3(gap, 0, 0)  # 每一列之间前进的间隔，1是紧挨着
        upVec = vec3.Vec3(0, gap, 0)
        text.drawText(self.mc, fonts.FONTS['8x8'], pos + forward, forward, upVec, content, foreground, forestyle,
                      background, backstyle)

    def drawHollowSphere(self, x, y, z, radius, blockID, style=0):
        """
                draws a hollow sphere around a point to a radius, sphere has to big enough to be hollow!

                :param int x:
                    The x position of the centre of the sphere.

                :param int y:
                    The y position of the centre of the sphere.

                :param int z:
                    The z position of the centre of the sphere.

                :param int radius:
                    The radius of the sphere.

                :param int blockID:
                    The block id.

                :param int style:
                    The block data value, defaults to ``0``.
                """
        self.mcDrawing.drawHollowSphere(x, y, z, radius, blockID, style)

    emptyBall = drawHollowSphere

    def drawFace(self, vertices, filled=False, blockID=35, style=0):
        """
            draws a face, when passed a collection of vertices which make up a polyhedron

            :param list vertices:
                A list of points, passed as list.

            :param boolean filled:
                If ``True`` fills the face with blocks.

            :param int blockID:
                The block id.

            :param int style:
                The block data value, defaults to ``0``.
        """
        # get the edges of the face
        edgesVertices = []
        # persist first vertex
        firstVertex = vertices[0]
        # get last vertex
        lastVertex = vertices[0]
        # loop through vertices and get edges
        if isinstance(vertices[0], (list, tuple)):
            for vertex in vertices[1:]:
                # got 2 vertices, get the points for the edge
                edgesVertices = edgesVertices + mcDrawing.getLine(lastVertex[0], lastVertex[1], lastVertex[2],
                                                                  vertex[0], vertex[1], vertex[2])
                # persist the last vertex found
                lastVertex = vertex
            # get edge between the last and first vertices
            edgesVertices = edgesVertices + mcDrawing.getLine(lastVertex[0], lastVertex[1], lastVertex[2],
                                                              firstVertex[0], firstVertex[1], firstVertex[2])
        else:
            for vertex in vertices[1:]:
                # got 2 vertices, get the points for the edge
                edgesVertices = edgesVertices + self.mcDrawing.getLine(lastVertex.x, lastVertex.y, lastVertex.z,
                                                                       vertex.x,
                                                                       vertex.y,
                                                                       vertex.z)
                # persist the last vertex found
                lastVertex = vertex
            # get edge between the last and first vertices
            edgesVertices = edgesVertices + self.mcDrawing.getLine(lastVertex.x, lastVertex.y, lastVertex.z,
                                                                   firstVertex.x,
                                                                   firstVertex.y, firstVertex.z)

        if (filled):
            # draw solid face
            # sort edges vertices
            def keyX(point):
                return point.x

            def keyY(point):
                return point.y

            def keyZ(point):
                return point.z

            edgesVertices.sort(key=keyZ)
            edgesVertices.sort(key=keyY)
            edgesVertices.sort(key=keyX)

            # draw lines between the points on the edges
            # this algorithm isnt very efficient, but it does always fill the gap
            lastVertex = edgesVertices[0]
            for vertex in edgesVertices[1:]:
                # got 2 vertices, draw lines between them
                self.mcDrawing.drawLine(lastVertex.x, lastVertex.y, lastVertex.z, vertex.x, vertex.y, vertex.z, blockID,
                                        style)
                # print "x = " + str(lastVertex.x) + ", y = " + str(lastVertex.y) + ", z = " + str(lastVertex.z) + " x2 = " + str(vertex.x) + ", y2 = " + str(vertex.y) + ", z2 = " + str(vertex.z)
                # persist the last vertex found
                lastVertex = vertex
        else:
            # draw wireframe
            self.mcDrawing.drawVertices(edgesVertices, blockID, style)

    plane = drawFace

    def setBlock(self, x, y, z, blockID, style=0):
        """
        Set block (x,y,z,blockID,[style])

        :param int x: The x coordinate
        :param int y: The y coordinate
        :param int z: The z coordinate
        :param int blockID: The block id.
        :param int style: The block data value, defaults to ``0``
        """
        self.mc.setBlock(x, y, z, blockID, style)
        pos = vec3.Vec3(x, y, z)
        logging.info("setBlock {} blockID:{} style:{}".format(pos, blockID, style))

    def setBlocks(self, x0, y0, z0, x1, y1, z1, blockID, style=0):
        """
        Set a cuboid of blocks (x0,y0,z0,x1,y1,z1,blockID,[style])


        :param int x0: The x0 coordinate
        :param int y0: The y0 coordinate
        :param int z0: The z0 coordinate
        :param int x1: The x1 coordinate
        :param int y1: The y1 coordinate
        :param int z1: The z1 coordinate
        :param int blockID: The block id
        :param int style: The block data value, defaults to ``0``
        """
        v0 = vec3.Vec3(x0, y0, z0)
        v1 = vec3.Vec3(x1, y1, z1)
        self.mc.setBlocks(x0, y0, z0, x1, y1, z1, blockID, style)
        logging.info("setBlocks {} {} blockID:{} style:{}".format(v0, v1, blockID, style))

    def setSign(self, *args):
        """
            Set a sign

            Wall signs (id=68) require data for facing direction 2=north, 3=south, 4=west, 5=east
            Standing signs (id=63) require data for facing rotation (0-15) 0=south, 4=west, 8=north, 12=east

            :param args: (x,y,z,blockID,facing direction,[line1,line2,line3,line4])
            """
        self.mc.setSign(*args)

    def getBlockByPlayer(self, player_name):
        """
            Get the blcokID 1 block below the player.

            :param string player_name: player's name
            :return: block id
            """
        player_id = self.getPlayerId(player_name)
        player_pos = self.mc.entity.getTilePos(player_id)
        blockID = self.mc.getBlock(player_pos.x, player_pos.y - 1, player_pos.z)
        if blockID == 0:
            logging.info("You are standing on AIR")
        elif blockID == 1:
            logging.info("You are standing on a STONE")
        elif blockID == 3:
            logging.info("You are standing on a DIRT")
        else:
            logging.info("You are standing on an unknown block")
        return blockID

    def getBlock(self, x, y, z):
        """
        Get block.

        :param int x: The x coordinate
        :param int y: The y coordinate
        :param int z: The z coordinate
        :return: block id
        """
        blockID = self.mc.getBlock(x, y, z)
        return blockID

    def getBlockWithData(self, x, y, z):
        """
        Get block with data.

        :param int x: The x coordinate
        :param int y: The y coordinate
        :param int z: The z coordinate
        :return: Block

        example:
        data = mc.getBlockWithData(x, y - 1, z)
        print(data)
        Get the block id and data.
        Suppose you are standing on a orange WOOL block,
        you gonna get a data like this -- Block(35, 1);
        If you are standing on a GRASS block,
        you gonna get a data like this -- Block(2, 0)
        """
        block_with_data = self.mc.getBlockWithData(x, y, z)
        return block_with_data

    getBlockData = getBlockWithData

    def getColor(self, x, y, z):
        block_with_data = self.mc.getBlockWithData(x, y, z)
        id = block_with_data.id
        style = block_with_data.data
        # 35羊毛；95彩色玻璃；159硬化粘土；160彩色玻璃板；171地毯；251混凝土（水泥）；252混凝土（水泥）粉末
        if id in [35, 95, 159, 160, 171, 251, 252]:
            color = style
            return color
        else:
            logging.info("可以得到颜色的方块有：35羊毛；95彩色玻璃；159硬化粘土；160彩色玻璃板；171地毯；251混凝土（水泥）；252混凝土（水泥）粉末")

    def getColorName(self, x, y, z):
        color_name = None
        id = self.getColor(x, y, z)
        if id == 0:
            color_name = "white"
        elif id == 1:
            color_name = "orange"
        elif id == 2:
            color_name = "magenta"
        elif id == 3:
            color_name = "light blue"
        elif id == 4:
            color_name = "yellow"
        elif id == 5:
            color_name = "lime"
        elif id == 6:
            color_name = "pink"
        elif id == 7:
            color_name = "gray"
        elif id == 8:
            color_name = "light gray"
        elif id == 9:
            color_name = "cyan"
        elif id == 10:
            color_name = "purple"
        elif id == 11:
            color_name = "blue"
        elif id == 12:
            color_name = "brown"
        elif id == 13:
            color_name = "green"
        elif id == 14:
            color_name = "red"
        elif id == 15:
            color_name = "black"
        return color_name

    def getBlocks(self, *args):
        """
        Get a cuboid of blocks.
        :param args: Vec3 or Int. Use the getPoint(x, y ,z) function to get the point.
                    Or (x1, y1, z1, x2, y2, z2)
        :return: map Iterator
                example:
                point1 = mymc.getPoint(x, y, z)
                point2 = mymc.getPoint(x, y - 10, z)
                print(type(point1))  # <class 'mcpi.vec3.Vec3'>

                blocks = mymc.getBlocks(point1, point2)
                print(blocks)  # <map object at 0x1077da0b8>

                for i in blocks:
                    print(i)   # 1, 1, 1, 1, 1, 3, 3, 3, 3, 2, 31
        """
        if len(args) > 2:
            blocks = self.getBlocksByXYZ(*args)
        else:
            blocks = self.getBlocksByPoints(*args)
        return blocks

    def getBlocksByXYZ(self, x1, y1, z1, x2, y2, z2):
        return self.mc.getBlocks(x1, y1, z1, x2, y2, z2)

    def getBlocksByPoints(self, point1, point2):
        return self.mc.getBlocks(point1.x, point1.y, point1.z, point2.x, point2.y, point2.z)

    def buildPixelArt(self, filename, player_name, air=False, t=0):
        """
        Build a pixel art below the player's position

        :param string filename: .csv
        :param string playername: player's name
        :param bool air:  show the pixel art or not
        """
        player_id = self.getPlayerId(player_name)
        pos = self.mc.entity.getTilePos(player_id)
        with open(sys.path[0] + '/' + 'csvFiles' + '/' + filename, mode='r', encoding='utf-8-sig') as f:
            lines = f.readlines()
        coords = lines[0].split(",")
        sizex = int(coords[0])
        sizey = int(coords[1])
        sizez = int(coords[2])

        lineidx = 1

        for y in range(sizey):
            lineidx = lineidx + 1
            for x in range(sizex):
                line = lines[lineidx]
                lineidx = lineidx + 1
                data = line.split(",")
                for z in range(sizez):
                    try:
                        d = int(data[z])
                        if air:
                            blockID = 0
                            blockstyle = 0
                        else:
                            blockID = d // 100
                            blockstyle = d % 100
                    except:
                        blockID = 0
                        blockstyle = 0
                    time.sleep(t)
                    self.mc.setBlock(pos.x + x, pos.y - y, pos.z + z, blockID, blockstyle)
        logging.info('buildPixelArt: {}'.format(filename))

    pixelArt = buildPixelArt

    def buildPixelArtbyPos(self, filename, x, y, z, air=False):
        """
        Build a pixel art below the player's position

        :param string filename: .csv
        :param int x: The x coordinate
        :param int y: The y coordinate
        :param int z: The z coordinate
        :param bool air: show the pixel art or not
        """
        pos = vec3.Vec3(x, y, z)
        if filename == "skull.csv" or filename == "herobrine.csv":
            self.mc.postToChat("This Pixel Art is designed by ISB student")
        with open(sys.path[0] + '/' + 'csvFiles' + '/' + filename, encoding='utf-8-sig') as f:
            lines = f.readlines()
        coords = lines[0].split(",")
        sizex = int(coords[0])
        sizey = int(coords[1])
        sizez = int(coords[2])

        lineidx = 1

        for y in range(sizey):
            lineidx = lineidx + 1
            for x in range(sizex):
                line = lines[lineidx]
                lineidx = lineidx + 1
                data = line.split(",")
                for z in range(sizez):
                    try:
                        d = int(data[z])
                        if air:
                            blockID = 0
                            blockstyle = 0
                        else:
                            blockID = d // 100
                            blockstyle = d % 100
                    except:
                        blockID = 0
                        blockstyle = 0
                    self.mc.setBlock(pos.x + x, pos.y - y, pos.z + z, blockID, blockstyle)

    def build(self, filename, posx, posy, posz, air=False):
        """
        Build pixel art on the position(posx, posy, posz)

        :param string filename: .csv file
        :param int posx: The x coordinate
        :param int posy: The y coordinate
        :param int posz: The z coordinate
        :param air: show the pixel art or not
        """
        with open(sys.path[0] + '/' + 'csvFiles' + '/' + filename, encoding='utf-8-sig') as f:
            lines = f.readlines()
        coords = lines[0].split(",")
        sizex = int(coords[0])
        sizey = int(coords[1])
        sizez = int(coords[2])

        lineidx = 1

        for y in range(sizey):
            lineidx = lineidx + 1
            for x in range(sizex):
                line = lines[lineidx]
                lineidx = lineidx + 1
                data = line.split(",")
                for z in range(sizez):
                    try:
                        d = int(data[z])
                        if air:
                            blockID = 0
                            blockstyle = 0
                        else:
                            blockID = d // 100
                            blockstyle = d % 100
                    except:
                        blockID = 0
                        blockstyle = 0
                    self.mc.setBlock(posx + x, posy - y, posz + z, blockID, blockstyle)
        logging.info('build: {}'.format(filename))

    def transferTo3d(self, strArt=""):
        piclist = strArt.split("\n")
        piclist.reverse()
        pic = []
        for i in piclist:
            if i:
                a = [j for j in i]
                pic.append(a)
        return pic

    def buildMaze(self, strArt="", playername="", height=1, blockID=35, style=0, t=0):
        """
        根据字符画，在我的世界绘制迷宫
        :param strArt: 迷宫字符画
        :param playername: 玩家名
        :param height: 迷宫高度
        :param blockID: 迷宫方块材质
        :param style: 迷宫方块样式/颜色
        :param t: 建造时间间隔
        """
        pos = self.mc.entity.getPos(mc.getPlayerEntityId(playername))
        x, y, z = pos.x, pos.y, pos.z
        for i in range(height):
            self.buildArt3dByXYZHorizontal(strArt, x, y, z, blockID, t)
            y += 1
        logging.info('buildMaze')

    def buildArt3d(self, strArt="", playername="", width=1, blockID=35, t=0):
        """
        根据字符画，在我的世界绘制垂直于地面的像素图
        :param strArt: 字符画
        :param playername: 玩家名
        :param width: 像素画厚度
        :param blockID: 像素画方块材质
        :param style: 像素画方块样式/颜色
        :param t: 建造时间间隔
        """
        pos = self.mc.entity.getPos(mc.getPlayerEntityId(playername))
        x, y, z = pos.x, pos.y, pos.z
        for i in range(width):
            self.buildArt3dByXYZVertical(strArt, x, y, z, blockID, t)
            x += 1
        logging.info('buildArt3d')

    def buildTorii(self, x, y, z):
        """
        在(x, y, z)坐标处建造一个鸟居建筑
        :param x:
        :param y:
        :param z:
        """
        self.mc.setBlocks(x + 4, y, z, x + 6, y + 1, z, 251, 15)
        self.mc.setBlocks(x - 4, y, z, x - 6, y + 1, z, 251, 15)
        self.mc.setBlocks(x + 5, y + 2, z, x + 5, y + 13, z, 152)
        self.mc.setBlocks(x - 5, y + 2, z, x - 5, y + 13, z, 152)
        self.mc.setBlocks(x - 9, y + 13, z, x + 9, y + 13, z, 152)
        self.mc.setBlocks(x - 9, y + 14, z, x + 9, y + 14, z, 251, 15)
        self.mc.setBlocks(x - 10, y + 15, z, x + 10, y + 15, z, 251, 15)
        self.mc.setBlocks(x - 7, y + 15, z, x + 7, y + 15, z, 0)
        self.mc.setBlocks(x - 8, y + 9, z, x + 8, y + 9, z, 152)
        self.mc.setBlocks(x, y + 9, z, x, y + 12, z, 152)
        self.mc.setBlock(x, y + 9, z - 1, 5)
        self.mc.setBlock(x, y + 10, z - 1, 50)
        self.mc.setBlock(x, y + 9, z + 1, 5)
        self.mc.setBlock(x, y + 10, z + 1, 50)
        self.mc.setBlock(x + 5, y + 9, z - 1, 5)
        self.mc.setBlock(x + 5, y + 10, z - 1, 50)
        self.mc.setBlock(x + 5, y + 9, z + 1, 5)
        self.mc.setBlock(x + 5, y + 10, z + 1, 50)

        self.mc.setBlock(x - 5, y + 9, z - 1, 5)
        self.mc.setBlock(x - 5, y + 10, z - 1, 50)
        self.mc.setBlock(x - 5, y + 9, z + 1, 5)
        self.mc.setBlock(x - 5, y + 10, z + 1, 50)
        logging.info('buildTorri')

    def buildArt3dByXYZHorizontal(self, strArt="", x=0, y=0, z=0, blockID=35, t=0):
        pic = self.transferTo3d(strArt)
        for i in pic:
            newz = z
            for j in i:
                if j == "w":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 0)
                    newz -= 1
                elif j == "r":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 14)
                    newz -= 1
                elif j == "g":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 13)
                    newz -= 1
                elif j == "b":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 11)
                    newz -= 1
                elif j == "y":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 4)
                    newz -= 1
                elif j == "o":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 1)
                    newz -= 1
                elif j == "k":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 15)
                    newz -= 1
                elif j == "p":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 10)
                    newz -= 1
                else:
                    newz -= 1
            x -= 1

    def buildArt3dByXYZVertical(self, strArt="", x=0, y=0, z=0, blockID=35, t=0):
        """
        在指定的坐标位置生成像素画
        :param strArt: 字符画变量
        :param x:
        :param y:
        :param z:
        :param blockID: 方块编号
        :param t: 建造间隔时间
        :return:
        """
        pic = self.transferTo3d(strArt)
        for i in pic:
            newz = z
            for j in i:
                if j == "w":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 0)
                    newz -= 1
                elif j == "r":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 14)
                    newz -= 1
                elif j == "g":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 13)
                    newz -= 1
                elif j == "b":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 11)
                    newz -= 1
                elif j == "y":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 4)
                    newz -= 1
                elif j == "o":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 1)
                    newz -= 1
                elif j == "k":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 15)
                    newz -= 1
                elif j == "p":
                    time.sleep(t)
                    self.mc.setBlock(x, y, newz + 1, blockID, 10)
                    newz -= 1
                else:
                    # mc.setBlock(x, y, newz + 1, 0)
                    newz -= 1
            y += 1

    def buildTree(self, branchLen, t):
        """
        Build a tree

        :param string player_name: player's name
        :param  minecraftstuff.MinecraftTurtle t: branch's length

        example:

        remember to set the tree direction to up:
        t.setverticalheading(90)

        """
        if branchLen > 6:
            if branchLen > 10:
                t.penblock(block.WOOD)
            else:
                t.penblock(block.LEAVES)

            # for performance
            x, y, z = t.position.x, t.position.y, t.position.z
            # draw branch
            t.forward(branchLen)

            t.up(20)
            self.buildTree(branchLen - 2, t)

            t.right(90)
            self.buildTree(branchLen - 2, t)

            t.left(180)
            self.buildTree(branchLen - 2, t)

            t.down(40)
            t.right(90)
            self.buildTree(branchLen - 2, t)

            t.up(20)

            # go back
            # t.backward(branchLen)
            # for performance - rather than going back over every line
            t.setposition(x, y, z)

    def buildColofulTree(self, branchLen, t):
        """
        Build a colorful WOOL blocks tree

        :param int branchLen: branch's length
        :param minecraftstuff.MinecraftTurtle t: turtle

        example:

        remember to set the tree direction to up:
        t.setverticalheading(90)
        """
        if branchLen > 6:
            t.penblock(35, random.randint(0, 15))

            # for performance
            x, y, z = t.position.x, t.position.y, t.position.z
            # draw branch
            t.forward(branchLen)

            t.up(20)
            self.buildColofulTree(branchLen - 2, t)

            t.right(90)
            self.buildColofulTree(branchLen - 2, t)

            t.left(180)
            self.buildColofulTree(branchLen - 2, t)

            t.down(40)
            t.right(90)
            self.buildColofulTree(branchLen - 2, t)

            t.up(20)

            # go back
            # t.backward(branchLen)
            # for performance - rather than going back over every line
            t.setposition(x, y, z)

    def buildTreeByPos(self, x=0, y=0, z=0, branchLen=20):
        """
        Build a tree by position

        :param int x: The x coordinate
        :param int y: The y coordinate
        :param int z: The z coordinate
        :param int branchLen: branch's length
        """
        steve = minecraftstuff.MinecraftTurtle(self.mc)
        steve.setx(x)
        steve.sety(y)
        steve.setz(z)
        steve.setverticalheading(90)
        steve.speed(0)
        self.buildTree(branchLen, steve)

    def buildColofulTreeByPos(self, x=0, y=0, z=0, branchLen=20):
        """
            Build a colorful WOOL block tree by position

            :param int x: The x coordinate
            :param int y: The y coordinate
            :param int z: The z coordinate
            :param int branchLen: branch's length
            """
        steve = minecraftstuff.MinecraftTurtle(self.mc)
        steve.setx(x)
        steve.sety(y)
        steve.setz(z)
        steve.setverticalheading(90)
        steve.speed(0)
        self.buildColofulTree(branchLen, steve)

    def getLine(self, x1, y1, z1, x2, y2, z2):
        """
        Returns all the points which would make up a line between 2 points as a list

        3d implementation of bresenham line algorithm

        :param int x1:
            The x position of the first point.

        :param int y1:
            The y position of the first point.

        :param int z1:
            The z position of the first point.

        :param int x2:
            The x position of the second point.

        :param int y2:
            The y position of the second point.

        :param int z2:
            The z position of the second point.

        example:
        line = mc.getLine(x, y, z, x, y - 3, z)  # [Vec3(10096,55,9578), Vec3(10096,54,9578), Vec3(10096,53,9578), Vec3(10096,52,9578)]
        """
        return self.mcDrawing.getLine(x1, y1, z1, x2, y2, z2)

    def distanceBetween(self, *args):
        """
        Calculate the distance between 2 position
        :param args: int or Vec3
        :return: distance
        """
        if len(args) > 2:
            distance_between = self.distanceBetweenByXYZ(*args)
        else:
            distance_between = self.distanceBetweenPoints(*args)
        return distance_between

    distance = distanceBetween

    def distanceBetweenByXYZ(self, x1, y1, z1, x2, y2, z2):
        """
        Calculate the distance between 2 position

        :param int x1: The x1 coordinate
        :param int y1: The y1 coordinate
        :param int z1: The z1 coordinate
        :param int x2: The x2 coordinate
        :param int y2: The y2 coordinate
        :param int z2: The z2 coordinate
        :return: distance
        """
        xd = x1 - x2
        yd = y1 - y2
        zd = z1 - z2
        return math.sqrt((xd * xd) + (yd * yd) + (zd * zd))

    def distanceBetweenPoints(self, point1, point2):
        """
        Calculate the distance between 2 position

        :param point1:  point1
        :param point2:  point2
        :return: distance
        """
        xd = point2.x - point1.x
        yd = point2.y - point1.y
        zd = point2.z - point1.z
        return math.sqrt((xd * xd) + (yd * yd) + (zd * zd))

    def shapeBlock(self, x, y, z, blockID, style=0, tag=''):
        """
        ShapeBlock - a class to hold one block within a shape

        :param int x:
            The x position.

        :param int y:
            The y position.

        :param int z:
            The z position.

        :param int blockID:
            The block id.

        :param int style:
            The block data value, defaults to ``0``.

        :param string tag:
            A tag for the block, this is useful for grouping blocks together and keeping track of them as the position of blocks can change, defaults to ``""``.
        """
        element = minecraftstuff.ShapeBlock(x, y, z, blockID, style)
        return element

    def setShapeBlock(self, x, y, z, blockID, style=0, tag=""):
        """
            sets one block in the shape and redraws it

            draws a single point in Minecraft, i.e. 1 block

            :param int x:
                The x position.

            :param int y:
                The y position.

            :param int z:
                The z position.

            :param int blockID:
                The block id.

            :param int blockData:
                The block data value, defaults to ``0``.

            :param string tag:
                A tag for the block, this is useful for grouping blocks together and keeping
                track of them as the position of blocks can change, defaults to ``""``.
        """
        minecraftstuff.MinecraftShape.setBlock(x, y, z, blockID, style=0, tag='')

    def createShape(self, shapePos, shapeBlocks=None):
        if isinstance(shapeBlocks[0], (list, tuple)):
            shape = self.createShapeBy2DList(shapePos, shapeBlocks)
        else:
            shape = self.createShapeByPoints(shapePos, shapeBlocks)
        return shape

    def createShapeByPoints(self, shapePos, shapeBlocks=None):
        """
        MinecraftShape - the implementation of a 'shape' in Minecraft.
        Each shape consists of one or many blocks with a position relative to each other.
        Shapes can be transformed by movement and rotation.

        :param mcpi.minecraft.Vec3 shapePos: The position where the shape should be created
        :param list shapeBlocks: A list of ShapeBlocks which make up the shape. This defaults to ``None``.
        :return: MinecraftShape
        """
        shape = minecraftstuff.MinecraftShape(self.mc, shapePos, shapeBlocks)
        return shape

    def createShapeBy2DList(self, shapePosList, shapeBlocks=None):
        """
        MinecraftShape - the implementation of a 'shape' in Minecraft.
        Each shape consists of one or many blocks with a position relative to each other.
        Shapes can be transformed by movement and rotation.

        :param mcpi.minecraft.Vec3 shapePos: The position where the shape should be created
        :param shapeBlocks: A list of ShapeBlocks which make up the shape. This defaults to ``None``.
        :return: MinecraftShape
        """
        shapeBlocks_list = []

        shapePos = vec3.Vec3(shapePosList[0], shapePosList[1], shapePosList[2])
        for i in shapeBlocks:
            x, y, z, blockID, style = i[0], i[1], i[2], i[3], i[4]
            element = minecraftstuff.ShapeBlock(x, y, z, blockID, style)
            shapeBlocks_list.append(element)
        shape = minecraftstuff.MinecraftShape(self.mc, shapePos, shapeBlocks_list)
        return shape

    def createTurtle(self, x, y, z):
        """
        MinecraftTurle - a graphics turtle, which can be used to create 'things' in Minecraft by controlling its position, angles and direction

        :param int x: The x coordinate
        :param int y: The y coordinate
        :param int z: The z coordinate
        :return: MinecraftTurtle
        """
        minecraft_turtle = minecraftstuff.MinecraftTurtle(self.mc)
        minecraft_turtle.setx(x)
        minecraft_turtle.sety(y)
        minecraft_turtle.setz(z)
        return minecraft_turtle

    def createPet(self, owner, blockID, type=0):
        """
        Create a ugly pet -_- aha！ And follow the owner.

        :param string owner: player's name
        :param int blockID: pet's blockID
        :param int type: The block data value, defaults to ``0``
        """
        player_id = self.getPlayerId(owner)
        myPetsPos = self.mc.entity.getTilePos(player_id)
        myPetsPos.x = myPetsPos.x + 5
        myPetsPos.y = self.mc.getHeight(myPetsPos.x, myPetsPos.z)
        self.mc.setBlock(myPetsPos.x, myPetsPos.y, myPetsPos.z, blockID, type)
        self.mc.postToChat("<block> Hi I'm your pet")
        target = myPetsPos.clone()  # pet's target
        while True:
            time.sleep(0.1)
            player_id = self.getPlayerId(owner)
            pos = self.mc.entity.getTilePos(player_id)
            target = pos.clone()
            # move your pet
            if myPetsPos != target:
                blocksBetween = self.getLine(myPetsPos.x, myPetsPos.y, myPetsPos.z, target.x, target.y, target.z)
                for blockBetween in blocksBetween[:-1]:
                    self.mc.setBlock(myPetsPos.x, myPetsPos.y, myPetsPos.z, 0)
                    myPetsPos = blockBetween.clone()
                    # myPetsPos.y = mc.getHeight(myPetsPos.x,myPetsPos.z)
                    self.mc.setBlock(myPetsPos.x, myPetsPos.y, myPetsPos.z, blockID, type)
                    time.sleep(0.1)
                target = myPetsPos.clone()

    def createAlien(self, playername):
        """
        Create a alien, just like the createPet() function

        :param string playername: player's name
        """
        player_id = self.getPlayerId(playername)
        myPetsPos = self.mc.entity.getTilePos(player_id)

        myPetsPos.x = myPetsPos.x + 5
        petBlocks = [minecraftstuff.ShapeBlock(-1, 0, 0, 35, 5),
                     minecraftstuff.ShapeBlock(0, 0, -1, 35, 5),
                     minecraftstuff.ShapeBlock(1, 0, 0, 35, 5),
                     minecraftstuff.ShapeBlock(0, 0, 1, 35, 5),
                     minecraftstuff.ShapeBlock(0, -1, 0, block.GLOWSTONE_BLOCK.id),
                     minecraftstuff.ShapeBlock(0, 1, 0, block.GLOWSTONE_BLOCK.id)]
        petShape = minecraftstuff.MinecraftShape(self.mc, myPetsPos, petBlocks)
        self.mc.postToChat("<block> Hi I'm your pet")
        # target = myPetsPos.clone()  # pet's target
        while True:
            time.sleep(0.25)
            player_id = self.getPlayerId(playername)
            pos = self.mc.entity.getTilePos(player_id)
            target = pos.clone()
            # move your pet
            if myPetsPos != target:
                blocksBetween = self.getLine(myPetsPos.x, myPetsPos.y, myPetsPos.z, target.x, target.y, target.z)
                for blockBetween in blocksBetween[:-1]:
                    # mc.setBlock(myPetsPos.x,myPetsPos.y,myPetsPos.z,0)
                    # myPetsPos = blockBetween.clone()
                    # myPetsPos.y = mc.getHeight(myPetsPos.x,myPetsPos.z)
                    # mc.setBlock(myPetsPos.x,myPetsPos.y,myPetsPos.z,blockID)
                    petShape.move(blockBetween.x + 5, blockBetween.y + 5, blockBetween.z)
                    time.sleep(0.25)
                target = myPetsPos.clone()

    def isHit(self, player_name, targetX, targetY, targetZ):
        """
        Check if the player hit the target block

        :param string player_name: player's name
        :param int targetX: The x coordinate
        :param int targetY: The y coordinate
        :param int targetZ: The z coordinate
        :return: True for hit, None for nothing happened
        """

        player_id = self.getPlayerId(player_name)
        events = self.mc.events.pollBlockHits()
        for e in events:
            pos = e.pos
            if pos.x == targetX and pos.y == targetY and pos.z == targetZ and e.entityId == player_id:
                return True

    def hitEvents(self):
        """
        Only triggered by sword

        :return: [BlockEvent]

        example:

        [BlockEvent(BlockEvent.HIT, -4, -1, -10, 1, 640522), BlockEvent(BlockEvent.HIT, 10116, -1, 9559, 1, 640452)]

        player(640522) hit the block(-4, -1, -10) on the up face, player(640452) hit the block(10116, -1, 9559) on the up face

        block faces(up n s w e bottom : 1 2 3 4 5 6)
        """
        blockHits = self.mc.events.pollBlockHits()
        return blockHits

    def getHitEvent(self):
        """
        Get the hitEvent

        :return: int

        example:

        (640452, Vec3(10115,-1,9557), 1)

        hitPlayerID(640452); hitPosition(x, y, z); hitFace：up n s w e bottom : 1 2 3 4 5 6

        x, y, z = mymc.getPlayerPosition(player_name)
        print(x, y, z)
        while True:
            event = mymc.getHitEvent()
            print(event)
            time.sleep(1)
        """
        events = self.mc.events.pollBlockHits()
        for e in events:
            if e == None:
                logging.info('df')
            else:
                # pos = e.pos
                # face = e.face
                # playerID = e.entityId
                # e = (playerID, pos, face)
                return e.face

    def chatEvents(self):
        """
        Triggered by posts to chat

        :return:

        example:

        [ChatEvent(ChatEvent.POST, 640452, sdf)]

        player(640452) post "abcd" to the Minecraft World
        """
        events = self.mc.events.pollChatPosts()
        return events

    def drawPentacleByPlayer(self, x, y, z, step=20, blockID=35, style=1, h=0, show=False, speed=0):
        """
        draw a pentacle on (x, y, z)

        :param int x: The x coordinate
        :param int y: The y coordinate
        :param int z: The z coordinate
        :param step: The length of every step of the MinecraftTurtle
        :param int blockID: block id
        :param int style: block style
        :param int h: relative height with the player
        :param show: show the MinecraftTurtle or not
        :param int speed: MinecraftTurtle's moving speed
        """
        ada = minecraftstuff.MinecraftTurtle(self.mc)
        ada.showturtle = show
        x = x - step / 2
        z = z - math.tan(math.radians(18)) * step / 2
        # print(z)
        ada.speed(speed)
        ada.penblock(blockID, style)

        ada.setx(x)
        ada.sety(y + h)
        ada.setz(z)

        for i in range(5):
            ada.forward(step)
            ada.right(144)

    def drawPentacleByPlayerRadius(self, x, y, z, radius=20, blockID=35, style=1, h=0):
        """
        draw a pentacle on (x, y, z), the player is in the middle of the pentacle

        :param int x: The x coordinate
        :param int y: The y coordinate
        :param int z: The z coordinate
        :param radius: The radius of the outer circle of the pentacle
        :param int blockID: block id
        :param int style: block style
        :param int h: relative height with the player
        """
        sin = int(math.sin(math.radians(36)) * radius)
        cos = int(math.cos(math.radians(36)) * radius)

        point1 = self.getPoint(x, y + h, z - radius)

        point2 = self.getPoint(x - cos, y + h, z - sin)
        point3 = self.getPoint(x + cos, y + h, z - sin)

        point4 = self.getPoint(x - sin, y + h, z + cos)
        point5 = self.getPoint(x + sin, y + h, z + cos)

        self.drawLineByPoints(point1, point4, blockID, style)
        self.drawLineByPoints(point1, point5, blockID, style)
        self.drawLineByPoints(point2, point3, blockID, style)
        self.drawLineByPoints(point2, point5, blockID, style)
        self.drawLineByPoints(point3, point4, blockID, style)

    def _drill_ground(self, x, y, z):
        """
        Build a drill ground(castle) on (x, y, z)

        :param self.mc: Minecraft.create()
        :param int x: The x coordinate
        :param int y: The y coordinate
        :param int z: The z coordinate
        """
        # ------------FLATTEN AND BASIC BUILD UP------------#
        # World Create Blocks 天空 地基 草地的建造
        # 清理以(x, y, z)坐标为中心的257*257场地
        sky = [x - 128, y + 0, z - 128, x + 128, y + 256, z + 128, 00]
        self.mc.setBlocks(sky)
        time.sleep(0.5)
        ground = [x - 128, y - 10, z - 128, x + 128, y - 1, z + 128, 7]
        self.mc.setBlocks(ground)
        time.sleep(0.5)
        grass = [x - 128, y - 1, z - 128, x + 128, y + -1, z + 128, 2]
        self.mc.setBlocks(grass)
        time.sleep(0.5)

        # Exterior Wall & Hollow 外墙
        wall = [x - 128, y + 0, z - 128, x + 128, y + 15, z + 128, 35, 1]
        self.mc.setBlocks(wall)
        time.sleep(0.5)

        hollow = [x - 125, y + 0, z - 125, x + 125, y + 15, z + 125, 00]
        self.mc.setBlocks(hollow)

        # Pathways 小路
        path1 = [x + 75, y - 1, z - 125, x + 85, y - 1, z + 125, 4]
        self.mc.setBlocks(path1)
        time.sleep(0.5)

        path2 = [x - 75, y - 1, z - 125, x - 85, y - 1, z + 125, 4]
        self.mc.setBlocks(path2)
        time.sleep(0.5)

        path3 = [x - 125, y - 1, z + 75, x + 125, y - 1, z + 85, 4]
        self.mc.setBlocks(path3)
        time.sleep(0.5)

        path4 = [x - 125, y - 1, z - 75, x + 125, y - 1, z - 85, 4]
        self.mc.setBlocks(path4)
        time.sleep(0.5)

        path5 = [x - 125, y - 1, z - 35, x + 125, y - 1, z - 20, 4]
        self.mc.setBlocks(path5)
        time.sleep(0.5)

        path6 = [x - 125, y - 1, z + 20, x + 125, y - 1, z + 35, 4]
        self.mc.setBlocks(path6)
        time.sleep(0.5)

        path7 = [x - 35, y - 1, z - 125, x - 20, y - 1, z + 125, 4]
        self.mc.setBlocks(path7)
        time.sleep(0.5)

        path8 = [x + 35, y - 1, z - 125, x + 20, y - 1, z + 125, 4]
        self.mc.setBlocks(path8)
        time.sleep(0.5)

        # Central Moat 护城河
        moat = [x - 75, y - 10, z - 75, x + 75, y - 1, z + 75, 9]
        self.mc.setBlocks(moat)
        time.sleep(0.5)

        # 大厅
        def hall(x1, y1, z1, x2, y2, z2, block):
            xoriginal = x1
            yoriginal = y1
            zoriginal = z1
            # main hall of the castle:
            hall = [x1, y1, z1, x2, y2, z2, block]
            self.mc.setBlocks(hall)
            hollow = [(x1 + 1), (y1 + 1), (z1 + 1), (x2 - 1), (y2 - 1), (z2 - 1), 00]
            self.mc.setBlocks(hollow)
            # Crenelations
            while x1 < x2:
                x1 = x1 + 2
                self.mc.setBlock(x1, y2 + 1, z1, block)
            x1 = xoriginal
            while z1 < z2:
                z1 = z1 + 2
                self.mc.setBlock(x1, y2 + 1, z1, block)
            z1 = zoriginal
            while x1 < x2:
                x1 = x1 + 2
                self.mc.setBlock(x1, y2 + 1, z2, block)
            x1 = xoriginal
            while z1 < z2:
                z1 = z1 + 2
                self.mc.setBlock(x2, y2 + 1, z1, block)
            z1 = zoriginal

        # 大厅窗户
        def windowsx(x, y, z):
            for i in range(5):
                for i in range(5):
                    self.mc.setBlock(x, y, z, 102)
                    y = y + 1
                x = x + 1
                y = y - 5
                for i in range(6):
                    self.mc.setBlock(x, y, z, 102)
                    y = y + 1
                x = x + 1
                y = y - 6
                for i in range(5):
                    self.mc.setBlock(x, y, z, 102)
                    y = y + 1
                x = x + 2
                y = y - 5

        # 大厅窗户
        def windowsz(x, y, z):
            for i in range(5):
                for i in range(5):
                    self.mc.setBlock(x, y, z, 102)
                    y = y + 1
                z = z + 1
                y = y - 5
                for i in range(6):
                    self.mc.setBlock(x, y, z, 102)
                    y = y + 1
                z = z + 1
                y = y - 6
                for i in range(5):
                    self.mc.setBlock(x, y, z, 102)
                    y = y + 1
                z = z + 2
                y = y - 5

        # 大厅窗台
        def hallsillsx(x, y, z):
            for i in range(5):
                for i in range(2):
                    self.mc.setBlock(x, y, z, 89)
                    x = x + 1
                self.mc.setBlock(x, y, z, 89)
                x = x + 2

        # 大厅窗台
        def hallsillsz(x, y, z):
            for i in range(5):
                for i in range(2):
                    self.mc.setBlock(x, y, z, 89)
                    z = z + 1
                self.mc.setBlock(x, y, z, 89)
                z = z + 2

        # 大门
        def doorway(x, y, z):
            while x < 3:
                while y < 5:
                    self.mc.setBlock(x, y, z, 0)
                    y = y + 1
                x = x + 1
                y = 1
                while y < 6:
                    self.mc.setBlock(x, y, z, 0)
                    y = y + 1
                x = x + 1
                y = 1
                while y < 7:
                    self.mc.setBlock(x, y, z, 0)
                    y = y + 1
                x = x + 1
                y = 1
                while y < 6:
                    self.mc.setBlock(x, y, z, 0)
                    y = y + 1
                x = x + 1
                y = 1
                while y < 5:
                    self.mc.setBlock(x, y, z, 0)
                    y = y + 1
                x = x + 1
                y = 1

        # 桥
        def drawbridge(x, y, z):
            for i in range(7):
                for i in range(60):
                    self.mc.setBlock(x, y, z, 17)
                    z = z - 1
                x = x + 1
                z = z + 60

        # 塔楼
        def tower(x1, y1, z1, x2, y2, z2, block):
            xoriginal = x1
            yoriginal = y1
            zoriginal = z1
            # Build and hollow out Tower structure
            tower = [x1, y1, z1, x2, y2, z2, block]
            self.mc.setBlocks(tower)
            hollow = [(x1 + 1), (y1 + 1), (z1 + 1), (x2 - 1), (y2 - 1), (z2 - 1), 00]
            self.mc.setBlocks(hollow)
            # Floors Within Towers
            floor1 = [(x1 + 1), (y1 + 4), (z1 + 1), (x2 - 2), (y1 + 4), (z2 - 1), 17]
            self.mc.setBlocks(floor1)
            floor2 = [(x1 + 1), (y1 + 8), (z1 + 2), (x2 - 1), (y1 + 8), (z2 - 1), 17]
            self.mc.setBlocks(floor2)
            floor3 = [(x1 + 2), (y1 + 12), (z1 + 1), (x2 - 1), (y1 + 12), (z2 - 1), 17]
            self.mc.setBlocks(floor3)
            # Stairways within Towers
            x1 = x1 + 5
            z1 = z1 + 5
            for i in range(4):
                z1 = z1 - 1
                y1 = y1 + 1
                self.mc.setBlock(x1, y1, z1, 114, 3)
            for i in range(4):
                x1 = x1 - 1
                y1 = y1 + 1
                self.mc.setBlock(x1, y1, z1, 114, 1)
            for i in range(4):
                z1 = z1 + 1
                y1 = y1 + 1
                self.mc.setBlock(x1, y1, z1, 114, 2)
            # Reset to original values
            x1 = xoriginal
            y1 = yoriginal
            z1 = zoriginal
            # crenelations
            for i in range(3):
                x1 = x1 + 2
                self.mc.setBlock(x1, y2 + 1, z1, block)
            for i in range(3):
                z1 = z1 + 2
                self.mc.setBlock(x1, y2 + 1, z1, block)
            for i in range(3):
                x1 = x1 - 2
                self.mc.setBlock(x1, y2 + 1, z1, block)
            for i in range(3):
                z1 = z1 - 2
                self.mc.setBlock(x1, y2 + 1, z1, block)

        # 塔楼门，高度2
        def towerDoors(x, y, z, block):
            for i in range(2):
                self.mc.setBlock(x, y, z, block)
                y = y + 1

        # 塔楼窗户，每个窗户的高度是3，每个塔楼有2侧面窗户，每一面有3个窗户
        def towerwindows(x, y, z):
            for i in range(3):
                for i in range(3):
                    self.mc.setBlock(x, y, z, 102)
                    y = y + 1
                y = y + 3

        # castle
        x1 = x - 15
        y1 = y
        z1 = z - 15
        x2 = x + 15
        y2 = y + 12
        z2 = z + 15
        self.mc.setBlocks(x1 - 5, y1 - 10, z1 - 5, x2 + 5, y2 - 12, z2 + 5, 44)
        time.sleep(0.5)

        hall(x1, y1, z1, x2, y2, z2, 24)
        time.sleep(0.5)

        tower(x1 - 3, y1, z1 - 3, x1 + 3, y2 + 6, z1 + 3, 24)
        time.sleep(0.5)

        tower(x2 - 3, y1, z1 - 3, x2 + 3, y2 + 6, z1 + 3, 24)
        time.sleep(0.5)

        tower(x1 - 3, y1, z2 - 3, x1 + 3, y2 + 6, z2 + 3, 24)
        time.sleep(0.5)

        tower(x2 - 3, y1, z2 - 3, x2 + 3, y2 + 6, z2 + 3, 24)
        time.sleep(0.5)

        towerDoors(x1 + 2, y1 + 1, z1 + 3, 00)
        towerDoors(x1 + 2, y1 + 1, z2 - 3, 00)
        towerDoors(x2 - 2, y1 + 1, z2 - 3, 00)
        towerDoors(x2 - 2, y1 + 1, z1 + 3, 00)
        towerDoors(x1 + 2, y2 + 1, z1 + 3, 00)
        towerDoors(x1 + 2, y2 + 1, z2 - 3, 00)
        towerDoors(x2 - 2, y2 + 1, z1 + 3, 00)
        towerDoors(x2 - 2, y2 + 1, z2 - 3, 00)

        towerwindows(x - 18, 2, z + 15)
        towerwindows(x - 18, 2, z - 15)
        towerwindows(x + 18, 2, z + 15)
        towerwindows(x + 18, 2, z - 15)
        towerwindows(x - 15, 2, z + 18)
        towerwindows(x - 15, 2, z - 18)
        towerwindows(x + 15, 2, z + 18)
        towerwindows(x + 15, 2, z - 18)

        hallsillsx(x1 + 6, y1 + 2, z2)
        hallsillsz(x1, y1 + 2, z1 + 6)
        hallsillsz(x2, y1 + 2, z1 + 6)

        windowsx(x1 + 6, y1 + 3, z2)
        windowsz(x1, y1 + 3, z1 + 6)
        windowsz(x2, y1 + 3, z1 + 6)

        # doorway(x1 + 13, y1 + 1, z1)
        drawbridge(x1 + 12, y1, z1 - 1)

        time.sleep(0.5)

        # ceiling lamps
        self.mc.setBlocks(x - 5, y + 11, z + -5, x + 5, y + 11, z + 5, 89)
        self.mc.setBlocks(x - 5, y + 10, z + -5, x + 5, y + 10, z + 5, 89)

        def drawGate(x, y, z):
            x1 = x - 2
            y1 = y + 1
            z1 = z - 15
            x2 = x + 2
            y2 = y + 5
            z2 = z - 15
            self.mc.setBlocks(x1, y1, z1, x2, y2, z2, 0)

        drawGate(x, y, z)

    def getAllFiles(self):
        # f = open(sys.path[0] + '/' + 'csvFiles' + '/' + 'house.csv', mode='r', encoding='utf-8-sig')
        dirs = sys.path[0] + '/' + 'csvFiles'
        csvList = os.listdir(dirs)
        return csvList

    def checkFileHad(self, filename):
        fileslist = self.getAllFiles()
        if filename in fileslist:
            return True
        else:
            return False

    def scan3D(self, player_name, filename, SIZEX, SIZEY, SIZEZ):
        """
        Scan an area and save the block data to a .csv file

        :param string player_name: player name
        :param string filename: .csv file
        :param int SIZEX: size in east and west direction, negative represents the west
        :param int SIZEY: size in vertical direction, negative represents the downward
        :param int SIZEZ: size in south and west direction, negative represents the north
        :return:
        """
        file_had = self.checkFileHad(filename)
        if file_had:
            logging.info("{}文件已经存在，如需覆盖请联系管理员".format(filename))
        else:
            logging.info("{}文件没有重名，请扫描完毕后通知管理员登记你的文件名，以防被别人覆盖".format(filename))

            pid = self.getPlayerId(player_name)
            pos = self.mc.entity.getTilePos(pid)
            originx, originy, originz = pos.x, pos.y, pos.z
            logging.info('3D扫描中... ...')
            # 使用读模式打开文件
            f = open(sys.path[0] + '/' + 'csvFiles' + '/' + filename, mode="w", encoding='utf-8-sig')
            # 把尺寸数据写到文件里
            f.write(str(abs(SIZEX)) + "," + str(abs(SIZEY)) + "," + str(abs(SIZEZ)) + "\n")

            for y in range(0, abs(SIZEY)):
                f.write("\n")
                for x in range(1, abs(SIZEX) + 1):
                    line = ""
                    for z in range(1, abs(SIZEZ) + 1):
                        if SIZEX > 0:
                            if SIZEZ > 0:
                                if SIZEY > 0:
                                    _block = self.mc.getBlockWithData(originx + x, originy + y, originz + z)
                                    # print('东南')
                                else:
                                    _block = self.mc.getBlockWithData(originx + x, originy - y, originz + z)
                                    # print("东南")
                            else:
                                if SIZEY > 0:
                                    _block = self.mc.getBlockWithData(originx + x, originy + y, originz - z)
                                    # print("东北")
                                else:
                                    _block = self.mc.getBlockWithData(originx + x, originy - y, originz - z)
                                    # print("东北")
                        else:
                            if SIZEZ > 0:
                                if SIZEY > 0:
                                    _block = self.mc.getBlockWithData(originx - x, originy + y, originz + z)
                                    # print("西南")
                                else:
                                    _block = self.mc.getBlockWithData(originx - x, originy - y, originz + z)
                                    # print("西南")
                            else:
                                if SIZEY > 0:
                                    _block = self.mc.getBlockWithData(originx - x, originy + y, originz - z)
                                    # print("西北")
                                else:
                                    _block = self.mc.getBlockWithData(originx - x, originy - y, originz - z)
                                    # print("西北")
                        blockid = _block.id
                        style = _block.data
                        # blockid 进行字符串处理变成3位数字符串
                        if blockid < 1:
                            blockid = "000"
                        elif blockid < 10:
                            blockid = "00" + str(blockid)
                        elif blockid < 100:
                            blockid = "0" + str(blockid)
                        else:
                            blockid = str(blockid)
                        # style方块样式变成2位数字符串
                        if style < 1:
                            style = "0" + str(style)
                        elif style < 10:
                            style = "0" + str(style)
                        else:
                            style = str(style)
                        # 把方块的id也加到line变量里
                        line = line + blockid + style
                        if line != "":
                            # line变量是非空，加一个逗号在后面
                            line = line + ","
                    f.write(line + "\n")
            f.close()
            logging.info('3D扫描完成')

    def print3D(self, player_name, filename, updown=True, t=0):
        """
        Paste

        :param string player_name: player's name
        :param string filename: .csv file
        :param updown: True-Normal, False-upside down
        :return:
        """
        file_had = self.checkFileHad(filename)
        if not file_had:
            logging.info("{}文件不存在，请确认文件名后使用{}".format(filename, self.getAllFiles()))
        else:
            # print("{}文件存在".format(filename))
            pid = self.getPlayerId(player_name)
            pos = self.mc.entity.getTilePos(pid)
            originx, originy, originz = pos.x, pos.y, pos.z
            f = open(sys.path[0] + '/' + 'csvFiles' + '/' + filename, mode='r', encoding='utf-8-sig')
            # 读取csv的每一行存到lines变量里
            lines = f.readlines()
            # 第一行读取立方体的尺寸大小数据
            coords = lines[0].split(",")
            sizex = int(coords[0])
            sizey = int(coords[1])
            sizez = int(coords[2])
            # 行数使用lineidx变量
            lineidx = 1

            if updown:
                logging.info('3D打印中... ...')
                for y in range(sizey):
                    lineidx = lineidx + 1
                    for x in range(sizex):
                        line = lines[lineidx]
                        lineidx = lineidx + 1
                        data = line.split(",")
                        for z in range(sizez):
                            # blockid = int(data[z][0:3])
                            # style = int(data[z][-2:])
                            try:
                                d = int(data[z])
                                blockID = d // 100
                                blockstyle = d % 100
                            except:
                                blockID = 0
                                blockstyle = 0
                            time.sleep(t)
                            self.mc.setBlock(originx + x + 1, originy + y, originz + z + 1, blockID, blockstyle)
            else:
                logging.info("3D打印中")
                for y in range(sizey):
                    lineidx = lineidx + 1
                    for x in range(sizex):
                        line = lines[lineidx]
                        lineidx = lineidx + 1
                        data = line.split(",")
                        for z in range(sizez):
                            # blockid = int(data[z][0:3])
                            # style = int(data[z][-2:])
                            try:
                                d = int(data[z])
                                blockID = d // 100
                                blockstyle = d % 100
                            except:
                                blockID = 0
                                blockstyle = 0
                            time.sleep(t)
                            self.mc.setBlock(originx + x + 1, originy - y, originz + z + 1, blockID, blockstyle)

            logging.info('3D打印完毕')

    def lantern(self, player_name, xoff=0, zoff=0, facing="east"):
        """
        在玩家身边放置一个路灯
        :param player_name: 玩家姓名
        :param xoff: 东西方向偏移量
        :param zoff: 南北方向偏移量
        :param facing: 灯的朝向 east、west、south、north
        """
        pid = self.getPlayerId(player_name)
        x, y, z = self.mc.entity.getTilePos(pid)
        if facing == "east":
            self.mc.setBlock(x + xoff, y, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 1, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 2, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 3, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 4, z + zoff, 85)
            self.mc.setBlock(x + xoff + 1, y + 4, z + zoff, 85)
            self.mc.setBlock(x + xoff + 1, y + 3, z + zoff, 169)
        elif facing == "west":
            self.mc.setBlock(x + xoff, y, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 1, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 2, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 3, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 4, z + zoff, 85)
            self.mc.setBlock(x + xoff - 1, y + 4, z + zoff, 85)
            self.mc.setBlock(x + xoff - 1, y + 3, z + zoff, 169)
        elif facing == 'south':
            self.mc.setBlock(x + xoff, y, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 1, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 2, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 3, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 4, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 4, z + zoff + 1, 85)
            self.mc.setBlock(x + xoff, y + 3, z + zoff + 1, 169)
        elif facing == "north":
            self.mc.setBlock(x + xoff, y, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 1, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 2, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 3, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 4, z + zoff, 85)
            self.mc.setBlock(x + xoff, y + 4, z + zoff - 1, 85)
            self.mc.setBlock(x + xoff, y + 3, z + zoff - 1, 169)

    def cobbleLantern(self, player_name='', xoff=0, zoff=0, color=0):
        """
        可变颜色的大石头路灯
        :param player_name: 玩家姓名
        :param xoff: 东西方向偏移量
        :param zoff: 南北方向偏移量
        :param color: 灯罩的颜色，0-15
        """
        pid = self.getPlayerId(player_name)
        x, y, z = self.mc.entity.getTilePos(pid)
        # 基座
        self.mc.setBlocks(x + xoff, y, z + zoff, x + xoff + 2, y + 1, z + zoff + 2, block.SANDSTONE)
        self.mc.setBlocks(x + xoff, y + 2, z + zoff, x + xoff + 2, y + 2, z + zoff + 2, block.SANDSTONE)
        # 柱子
        self.mc.setBlocks(x + xoff + 1, y + 3, z + zoff + 1, x + xoff + 1, y + 11, z + zoff + 1, 139)
        # 灯座
        self.mc.setBlocks(x + xoff, y + 12, z + zoff, x + xoff + 2, y + 12, z + zoff + 2, 139)
        self.mc.setBlock(x + xoff, y + 12, z + zoff, 0)
        self.mc.setBlock(x + xoff + 2, y + 12, z + zoff + 2, 0)
        self.mc.setBlock(x + xoff + 2, y + 12, z + zoff, 0)
        self.mc.setBlock(x + xoff, y + 12, z + zoff + 2, 0)
        self.mc.setBlocks(x + xoff, y + 13, z + zoff, x + xoff + 2, y + 13, z + zoff + 2, 139)  # cobble stone wall
        # 灯罩
        self.mc.setBlocks(x + xoff, y + 14, z + zoff, x + xoff + 2, y + 14, z + zoff + 2, 160, color)
        self.mc.setBlock(x + xoff + 1, y + 14, z + zoff + 1, 0)
        self.mc.setBlock(x + xoff + 1, y + 14, z + zoff + 1, 169)  # 灯芯，海晶灯
        self.mc.setBlocks(x + xoff, y + 15, z + zoff, x + xoff + 2, y + 15, z + zoff + 2, 44, 3)  # 灯顶
        self.mc.setBlock(x + xoff + 1, y + 15, z + zoff + 1, 43, 3)  # 灯芯，海晶灯
        self.mc.setBlock(x + xoff + 1, y + 16, z + zoff + 1, 139)  # 灯芯，海晶灯

        # <------------------------------------------------------------------->
        # deprecated
        # 魔法阵展示需要的代码
        # 准备淘汰，把课程展示那里的代码改成
        # ministack.drawPentacleByPlayer('xiaozhan', step, 35, 4) step大小老师上课前自己测试好
        def drawPentacle_mini(self, h, blockID, style):
            point1 = self.getPoint(8, h, -6)
            point2 = self.getPoint(8, h, 6)
            point3 = self.getPoint(-4, h, 9)
            point4 = self.getPoint(-10, h, 0)
            point5 = self.getPoint(-4, h, -9)
            self.drawLineByPoints(point1, point3, blockID, style)
            self.drawLineByPoints(point1, point4, blockID, style)
            self.drawLineByPoints(point2, point4, blockID, style)
            self.drawLineByPoints(point2, point5, blockID, style)
            self.drawLineByPoints(point3, point5, blockID, style)

        # 写死的五角星函数, deprecated
        def drawPentacle(self, h, blockID, style):
            point1 = self.getPoint(23, h, -12)
            point2 = self.getPoint(18, h, 17)
            point3 = self.getPoint(-12, h, 23)
            point4 = self.getPoint(-26, h, -4)
            point5 = self.getPoint(-5, h, -26)
            self.drawLineByPoints(point1, point3, blockID, style)
            self.drawLineByPoints(point1, point4, blockID, style)
            self.drawLineByPoints(point2, point4, blockID, style)
            self.drawLineByPoints(point2, point5, blockID, style)
            self.drawLineByPoints(point3, point5, blockID, style)

    def pave(self, x, z, x1, z1, blockID=35, style=0, spd=0):
        """
        铺设道路，从(x, ~, z)到(x1, ~, z1), 高度按照地形
        :param int x: 起点坐标x
        :param int z: 起点坐标z
        :param int x1: 起点坐标x1
        :param int z1: 起点坐标z1
        :param int blockID: 道路材质
        :param int style: 道路材质的样式
        :param int spd: 建造速度
        """
        ew = x1 - x + 1
        sn = z1 - z
        ait = AITurtle(self.address)
        y = self.getHeight(x, z)  # 起点 海拔
        ait.setposition(x, y, z)
        ait.walk()
        ait.penblock(blockID, style)
        ait.speed(spd)
        # 铺路
        for i in range(ew):
            ysn = self.getHeight(x + i, z)
            ait.setposition(x + i, ysn, z)  # 每一列的起点
            yen = self.getHeight(x + i, z + sn)
            ait.goto(x + i, yen, z + sn)  # 每一列的终点

        # 擦除海龟方块
        y1 = self.getHeight(ait.position.x, ait.position.z)  # 终点海拔
        ait._clearTurtle(ait.position.x, y1, ait.position.z)
        v0 = vec3.Vec3(x, y, z)
        v1 = vec3.Vec3(x1, y1, z1)
        logging.info("pave {} {} blockID:{} style:{}".format(v0, v1, blockID, style))


class AITurtle(MinecraftTurtle):
    def __init__(self, address='101.200.42.193', port=4711, position=vec3.Vec3(0, 0, 0), offset_front=(1, 0),
                 offset_left=(0, -1),
                 offset_right=(0, 1)):
        """
        A clever MinecraftTurtle that can detect the id of front, left and right block.

        :param mc:
        :param position: AI turtle's position
        :param offset_front: the relative position front to you
        :param offset_left: the relative position left to you
        :param offset_right: the relative position right to you
        """
        mc = minecraft.Minecraft.create(address, port)
        super().__init__(mc, position)
        self.offset_front = offset_front
        self.offset_left = offset_left
        self.offset_right = offset_right

    def goto(self, x, y, z):
        """
        move to a position
        :param x: turtle's x coordinate
        :param y: turtle's y coordinate
        :param z: turtle's z coordinate
        """
        super()._moveTurtle(x, y, z)

    # def right(self, angle):
    #     """
    #     Rotate the turtle right
    #     Overrides the method to hold the negative degrees and big degrees And show the right heading
    #     :param float angle:
    #         the angle in degrees to rotate.
    #     """
    #     # rotate turtle angle to the right
    #     if 0 < self.heading < 360 and 0 < angle < 360:
    #         self.heading = self.heading + angle

    # def left(self, angle):
    #     """
    #     Rotate the turtle left
    #     Overrides the method to hold the negative degrees and big degrees And show the right heading
    #     :param float angle:
    #         the angle in degrees to rotate.
    #     """
    #     # rotate turtle angle to the left
    #     if 0 < self.heading < 360 and 0 < angle < 360:
    #         self.heading = self.heading - angle

    # def forward(self, distance):
    #     super().forward(distance)
    # def backward(self, distance):
    #     super().backward(distance)
    #
    # def setposition(self, x, y, z):
    #     super().setposition(x, y, z)

    def offset(self):
        """
        0/ 360: east
        90: south
        180: west
        270: north

        :return: ((frontOffset), (leftOffset), (rightOffset))
        """
        hd = self.heading
        if hd == 0 or hd == 360:
            # print("E")
            self.offset_front = (1, 0)
            self.offset_left = (0, -1)
            self.offset_right = (0, 1)
        elif hd == 90 or hd == 70:
            # print("S")
            self.offset_front = (0, 1)
            self.offset_left = (1, 0)
            self.offset_right = (-1, 0)
        elif hd == 180:
            # print("W")
            self.offset_front = (-1, 0)
            self.offset_left = (0, 1)
            self.offset_right = (0, -1)
        elif hd == 270:
            # print("N")
            self.offset_front = (0, -1)
            self.offset_left = (-1, 0)
            self.offset_right = (1, 0)
        # print(self.offset_front, self.offset_left, self.offset_right)
        return self.offset_front, self.offset_left, self.offset_right

    def getFrontBlockPos(self):
        x = self.position.x + self.offset()[0][0]
        y = self.position.y
        z = self.position.z + self.offset()[0][1]
        vec_front = vec3.Vec3(x, y, z)
        return vec_front
        pass

    def getLeftBlockPos(self):
        x = self.position.x + self.offset()[1][0]
        y = self.position.y
        z = self.position.z + self.offset()[1][1]
        vec_left = vec3.Vec3(x, y, z)
        return vec_left

    def getRightBlockPos(self):
        x = self.position.x + self.offset()[2][0]
        y = self.position.y
        z = self.position.z + self.offset()[2][1]
        vec_right = vec3.Vec3(x, y, z)
        return vec_right

    # def auto(self):
    #     front_block_id = self.getFrontBlockPos()
    #     right_block_id = self.getRightBlockPos()
    #     if front_block_id == 0:
    #         self.forward(1)
    #     else:
    #         if right_block_id == 0:
    #             self.right(90)
    #             self.forward(1)
    #         else:
    #             self.left((90))
    #             self.forward(1)

    # fd = forward
    # bk = backward
    # rt = right
    # lt = left
    # goto = setposition
    # setpos = setposition


# DFA算法
class DFAFilter(object):
    def __init__(self):
        self.keyword_chains = {}  # 关键词链表
        self.delimit = '\x00'  # 限定

    def add(self, keyword):
        keyword = keyword.lower()  # 关键词英文变为小写
        chars = keyword.strip()  # 关键字去除首尾空格和换行
        if not chars:  # 如果关键词为空直接返回
            return
        level = self.keyword_chains
        # 遍历关键字的每个字
        for i in range(len(chars)):
            # 如果这个字已经存在字符链的key中就进入其子字典
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def parse(self, filename):
        with open(sys.path[0] + '/' + filename, mode='r', encoding='utf-8-sig') as f:
            for keyword in f:
                self.add(str(keyword).strip())
        # print(self.keyword_chains)

    def filter(self, message, repl=""):
        message = str(message).lower()
        ret = []
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        ret.append(repl * step_ins)
                        start += step_ins - 1
                        break
                else:
                    ret.append(message[start])
                    break
            else:
                ret.append(message[start])
            start += 1

        return ''.join(ret)

# # api使用类
# class apiGetMsg():
#     def __init__(self, apiUrl, apiKey):
#         self.apiUrl = apiUrl
#         self.apiKey = apiKey
#
#     def get_response(self, msg):
#         data = {
#             # "Content-Type: application/json"
#             'x-api-key': self.apiKey,
#             'content': msg,
#             "type": 1
#         }
#         try:
#             r = requests.post(self.apiUrl, data=data).json()
#             return r
#             # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
#             # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
#             # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
#         except:
#             # 将会返回一个None
#             return None

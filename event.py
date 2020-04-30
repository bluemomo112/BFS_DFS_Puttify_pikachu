# encoding: utf-8
from .vec3 import Vec3


class BlockEvent:
    """An Event related to blocks (e.g. placed, removed, hit)"""
    """检测玩家使用Sword右键操作砖块"""
    HIT = 0

    def __init__(self, type, x, y, z, face, entityId):
        self.type = type
        self.pos = Vec3(x, y, z)
        self.face = face
        self.entityId = entityId

    def __repr__(self):
        sType = {
            BlockEvent.HIT: "BlockEvent.HIT"
        }.get(self.type, "???")

        return "BlockEvent(%s, %d, %d, %d, %d, %d)" % (
            sType, self.pos.x, self.pos.y, self.pos.z, self.face, self.entityId);

    @staticmethod
    def Hit(x, y, z, face, entityId):
        """

        :param x: 玩家击打的坐标x位置
        :param y: 玩家击打的坐标y位置
        :param z: 玩家击打的坐标z位置
        :param face: 玩家击打的砖块哪一面：up n s w e bottom : 1 2 3 4 5 6
        :param entityId: 玩家ID 谁打的砖块
        :return: <class 'mcpi.event.BlockEvent'>

        e.g.
        import mcpi.minecraft as minecraft
        import mcpi.minecraftstuff as minecraftstuff
        from mcpi import vec3

        mc = minecraft.Minecraft.create()
        mcDrawing = minecraftstuff.MinecraftDrawing(mc)
        vec = vec3.Vec3()
        player = "xiaozhan"
        id = mc.getPlayerEntityId(player)
        print(id)
        pos = mc.entity.getPos(id)
        x, y, z = pos.x, pos.y, pos.z

        while True:
            events = mc.events.pollBlockHits()
            for e in events:
                print(e, type(e))

        output: BlockEvent(BlockEvent.HIT, 8, 16, 4, 5, 37)
        """
        return BlockEvent(BlockEvent.HIT, x, y, z, face, entityId)


class ChatEvent:
    """An Event related to chat (e.g. posts)"""
    POST = 0

    def __init__(self, type, entityId, message):
        self.type = type
        self.entityId = entityId
        self.message = message

    def __repr__(self):
        sType = {
            ChatEvent.POST: "ChatEvent.POST"
        }.get(self.type, "???")

        return "ChatEvent(%s, %d, %s)" % (
            sType, self.entityId, self.message);

    @staticmethod
    def Post(entityId, message):
        return ChatEvent(ChatEvent.POST, entityId, message)

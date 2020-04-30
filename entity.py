# encoding: utf-8
class Entity:
    '''Minecraft PI entity description. Can be sent to Minecraft.spawnEntity'''

    def __init__(self, id, name=None):
        self.id = id
        self.name = name

    def __cmp__(self, rhs):
        return hash(self) - hash(rhs)

    def __eq__(self, rhs):
        return self.id == rhs.id

    def __hash__(self):
        return self.id

    def __iter__(self):
        '''Allows an Entity to be sent whenever id is needed'''
        return iter((self.id,))

    def __repr__(self):
        return 'Entity(%d)' % (self.id)


EXPERIENCE_ORB = Entity(2, "EXPERIENCE_ORB")  # 经验值
AREA_EFFECT_CLOUD = Entity(3, "AREA_EFFECT_CLOUD")  # 效果区域云
ELDER_GUARDIAN = Entity(4, "ELDER_GUARDIAN")  # 远古守卫者
WITHER_SKELETON = Entity(5, "WITHER_SKELETON")  # 凋零骷髅
STRAY = Entity(6, "STRAY")  # 流浪者
EGG = Entity(7, "EGG") # 蛋
LEASH_HITCH = Entity(8, "LEASH_HITCH")  # 没找到对应的实体
PAINTING = Entity(9, "PAINTING")  # 画
ARROW = Entity(10, "ARROW")  # 箭
SNOWBALL = Entity(11, "SNOWBALL")  # 雪球
FIREBALL = Entity(12, "FIREBALL")  # 火球
SMALL_FIREBALL = Entity(13, "SMALL_FIREBALL")  # 小火球
ENDER_PEARL = Entity(14, "ENDER_PEARL")  # 末影珍珠
ENDER_SIGNAL = Entity(15, "ENDER_SIGNAL")  # 末影之眼
THROWN_EXP_BOTTLE = Entity(17, "THROWN_EXP_BOTTLE")  # 扔掉的经验瓶子
ITEM_FRAME = Entity(18, "ITEM_FRAME")  # 物品展示框，无法使用
WITHER_SKULL = Entity(19, "WITHER_SKULL")  # 凋零骷髅，可以看成是发射炮弹
PRIMED_TNT = Entity(20, "PRIMED_TNT")  # 待发的TNT（生成的时候已经是激活状态） #  课堂管理
HUSK = Entity(23, "HUSK")  # 尸壳（攻击力比较大，是僵尸的变种之一）
SPECTRAL_ARROW = Entity(24, "SPECTRAL_ARROW")  # 光灵箭
SHULKER_BULLET = Entity(25, "SHULKER_BULLET")  # 浅影贝（无法使用，掉落会消失）
DRAGON_FIREBALL = Entity(26, "DRAGON_FIREBALL")  # 末影龙火球
ZOMBIE_VILLAGER = Entity(27, "ZOMBIE_VILLAGER")  # 僵尸村民
SKELETON_HORSE = Entity(28, "SKELETON_HORSE")  # 骷髅马
ZOMBIE_HORSE = Entity(29, "ZOMBIE_HORSE")  # 僵尸马
ARMOR_STAND = Entity(30, "ARMOR_STAND")  # 盔甲架
DONKEY = Entity(31, "DONKEY")  # 驴
MULE = Entity(32, "MULE")  # 骡
EVOKER_FANGS = Entity(33, "EVOKER_FANGS")  # 尖牙
EVOKER = Entity(34, "EVOKER")  # 唤魔者（尖牙，恼鬼）
VEX = Entity(35, "VEX")  # 恼鬼
VINDICATOR = Entity(36, "VINDICATOR")  # 卫道士
ILLUSIONER = Entity(37, "ILLUSIONER")  # 幻术师
MINECART_COMMAND = Entity(40, "MINECART_COMMAND")  # 命令方块矿车
BOAT = Entity(41, "BOAT")  # 船
MINECART = Entity(42, "MINECART")  # 漏斗矿车
MINECART_CHEST = Entity(43, "MINECART_CHEST")  # 带箱子的矿车
MINECART_FURNACE = Entity(44, "MINECART_FURNACE")  # 动力矿车或熔炉矿车
MINECART_TNT = Entity(45, "MINECART_TNT")  # TNT矿石车
MINECART_HOPPER = Entity(46, "MINECART_HOPPER")  # 漏斗矿车
MINECART_MOB_SPAWNER = Entity(47, "MINECART_MOB_SPAWNER")
CREEPER = Entity(50, "CREEPER")  # 爬行者
SKELETON = Entity(51, "SKELETON")  # 骨架
SPIDER = Entity(52, "SPIDER")  # 蜘蛛
GIANT = Entity(53, "GIANT")  # 巨人
ZOMBIE = Entity(54, "ZOMBIE")  # 僵尸
SLIME = Entity(55, "SLIME")  # 粘液
GHAST = Entity(56, "GHAST")  # 地狱幽灵
PIG_ZOMBIE = Entity(57, "PIG_ZOMBIE")  # 僵尸猪
ENDERMAN = Entity(58, "ENDERMAN")  # 末影
CAVE_SPIDER = Entity(59, "CAVE_SPIDER")  # 洞穴蜘蛛
SILVERFISH = Entity(60, "SILVERFISH")  # 银鱼
BLAZE = Entity(61, "BLAZE")  # 火焰
MAGMA_CUBE = Entity(62, "MAGMA_CUBE")  # 岩浆立方体
ENDER_DRAGON = Entity(63, "ENDER_DRAGON")  # 末影龙
WITHER = Entity(64, "WITHER")  # 枯萎者
BAT = Entity(65, "BAT")  # 蝙蝠
WITCH = Entity(66, "WITCH")  # 女巫
ENDERMITE = Entity(67, "ENDERMITE")  # 末影蟎
GUARDIAN = Entity(68, "GUARDIAN")  # 守卫者
SHULKER = Entity(69, "SHULKER")  # 界伏蚌
PIG = Entity(90, "PIG")  # 猪
SHEEP = Entity(91, "SHEEP")  # 羊
COW = Entity(92, "COW")  # 牛
CHICKEN = Entity(93, "CHICKEN")  # 鸡
SQUID = Entity(94, "SQUID")  # 乌贼
WOLF = Entity(95, "WOLF")  # 狼
MUSHROOM_COW = Entity(96, "MUSHROOM_COW")  # 蘑菇牛
SNOWMAN = Entity(97, "SNOWMAN")  # 雪人
OCELOT = Entity(98, "OCELOT")  # 山猫
IRON_GOLEM = Entity(99, "IRON_GOLEM")  # 铁傀儡
HORSE = Entity(100, "HORSE")  # 马
RABBIT = Entity(101, "RABBIT")  # 兔子
POLAR_BEAR = Entity(102, "POLAR_BEAR")  # 北极熊
LLAMA = Entity(103, "LLAMA")  # 羊驼
LLAMA_SPIT = Entity(104, "LLAMA_SPIT")  # 骆驼
PARROT = Entity(105, "PARROT")  # 鹦鹉
VILLAGER = Entity(120, "VILLAGER")  # 村民
ENDER_CRYSTAL = Entity(200, "ENDER_CRYSTAL")  # 末影水晶

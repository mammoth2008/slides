在设计这个关系型数据库时，我们需要思考《王者荣耀》游戏的主要组成部分以及他们之间的关系。我们可以包括以下几个表：

1. `用户表 (Users)`：包含所有玩家的信息
   - 用户ID
   - 用户名
   - 用户密码
   - 注册日期
   - 最后登录日期
   - 游戏等级
   - 胜利场次
   - 失败场次
   
2. `英雄表 (Heroes)`：包含所有可用英雄的信息
   - 英雄ID
   - 英雄名称
   - 英雄类型
   - 英雄生命值
   - 英雄攻击力
   - 英雄描述
   
3. `用户英雄表 (UserHeroes)`：展示每个用户拥有哪些英雄
   - 用户ID
   - 英雄ID
   - 获取日期
   - 英雄等级
   - 英雄经验值

4. `比赛表 (Matches)`：记录比赛的相关信息
   - 比赛ID
   - 开始时间
   - 结束时间
   - 胜利方（用户ID）

5. `比赛参与表 (MatchParticipation)`：记录比赛中哪些玩家参与以及他们使用的英雄
   - 比赛ID
   - 用户ID
   - 英雄ID
   - 击杀数
   - 死亡数
   - 助攻数
   - 经验值

以上表格是一个基础的关系型数据库设计。你可以通过这个设计理解一些数据库的基本概念，如主键、外键、表连接等等。

1. 主键（Primary Key）：每个表都有主键，用于唯一标识表中的每一行。例如，在用户表中，用户ID就是主键。

2. 外键（Foreign Key）：在一个表中引用另一个表的主键。例如，在用户英雄表中，用户ID和英雄ID就是外键，它们分别引用了用户表和英雄表的主键。

3. 表连接（Table Join）：通过外键将两个或更多的表联接起来，以便能够从不同的表中获取相关联的数据。例如，我们可以通过用户ID将用户表和用户英雄表连接起来，这样就可以找到每个用户拥有的所有英雄。



很好，让我们继续下一步。这是创建英雄表的 SQL 代码，我们可以看到其中稍微有一些改进「「「/* 创建英雄表 */
CREATE TABLE Heroes (
    HeroID INT UNSIGNED AUTO_INCREMENT,     /* 英雄ID，自增 */
    HeroName VARCHAR(50) NOT NULL,          /* 英雄名 */
    HeroType VARCHAR(30) NOT NULL,          /* 英雄类型 */
    HeroDifficultyLevel INT NOT NULL,       /* 英雄难度级别 */
    HeroLife INT NOT NULL,                  /* 英雄生命值 */
    HeroAttack INT NOT NULL,                /* 英雄攻击力 */
    HeroDescription TEXT,                   /* 英雄描述 */
    PRIMARY KEY (HeroID)                    /* 设置主键为HeroID */
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
」」」请根据你对游戏《王者荣耀》（Honor of Kings或Arena of Valor）的理解，产生 50 条英雄数据，逐一列出它们，返回将它们添加到 Users 表中的 SQL 代码。
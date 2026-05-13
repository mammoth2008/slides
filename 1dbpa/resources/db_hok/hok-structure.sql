
/* 创建数据库 HOK 
CREATE DATABASE IF NOT EXISTS HOK;
USE HOK;
*/
/* 创建用户表 */
CREATE TABLE Users (
    UserID INT UNSIGNED AUTO_INCREMENT,     /* 用户ID，自增 */
    UserName VARCHAR(50) NOT NULL,          /* 用户名 */
    UserPassword VARCHAR(50) NOT NULL,      /* 用户密码 */
    RegisterDate DATE NOT NULL,             /* 注册日期 */
    LastLoginDate DATE,                     /* 最后登录日期 */
    GameLevel INT NOT NULL,                 /* 游戏等级 */
    Wins INT DEFAULT 0,                     /* 胜利场次 */
    Losses INT DEFAULT 0,                   /* 失败场次 */
    PRIMARY KEY (UserID)                    /* 设置主键为UserID */
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 创建英雄表 */
CREATE TABLE Heroes (
    HeroID INT UNSIGNED AUTO_INCREMENT,     /* 英雄ID，自增 */
    HeroName VARCHAR(50) NOT NULL,          /* 英雄名 */
    HeroType VARCHAR(30) NOT NULL,          /* 英雄类型 */
    HeroLife INT NOT NULL,                  /* 英雄生命值 */
    HeroAttack INT NOT NULL,                /* 英雄攻击力 */
    HeroDescription TEXT,                   /* 英雄描述 */
    PRIMARY KEY (HeroID)                    /* 设置主键为HeroID */
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 创建用户英雄表 */
CREATE TABLE UserHeroes (
    UserID INT UNSIGNED,                    /* 用户ID */
    HeroID INT UNSIGNED,                    /* 英雄ID */
    ObtainDate DATE NOT NULL,               /* 获取日期 */
    HeroLevel INT DEFAULT 1,                /* 英雄等级 */
    HeroExperience INT DEFAULT 0,           /* 英雄经验值 */
    PRIMARY KEY (UserID, HeroID),           /* 设置复合主键为UserID和HeroID */
    FOREIGN KEY (UserID) REFERENCES Users(UserID), /* 设置UserID为外键，引用Users表的UserID */
    FOREIGN KEY (HeroID) REFERENCES Heroes(HeroID) /* 设置HeroID为外键，引用Heroes表的HeroID */
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 创建比赛表 */
CREATE TABLE Matches (
    MatchID INT UNSIGNED AUTO_INCREMENT,    /* 比赛ID，自增 */
    StartTime DATETIME NOT NULL,            /* 开始时间 */
    EndTime DATETIME,                       /* 结束时间 */
    WinnerID INT UNSIGNED,                  /* 胜利方用户ID */
    PRIMARY KEY (MatchID),                  /* 设置主键为MatchID */
    FOREIGN KEY (WinnerID) REFERENCES Users(UserID) /* 设置WinnerID为外键，引用Users表的UserID */
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/* 创建比赛参与表 */
CREATE TABLE MatchParticipation (
    MatchID INT UNSIGNED,                   /* 比赛ID */
    UserID INT UNSIGNED,                    /* 用户ID */
    HeroID INT UNSIGNED,                    /* 英雄ID */
    Kills INT DEFAULT 0,                    /* 击杀数 */
    Deaths INT DEFAULT 0,                   /* 死亡数 */
    Assists INT DEFAULT 0,                  /* 助攻数 */
    ExperienceGained INT DEFAULT 0,         /* 获取的经验值 */
    PRIMARY KEY (MatchID, UserID),          /* 设置复合主键为MatchID和UserID */
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID), /* 设置MatchID为外键，引用Matches表的MatchID */
    FOREIGN KEY (UserID) REFERENCES Users(UserID),     /* 设置UserID为外键，引用Users表的UserID */
    FOREIGN KEY (HeroID) REFERENCES Heroes(HeroID)     /* 设置HeroID为外键，引用Heroes表的HeroID */
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

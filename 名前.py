from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

# SQLite 使用時
# SQLite - File（通常のファイル保存）
engine = create_engine('sqlite:///sample_db.sqlite3')  # スラッシュは3本

# SQLログを表示したい場合には echo=True を指定
engine = create_engine('sqlite:///sample_db.sqlite3', echo=True)



# モデルの作成
# 説明のためファイル内に定義しますが、実際は別ファイル化して import します。

# まずベースモデルを生成します
Base = declarative_base()

class User(Base):
    """
    生徒モデル
    必ず Base を継承
    """
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    age = Column(Integer)  # 点数

    def __repr__(self):
        return "<User(id='%s', name='%s', age='%s')>" % (self.id, self.name, self.age)

Base.metadata.create_all(engine)  # 作成した engine を引数にすること


# SQLAlchemy はセッションを介してクエリを実行する

Session = sessionmaker(bind=engine)
session = Session()

# 1レコードの追加
session.add(User(id=1, name='露亜（ろあ）', age=12))


# 複数レコードの追加
session.add_all([
    User(id=5, name='露衣（ろい）', age=34),
    User(id=7, name='露維埜（ろいの）', age=56),
])
# コミット（データ追加を実行）
session.commit()
# 全件取得
result = session.query(User).all()  # .all() は省略可
for user in result:
    print(user.name, user.age)
    """

　　露亜（ろあ） 12

　　露衣（ろい） 34

　　露維埜（ろいの） 56

　　朗沙（ろうざ） 65

　　朗咲（ろうざ）78
    """
for user in session.query(User).filter(User.age < 70):
    print(user.name)
    """
    朗咲（ろうざ）
    """
# セッション・クローズ
# DB処理が不要になったタイミングやスクリプトの最後で実行
session.close()


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


# 次にベースモデルを継承してモデルクラスを定義します
class Student(Base):
    """
    生徒モデル
    必ず Base を継承
    """
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    score = Column(Integer)  # 点数

    def __repr__(self):
        return "<Student(id='%s', name='%s', score='%s')>" % (self.id, self.name, self.score)

Base.metadata.create_all(engine)  # 作成した engine を引数にすること


# SQLAlchemy はセッションを介してクエリを実行する

Session = sessionmaker(bind=engine)
session = Session()

# 1レコードの追加
#session.add(Student(id=1, name='Suzuki', score=70))


# 複数レコードの追加
#session.add_all([
    #Student(id=5, name='Yamada', score=73),
#    Student(id=7, name='Watanabe', score=88),
#])
# コミット（データ追加を実行）
#session.commit()
# 全件取得
result = session.query(Student).all()  # .all() は省略可
for student in result:
    print(student.name, student.score)
    """
    Suzuki 70
    Yamada 73
    Watanabe 88
    Tanaka 65
    """
for student in session.query(Student).filter(Student.score < 70):
    print(student.name)
    """
    Yamada
    """
# セッション・クローズ
# DB処理が不要になったタイミングやスクリプトの最後で実行
session.close()

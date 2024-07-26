from sqlalchemy import create_engine, Column, String, Integer, Sequence, TIMESTAMP, Boolean, Enum, select, ForeignKey, update
from urllib.parse import urlparse, parse_qs
from sqlalchemy.orm import sessionmaker, relationship, joinedload, declarative_base
from sqlalchemy.exc import DuplicateColumnError
from typing import Any, TypedDict, cast
from sqlalchemy.sql import func
from typing import Optional
from loguru import logger
from config import config
# from datetime import datetime
  
Base = declarative_base()


class Tables():
  class Playlist(Base):
    __tablename__ = 'playlists'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String, default=None)
    url = Column(String, unique=True)
    queue_status = Column(Enum('queued', 'completed', name='queue_status'), default='queued')
    create_time = Column(TIMESTAMP, default=func.now())
    downloaded_time = Column(TIMESTAMP, default=None)
    downloaded_items = relationship('Downloaded', back_populates='playlist')

  class Downloaded(Base):
    __tablename__ = 'downloaded'
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)
    playlist_url = Column(String, ForeignKey('playlists.url'))
    url = Column(String)
    path = Column(String)
    elapsed = Column(String)
    create_time = Column(TIMESTAMP, default=func.now())
    playlist = relationship('Playlist', back_populates='downloaded_items')

  class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    Username = Column(String, default=None, unique=True)
    password = Column(String(50))
    salt = Column(String())


def spliturl(url: list):
  """Splits url and returns the youtube video/playlist id

  Args:
      url (string): Youtube url Eg: https://www.youtube.com/watch?v=sVJEaYNOUNw&t=162s

  Returns:
      string: End of youtube url
  """
  parsed_url = urlparse(url) #type: ignore

  query_params = parse_qs(parsed_url.query)
  video_id = query_params.get('v')
  playlist_id = query_params.get('list')
  if not playlist_id == None:
      url.append(playlist_id)
  else:
      url.append(video_id)
  return url


class interactions:
  def __init__(self):
    session = sessionmaker()
    self.engine = create_engine(
      f'postgresql+psycopg2://{config.db.user}@{config.db.host}:{config.db.port}/{config.db.db}',
      pool_size=5,
      max_overflow=0,
      echo=False,
      connect_args={"options": f"-c timezone={config.db.timezone}"}
      )
    self.stmt = (

    )
    

   
  def createEntry(self, title, url, datetime):
    try:
      conn = self.engine.connect()
      entry=Tables.Playlist(title=None, url=url)
      return 'Successfull'
    except DuplicateColumnError as e:
      return {
        'data':{
        'message': 'Url Already Exists',
        'error': e
        }
      }

  def getQueued(self):
    pass

  def test(self):
    pass

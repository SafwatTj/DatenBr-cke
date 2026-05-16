# models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from database import Base
from datetime import datetime

class Dokument(Base):
    __tablename__ = "dokumente"

    id = Column(Integer, primary_key=True, index=True)
    dateiname = Column(String(255), nullable=False)
    quelle = Column(String(50), nullable=False)  # 'excel' oder 'pdf'
    daten_inhalt = Column(Text, nullable=True)   # JSON als String
    erstellt_am = Column(DateTime, default=datetime.now)
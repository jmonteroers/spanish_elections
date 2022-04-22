from sqlalchemy.orm import declarative_base, relationship

from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey


Base = declarative_base()


class Election(Base):
    """Table with metadata about an election.

    Fields
        - Date
        - Type: congreso, senado
    """
    __tablename__ = "elections"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    type = Column(String(50), nullable=False)


class ProvinceResult(Base):
    """Table with the overall results in a province per election

    Schema:
        - Election
        - ProvinceName
        - ProvinceId
        - TotalSeats
        - Ballots
        - Null ballots
        - Blank ballots
        - Abstentions
    """
    __tablename__ = "province_results"

    id = Column(Integer, primary_key=True)
    province_name = Column(String, nullable=False)
    province_id = Column(Integer, nullable=False)
    total_seats = Column(Integer)
    perc_counted = Column(Float)
    ballots = Column(Integer)
    null_ballots = Column(Integer)
    blank_ballots = Column(Integer)
    abstentions = Column(Integer)
    election_id = Column(Integer, ForeignKey("elections.id"))
    election = relationship("Election", back_populates="province_results")
    

class PPartyResult(Base):
    """Table with the results by political parties, per province in a election

    Schema:
        - ProvinceElectionResult
        - PoliticalPartyName
        - PoliticalPartyId
        - Ballots
        - Seats
    """
    __tablename__ = "pparty_results"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    pparty_id = Column(Integer, nullable=False)
    ballots = Column(Integer)
    seats = Column(Integer)
    province_result_id = Column(Integer, ForeignKey("province_results.id"))
    province_result = relationship("ProvinceResult", back_populates="results_per_pparty")


def create_databases(engine):
    Election.province_results = relationship("ProvinceResult", back_populates="election")
    ProvinceResult.results_per_pparty = relationship("PPartyResult", back_populates="province_result")
    Base.metadata.create_all(engine)
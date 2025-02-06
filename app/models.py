# app/models.py
from sqlalchemy import Column, String, Numeric
from .database import Base

class SupportItem(Base):
    __tablename__ = "support_items"
    
    support_item_number = Column(String, primary_key=True, index=True)
    support_item_name = Column(String, nullable=False)
    registration_group_number = Column(String)
    registration_group_name = Column(String)
    support_category_number = Column(String)
    support_category_number_pace = Column(String)
    support_category_name = Column(String)
    support_category_name_pace = Column(String)
    unit = Column(String)
    quote = Column(String)
    start_date = Column(String)  # Consider using Date if needed.
    end_date = Column(String)
    
    # Price fields as numeric columns (up to 10 digits with 2 decimal places)
    act = Column(Numeric(10, 2))
    nsw = Column(Numeric(10, 2))
    nt = Column(Numeric(10, 2))
    qld = Column(Numeric(10, 2))
    sa = Column(Numeric(10, 2))
    tas = Column(Numeric(10, 2))
    vic = Column(Numeric(10, 2))
    wa = Column(Numeric(10, 2))
    
    remote = Column(Numeric(10, 2))
    very_remote = Column(Numeric(10, 2))
    
    non_face_to_face_support_provision = Column(String)
    provider_travel = Column(String)
    short_notice_cancellations = Column(String)
    ndia_requested_reports = Column(String)
    irregular_sil_supports = Column(String)
    type = Column(String)
    
    def as_dict(self):
        return {
            "support_item_number": self.support_item_number,
            "support_item_name": self.support_item_name,
            "registration_group_number": self.registration_group_number,
            "registration_group_name": self.registration_group_name,
            "support_category_number": self.support_category_number,
            "support_category_number_pace": self.support_category_number_pace,
            "support_category_name": self.support_category_name,
            "support_category_name_pace": self.support_category_name_pace,
            "unit": self.unit,
            "quote": self.quote,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "act": float(self.act) if self.act is not None else None,
            "nsw": float(self.nsw) if self.nsw is not None else None,
            "nt": float(self.nt) if self.nt is not None else None,
            "qld": float(self.qld) if self.qld is not None else None,
            "sa": float(self.sa) if self.sa is not None else None,
            "tas": float(self.tas) if self.tas is not None else None,
            "vic": float(self.vic) if self.vic is not None else None,
            "wa": float(self.wa) if self.wa is not None else None,
            "remote": float(self.remote) if self.remote is not None else None,
            "very_remote": float(self.very_remote) if self.very_remote is not None else None,
            "non_face_to_face_support_provision": self.non_face_to_face_support_provision,
            "provider_travel": self.provider_travel,
            "short_notice_cancellations": self.short_notice_cancellations,
            "ndia_requested_reports": self.ndia_requested_reports,
            "irregular_sil_supports": self.irregular_sil_supports,
            "type": self.type,
        }

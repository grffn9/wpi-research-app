from datetime import datetime, timezone
from typing import Optional

from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

from app.auth.auth_models import User

class Faculty(User):
    __tablename__='faculty'

    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    is_verified: sqlo.Mapped[bool] = sqlo.mapped_column(default=False)
    
    __mapper_args__ = {
    'polymorphic_identity': 'Faculty'
    }
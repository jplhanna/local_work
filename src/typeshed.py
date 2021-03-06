from dataclasses import dataclass
from dataclasses import field
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import TYPE_CHECKING
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import TypedDict
from typing import Union

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy.orm import RelationshipProperty
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.sql import ColumnElement
from sqlalchemy.sql import FromClause
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy.sql.elements import Label
from sqlalchemy.sql.functions import Function
from sqlalchemy.sql.selectable import CTE

if TYPE_CHECKING:
    from src.helpers.sqlalchemy_helpers import BaseModel  # noqa

    BooleanColumnElement = ColumnElement[Boolean]
else:
    BooleanColumnElement = ColumnElement


class DBConfigDict(TypedDict):
    database_uri: str
    async_database_uri: str


class DiscordConfigDict(TypedDict):
    account_token: str
    log_filename: str
    log_level: str


class ConfigDict(TypedDict):
    db: DBConfigDict
    discord: DiscordConfigDict


SQLLogicType = Union[BinaryExpression, BooleanClauseList, bool, BooleanColumnElement]
JoinOnType = Union[Type["BaseModel"], AliasedClass, RelationshipProperty]


@dataclass
class JoinStruct:
    join_model: JoinOnType
    join_on: Union[Optional[SQLLogicType], RelationshipProperty] = field(default=None)
    use_outer_join: bool = field(default=False)

    def get_join_data(self) -> Union[Tuple[JoinOnType], Tuple[JoinOnType, Union[SQLLogicType, RelationshipProperty]]]:
        if self.join_on is not None:
            return self.join_model, self.join_on
        return (self.join_model,)

    def get_join_func(self) -> Literal["outerjoin", "join"]:
        if self.use_outer_join:
            return "outerjoin"
        return "join"


JoinListType = Sequence[
    Union[
        FromClause,
        JoinStruct,
        Tuple[JoinOnType, Union[SQLLogicType, RelationshipProperty]],
        Tuple[CTE, SQLLogicType],
    ]
]

EntitiesType = Union[Column, Label, Type["BaseModel"], Function]
BaseModelType = TypeVar("BaseModelType", bound="BaseModel")  # pylint: disable=C0103

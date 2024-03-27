from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.sql.operators import and_
from toolz.curried import map, compose_left

from omniagent.db.database import DBSession
from omniagent.db.models import ChatHistory, ChatSession
from omniagent.dto.chat_history import ChatHistory as ChatHistoryDto
from omniagent.dto.chat_history import ChatMessage as ChatMessageDto
from omniagent.dto.chat_history import ChatSession as ChatSessionDto
from omniagent.dto.session import SessionTreeNodeDTOType, SessionTab


def get_sessions(user_id: str, offset: int, limit: int):
    with DBSession() as db_sess:
        all0 = (
            db_sess.query(ChatSession)
            .filter(
                and_(
                    and_(
                        ChatSession.user_id == user_id,
                        None == ChatSession.deleted_at,
                    ),
                    ChatSession.type == SessionTreeNodeDTOType.session,
                )
            )
            .order_by(desc("created_at"))
            .limit(limit)
            .offset(offset)
            .all()
        )
        return compose_left(map(ChatSessionDto.from_orm), list)(all0)


def get_recent_sessions(user_id: str, offset: int, limit: int):
    with DBSession() as db_sess:
        all0 = (
            db_sess.query(ChatSession)
            .filter(
                and_(
                    and_(
                        and_(
                            ChatSession.user_id == user_id,
                            None == ChatSession.deleted_at,
                        ),
                        ChatSession.tab == SessionTab.recent,
                    ),
                    ChatSession.type == SessionTreeNodeDTOType.session,
                )
            )
            .order_by(desc("created_at"))
            .limit(limit)
            .offset(offset)
            .all()
        )
        return compose_left(map(ChatSessionDto.from_orm), list)(all0)


def get_histories(
    user_id: str, session_id: str, offset: int, limit: int
) -> ChatHistoryDto:
    with DBSession() as db_sess:
        all0 = (
            db_sess.query(ChatHistory)
            .filter(
                and_(
                    ChatHistory.session_id == session_id, ChatHistory.user_id == user_id
                )
            )
            .order_by(desc("send_at"))
            .limit(limit)
            .offset(offset)
            .all()
        )

        msgs = ChatMessageDto.from_orm(all0)

        one = (
            db_sess.query(ChatSession)
            .filter(ChatSession.session_id == session_id)
            .one()
        )
        return ChatHistoryDto(
            title=one.title,
            messages=msgs,
        )


def delete_histories(user_id: str, session_id: str):
    with DBSession() as db_sess:
        db_sess.query(ChatSession).filter(
            and_(
                ChatSession.session_id == session_id,
                ChatSession.user_id == user_id,
            )
        ).update({"deleted_at": datetime.utcnow()})
        db_sess.commit()

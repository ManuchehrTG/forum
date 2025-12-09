from .base import MessageType, MessageBase, Message, MessageResponse
from .message_post import MessagePost, MessagePostCreateRequest, MessagePostResponse, MessageWithPost, MessageWithPostResponse
from .message_comment import MessageComment, MessageCommentCreateRequest, MessageCommentResponse, MessageWithComment, MessageWithCommentResponse
from .message_task import MessageTaskStatusType, MessageTask, MessageTaskCreateRequest, MessageTaskResponse, MessageWithTask, MessageWithTaskResponse
from .reactions import MessageReactionType, MessageReaction, MessageReactionUpdateRequest, MessageReactionResponse

MessageCreateRequest = MessagePostCreateRequest | MessageCommentCreateRequest | MessageTaskCreateRequest

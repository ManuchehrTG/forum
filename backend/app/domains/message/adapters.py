from app.domains.openai.schemas import OpenAIGenerateText, OpenAIGenerateTextResponse
from app.domains.media_file.schemas import MediaFile, MediaFileResponse
from .schemas import (
	Message, MessageResponse,
	MessagePost, MessagePostResponse, MessageWithPost, MessageWithPostResponse,
	MessageTask, MessageTaskResponse, MessageWithTask, MessageWithTaskResponse,
	MessageComment, MessageCommentResponse, MessageWithComment, MessageWithCommentResponse,
	MessageReaction, MessageReactionResponse
)

def openai_generate_text_to_response(openai_generate_text: OpenAIGenerateText) -> OpenAIGenerateTextResponse:
	return OpenAIGenerateTextResponse(**openai_generate_text.model_dump())

def message_to_response(message: Message) -> MessageResponse:
	return MessageResponse(**message.model_dump())

def message_post_to_response(message_post: MessagePost) -> MessagePostResponse:
	return MessagePostResponse(**message_post.model_dump())

def message_task_to_response(message_task: MessageTask) -> MessageTaskResponse:
	return MessageTaskResponse(**message_task.model_dump())

def message_comment_to_response(message_comment: MessageComment) -> MessageCommentResponse:
	return MessageCommentResponse(**message_comment.model_dump())

def message_with_post_to_response(message_with_post: MessageWithPost) -> MessageWithPostResponse:
	return MessageWithPostResponse(
		message=message_to_response(message=message_with_post.message),
		message_post=message_post_to_response(message_post=message_with_post.message_post)
	)

def message_with_task_to_response(message_with_task: MessageWithTask) -> MessageWithTaskResponse:
	return MessageWithTaskResponse(
		message=message_to_response(message=message_with_task.message),
		message_task=message_task_to_response(message_task=message_with_task.message_task)
	)

def message_with_comment_to_response(message_with_comment: MessageWithComment) -> MessageWithCommentResponse:
	return MessageWithCommentResponse(
		message=message_to_response(message=message_with_comment.message),
		message_comment=message_comment_to_response(message_comment=message_with_comment.message_comment)
	)

def media_file_to_response(media_file: MediaFile) -> MediaFileResponse:
	return MediaFileResponse(**media_file.model_dump())

def message_reaction_to_response(message_reaction: MessageReaction) -> MessageReactionResponse:
	return MessageReactionResponse(**message_reaction.model_dump())

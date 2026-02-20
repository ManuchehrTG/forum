# from uuid import UUID

# from src.application.decorators import handle_domain_errors

# from src.application.messages.commands import CreateMessageCommand
# from src.domain.messages.entities import Message
# from src.domain.messages.repository import MessageRepository

# class CreateMessage:
# 	def __init__(self, message_repo: MessageRepository):
# 		self.message_repo = message_repo

# 	@handle_domain_errors
# 	async def execute(self, command: CreateMessageCommand) -> UUID:
# 		message = Message.create(
# 			text=command.text,
# 			type=command.type,
# 			author_id=command.author_id,
# 			theme_id=command.theme_id,
# 			section_id=command.section_id
# 		)

# 		await self.message_repo.save(message)

# 		return message.id
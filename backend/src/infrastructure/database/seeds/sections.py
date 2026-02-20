from src.domain.messages.value_objects import MessageType
from src.domain.sections.entities import Section
from src.domain.sections.exceptions import SectionNotFoundError
from src.domain.sections.repository import SectionRepository
from src.domain.sections.value_objects import TechVersionType

SECTIONS = [
	{
		"code": "discussion",
		"allow_hide": True,
		"tech_version": TechVersionType.MINIMUM,
		"message_types": [
			{"message_type": MessageType.POST, "allow_comments": False}
		]
	},
	{
		"code": "experience_exchange",
		"allow_hide": True,
		"tech_version": TechVersionType.MINIMUM,
		"message_types": [
			{"message_type": MessageType.POST, "allow_comments": True}
		]
	},
	{
		"code": "description",
		"allow_hide": False,
		"tech_version": TechVersionType.MINIMUM,
		"message_types": [
			{"message_type": MessageType.POST, "allow_comments": True}
		]
	},
	{
		"code": "perfect_result",
		"allow_hide": True,
		"tech_version": TechVersionType.MINIMUM,
		"message_types": [
			{"message_type": MessageType.POST, "allow_comments": True}
		]
	},
	{
		"code": "project_modules",
		"allow_hide": True,
		"tech_version": TechVersionType.MINIMUM,
	},
	{
		"code": "chat_ideas",
		"allow_hide": True,
		"tech_version": TechVersionType.FULL,
		"openai_prompt": "Улучшите текст идеи, сделав его максимально лаконичным. Ответь только улучшенным текстом, без дополнительных комментариев.",
		"message_types": [
			{"message_type": MessageType.POST, "allow_comments": True}
		]
	},
	{
		"code": "chat_qa",
		"allow_hide": True,
		"tech_version": TechVersionType.FULL,
		"message_types": [
			{"message_type": MessageType.POST, "allow_comments": True}
		]
	},
	{
		"code": "chat_publications",
		"allow_hide": True,
		"tech_version": TechVersionType.FULL,
		"message_types": [
			{"message_type": MessageType.POST, "allow_comments": True}
		]
	},
	{
		"code": "chat_tasks",
		"allow_hide": True,
		"tech_version": TechVersionType.FULL,
		"message_types": [
			{"message_type": MessageType.TASK, "allow_comments": True},
			{"message_type": MessageType.TASK_ASSIGNMENT, "allow_comments": False}
		]
	},
	{
		"code": "chat_experiments",
		"allow_hide": True,
		"tech_version": TechVersionType.FULL,
		"message_types": [
			{"message_type": MessageType.TASK, "allow_comments": True},
			{"message_type": MessageType.TASK_ASSIGNMENT, "allow_comments": False}
		]
	},
]

async def seed_sections(section_repo: SectionRepository):
	for data in SECTIONS:
		try:
			section = await section_repo.get_by_code(data["code"])
		except SectionNotFoundError:
			section = Section(code=data["code"], allow_hide=data["allow_hide"], tech_version=data["tech_version"], openai_prompt=data.get("openai_prompt"))

		for mt in data.get("message_types", []):
			if not section.has_allowed_message_type(mt["message_type"]):
				section.add_allowed_message_type(message_type=mt["message_type"], allow_comments=mt["allow_comments"])

		await section_repo.save(section)

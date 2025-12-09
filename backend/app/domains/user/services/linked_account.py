from ..repositories import LinkedAccountRepository
from ..schemas import LinkedAccountCreateData

class LinkedAccountService:
	async def create_linked_account(self, linked_account_data: LinkedAccountCreateData):
		return await LinkedAccountRepository.create_linked_account(data=linked_account_data)

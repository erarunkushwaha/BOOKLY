from .model import User
from sqlalchemy.ext.asyncio import AsyncSession

# from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
import logging
from .schema import UserCreateModel
from .utils import generate_password_hash


# Configure logging
logger = logging.getLogger(__name__)


class UserService:

    @staticmethod
    async def get_user_by_email(email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.execute(statement)
        print("#####----::", result)

        user = result.first()
        print("user #####----::", user)

        logger.info(f"Retrieved  user from database")
        return user

    async def user_exist(self, email: str, session: AsyncSession):
        statement = await UserService.get_user_by_email(email, session)

        return True if statement is not None else False

    @staticmethod
    async def create_user(user_data: UserCreateModel, session: AsyncSession):
        # print("user data #####----::", user_data)

        user_data_dict = user_data.model_dump()
        # print("user_data_dict #####----::", user_data_dict)

        # Extract and remove the plain password
        plain_password = user_data_dict.pop("password")
        # Hash the password and add to dict
        # user_data_dict["password_hash"] = generate_password_hash(plain_password)
        user_data_dict["password_hash"] = plain_password
        
    
        # Now create the user with the correct fields
        new_user = User(**user_data_dict)
        # print("new_user #####----::", new_user)

        # print("password #####----::", new_user)

        session.add(new_user)
        print("**************. ONE **********")
        
        await session.flush()

        await session.refresh(new_user)
        print("**************. TWO **********")
        
        await session.commit()
        print("**************. THREE **********")
        
        
        logger.info(f"NEW USER CREATED ************************: {new_user.first_name} (uid: {new_user.last_name})")
        

        return new_user

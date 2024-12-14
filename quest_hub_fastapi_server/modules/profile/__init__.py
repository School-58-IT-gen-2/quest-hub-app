from fastapi import status
from typing import List, Optional
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from quest_hub_fastapi_server.adapters.db_source import DBSource
from quest_hub_fastapi_server.modules.profile.models import (
    RequestProfileModel,
    DatabaseProfileModel,
)


def get_profile():
    return Profile()


class Profile:
    def __init__(self):
        self.db_table_name = "profiles"
        self.db_source = DBSource()

    def __get_dict_by_tg_id(self, tg_id: int) -> dict:
        profile_dict_list = self.db_source.get_by_value(
            self.db_table_name, "tg_id", tg_id
        )
        if len(profile_dict_list) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Профиль не найден.",
            )
        if len(profile_dict_list) > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Найдено несколько профилей с таким tg_id.",
            )
        return profile_dict_list[0]

    def get_by_tg_id(self, tg_id: int) -> Optional[DatabaseProfileModel]:
        """Получение профиля по идентификатору Telegram."""
        profile_dict_list = self.__get_dict_by_tg_id(tg_id)
        return DatabaseProfileModel(**profile_dict_list)

    def delete(self, tg_id: int) -> List[dict]:
        profile_model = self.get_by_tg_id(tg_id)
        self.db_source.delete(self.db_table_name, profile_model.id)
        profile_dict_list = self.db_source.get_by_value(
            self.db_table_name, "tg_id", profile_model.id
        )
        if len(profile_dict_list) == 0:
            return JSONResponse(status_code=204, content={})
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Возникла ошибка при удалении",
            )

    def create_or_update(
        self,
        rq_profile_model: RequestProfileModel,
    ) -> DatabaseProfileModel:
        """Создание нового профиля, если он не существует."""
        profile_dict_list = self.db_source.get_by_value(
            self.db_table_name, "tg_id", rq_profile_model.tg_id
        )
        if len(profile_dict_list) == 0:
            created_profile_dict = self.db_source.insert(
                self.db_table_name,
                rq_profile_model.model_dump(),
            )
            return DatabaseProfileModel(**created_profile_dict[0])
        if len(profile_dict_list) == 1:
            tg_id = profile_dict_list[0].get("id")
            updated_profile_dict_list = self.db_source.update(
                self.db_table_name, rq_profile_model.model_dump(), tg_id
            )
            return DatabaseProfileModel(**updated_profile_dict_list[0])
        if len(profile_dict_list) > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Найдено несколько профилей с таким tg_id.",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Низвестная ошибка при создании пользователя",
            )

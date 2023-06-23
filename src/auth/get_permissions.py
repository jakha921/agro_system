from fastapi import HTTPException
from functools import wraps
from fastapi import Request


def has_permission(permission_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = next(arg for arg in args if isinstance(arg, Request))
            # Проверка разрешения пользователя
            # Получение пользователя из сессии или токена аутентификации
            # Проверка наличия разрешения у пользователя
            # В случае отсутствия разрешения выбросить исключение HTTPException
            if not has_permission:
                raise HTTPException(status_code=403, detail="Нет доступа")
            return await func(*args, **kwargs)

        return wrapper

    return decorator

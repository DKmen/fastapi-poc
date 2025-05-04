from sqlmodel import Session, text

from app.db import engine
from app.helper import logger, encrypt_string
from app.models import PermissionType, User, Permission, Role, RolePermission, UserRole

content = {
    "users": [
        {
            "name": "John Doe",
            "email": "john.doe@gmail.com",
            "password": "john.doe@123",
            "role": "Admin"
        }
    ],
    "permissions": [
        {
            "name": "Admin Permission",
            "permission_routes": ".*",
            "permission_type": PermissionType.ADMIN,
        },
        {
            "name": "Project Create Permission",
            "permission_routes": ".*project.*",
            "permission_type": PermissionType.POST,
        },
        {
            "name": "Project Delete Permission",
            "permission_routes": ".*project.*",
            "permission_type": PermissionType.DELETE,
        },
        {
            "name": "Project Update Permission",
            "permission_routes": ".*project.*",
            "permission_type": PermissionType.PATCH,
        },
        {
            "name": "Project Get Permission",
            "permission_routes": ".*project.*",
            "permission_type": PermissionType.GET,
        },
        {
            "name": "User Create Permission",
            "permission_routes": ".*user.*",
            "permission_type": PermissionType.POST,
        },
        {
            "name": "User Delete Permission",
            "permission_routes": ".*user.*",
            "permission_type": PermissionType.DELETE,
        },
        {
            "name": "User Update Permission",
            "permission_routes": ".*user.*",
            "permission_type": PermissionType.PATCH,
        },
        {
            "name": "User Get Permission",
            "permission_routes": ".*user.*",
            "permission_type": PermissionType.GET,
        },
    ],
    "roles": [
        {
            "name": "Admin",
            "permissions": [
                "Admin Permission",
            ],
        },
        {
            "name": "User",
            "permissions": [
                "Project Get Permission",
            ],
        },
    ],
}

def seed():
    logger.info({"message": "(seed) seeder is running"})

    # delete all data
    with Session(engine) as session:
        # delete all data
        session.exec(text('DELETE FROM "user_role"'))
        session.exec(text('DELETE FROM "role_permission"'))
        session.exec(text('DELETE FROM "permission"'))
        session.exec(text('DELETE FROM "role"'))
        session.exec(text('DELETE FROM "user"'))

        session.commit()

    users = []
    # create users
    with Session(engine) as session:
        for user in content["users"]:
            users.append(
                User(
                    name=user["name"],
                    email=user["email"],
                    password=encrypt_string(user["password"]),
                )
            )
        
        # create users
        session.add_all(users)
        session.commit()
        
        for index, user in enumerate(users):
            session.refresh(user)
            content["users"][index]["id"] = user.id
    
    logger.debug({
        "message": "(seed) users created",
        "users": users,
        "content": content,
    })

    permissions = []
    # create permissions
    with Session(engine) as session:
        for permission in content["permissions"]:
            permissions.append(
                Permission(
                    name=permission["name"],
                    permission_routes=permission["permission_routes"],
                    permission_type=permission["permission_type"],
                )
            )
        
        # create permissions
        session.add_all(permissions)
        session.commit()

        for index, permission in enumerate(permissions):
            session.refresh(permission)
            content["permissions"][index]["id"] = permission.id

    logger.debug({
        "message": "(seed) permissions created",
        "permissions": permissions,
        "content": content,
    })

    roles = []
    # create roles
    with Session(engine) as session:
        for role in content["roles"]:
            roles.append(
                Role(
                    name=role["name"],
                )
            )

        # create roles
        session.add_all(roles)
        session.commit()

        for index, role in enumerate(roles):
            session.refresh(role)
            content["roles"][index]["id"] = role.id
    
    logger.debug({
        "message": "(seed) roles created",
        "roles": roles,
        "content": content,
    })

    role_permissions = []
    # attech role permissions
    with Session(engine) as session:
        for role in content["roles"]:
            for permission in role["permissions"]:
                created_permission = [ per["id"] for per in content["permissions"] if per["name"] == permission ][0]
                role_permissions.append(
                    RolePermission(
                        permission_id=created_permission,
                        role_id=role["id"],
                    )
                )
        
        # create role permissions
        session.add_all(role_permissions)
        session.commit()

        for index, role_permission in enumerate(role_permissions):
            session.refresh(role_permission)
        
    user_role = []
    # attech role with user
    with Session(engine) as session:
        for user in content["users"]:
            current_role = [ role["id"] for role in content["roles"] if role["name"] == user["role"] ][0]
            user_role.append(
                UserRole(
                    user_id=user["id"],
                    role_id=current_role,
                )
            )
        
        # create user roles
        session.add_all(user_role)
        session.commit()

        for index, user_role in enumerate(user_role):
            session.refresh(user_role)

if __name__ == "__main__":
    seed()

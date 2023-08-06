# encoding: utf-8
"""
@project: djangoModel->role_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 角色服务
@created_time: 2022/9/2 15:37
"""
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F

from xj_user.services.user_service import UserService
from ..models import Role, UserToRole
from ..utils.custom_tool import format_list_handle
from ..utils.j_recur import JRecur
from ..utils.model_handle import format_params_handle


# 用户组 树状数据返回
class RoleTreeService(object):
    @staticmethod
    def get_tree(data_list, parent_group):
        tree = []
        for item in data_list:
            if str(item['parent_role_id']) == str(parent_group):
                item['name'] = item['role_name']
                item['children'] = RoleTreeService.get_tree(data_list, item['id'])
                tree.append(item)
        return tree

    @staticmethod
    def get_trees(data_list, parent_group):
        # 适配模式进行 搜索
        tree = []
        if parent_group != 0:  # 不从根节点搜索，自定义搜索
            base_node = Role.objects.filter(id=parent_group).to_json()  # 如果是搜索，则获取该节点角色信息
            for item in data_list:
                if str(item['parent_role_id']) == str(parent_group):
                    item['name'] = item['role_name']
                    item['children'] = RoleTreeService.get_tree(data_list, item['id'])
                    tree.append(item)
            base_node[0]['children'] = tree
            return base_node[0]
        else:  # 进行根节点搜索
            for item in data_list:
                if not str(item['parent_role_id']) == str(parent_group):
                    continue
                child = RoleTreeService.get_tree(data_list, item['id'])
                item['name'] = item['role_name']
                item['children'] = child
                tree.append(item)
        return tree

    @staticmethod
    def role_tree(role_id=0):
        data_list = list(Role.objects.all().values())
        group_tree = RoleTreeService.get_trees(data_list, role_id)
        return group_tree, None


class RoleService:
    @staticmethod
    def add_role(params):
        params = format_params_handle(param_dict=params,
                                      filter_filed_list=["role", "role_name", "parent_role_id", "permission_id",
                                                         "user_group_id", "description"])
        if not params:
            return None, "参数不能为空"
        instance = Role.objects.create(**params)
        return {"id": instance.id}, None

    @staticmethod
    def edit_role(params):
        params = format_params_handle(param_dict=params,
                                      filter_filed_list=["role_id", "role", "role_name", "parent_role_id",
                                                         "permission_id",
                                                         "user_group_id", "description"])
        id = params.pop("role_id", None)
        if not id:
            return None, "ID 不可以为空"
        if not params:
            return None, "没有可以修改的字段"
        instance = Role.objects.filter(id=id)
        if params:
            instance.update(**params)
        return None, None

    @staticmethod
    def del_role(id):
        if not id:
            return None, "ID 不可以为空"

        user_role_set = UserToRole.objects.filter(role_id=id).exists()
        if user_role_set:
            return None, "该角色有绑定关系,无法删除"
        instance = Role.objects.filter(id=id)
        if instance:
            instance.delete()
        return None, None

    @staticmethod
    def get_role_list(params, need_pagination=True):
        # 不分页查询
        if not need_pagination:
            params = format_params_handle(
                param_dict=params,
                filter_filed_list=["id", "id_list", "permission_id", "user_group_id", "user_group_id_list"],
                alias_dict={"id_list": "id__in", "user_group_id_list": "user_group_id__in"}
            )
            # print("params:", params)
            query_set = Role.objects.filter(**params)
            if not query_set:
                return [], None
            user_list = list(query_set.values())
            for i in user_list:
                id(i)
                i["is_role"] = True
                i["name"] = i["role_name"]
            return user_list, None
        # 分页查询
        page = params.pop("page", 1)
        size = params.pop("size", 20)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "permission_id", "role", "user_group_id", "page", "size"]
        )
        query_set = Role.objects.filter(**params).values()
        count = query_set.count()
        finish_set = list(Paginator(query_set, size).page(page).object_list)
        return {'size': int(size), 'page': int(page), 'count': count, 'list': finish_set}, None
        # return finish_set, None

    @staticmethod
    def user_role_list(user_id):
        """获取当前用户的所有角色"""
        return list(UserToRole.objects.filter(user_id=user_id).annotate(
            role_value=F('role_id__role'),
            role_name=F('role_id__role_name'),
            permission_id=F('role_id__permission'),
            permission_name=F('role_id__permission__permission_name'),
            user_group_value=F('role_id__user_group__group'),
            user_group_name=F('role_id__user_group__group_name'),
        ).values('id', 'role_id', 'user_id', 'role_value', 'role_name', 'permission_id', 'permission_name',
                 'user_group_value', 'user_group_name'))

    @staticmethod
    def is_this_role(user_id=None, role_id=None, role_key=None):
        """
        判断该用户是否属于该角色
        :return: res, err
        """
        if not user_id or (not role_id and not role_key):
            return False, None
        role_obj = UserToRole.objects.annotate(role_key=F("role__role")).filter(user_id=user_id)
        if role_id:
            res = role_obj.filter(role_id=role_id).first()
        else:
            res = role_obj.filter(role_key=role_key).first()
        return True if res else False, None

    @staticmethod
    def user_role_users(role_id, page, size, is_subtree=False):
        """
        查询该角色下面所有用户的用户进出信息信息
        :param group_id: 分组id
        :param page: 页数
        :param size: 条数
        :return:
        """
        if is_subtree:
            role_id_tree, err = RoleService.get_user_role_tree(role_id)
            if err:
                return None, err
            role_id_list = JRecur.get_value_in_forest(role_id_tree)

            user_set = UserToRole.objects.filter(role__in=role_id_list)
        else:
            user_set = UserToRole.objects.filter(role=role_id)

        user_set = user_set.annotate(user_role_value=F("role__role_name"))
        user_set = user_set.values(
            "user_id",
            "role",
        )
        params = {
            "page": page,
            "size": size
        }
        # TODO 这样的逻辑 返回的用户组列表 无法显示全部 。解决方案一：在详情的时候处理用户所在的组 方案二：通过聚合表 拿到用户的组
        user_id_list = [it['user_id'] for it in user_set]
        if not user_id_list:
            return {"count": 0, "list": []}, None

        user_serv, err = UserService.user_list(params, allow_user_list=user_id_list)
        if err:
            return None, err
        return user_serv, None

    @staticmethod
    def get_user_role_tree(role_id=None, is_family_tree=False):
        """
        获取用户所在角色树
        @param group_id 用户组ID，如果有则过滤用户组，没有会返回全部分组，请慎用。
        @param is_family_tree 是否返回整个家族数。
        """
        data_list = list(Role.objects.filter().annotate(name=F('role_name')).values(
            "id",
            "role",
            "role_name",
            "parent_role_id",
            "permission_id",
            "user_group_id",
            "description",
        ))
        role_tree = JRecur.create_forest(data_list, parent_key='parent_role_id')
        if role_id:
            role_tree = JRecur.filter_forest(source_forest=role_tree, find_key='id', find_value=role_id,
                                             is_family_tree=is_family_tree)
        return role_tree, None

    @staticmethod
    def user_list_by_roles(role_list):
        """按角色ID获取相关用户列表"""
        return list(UserToRole.objects.filter(role_id__in=role_list).values() or [])

    @staticmethod
    def user_bind_role(user_id, role_id):
        # 用户绑定角色
        if not user_id or not role_id:
            return None, "参数错误，user_id, role_id 必传"
        try:
            UserToRole.objects.get_or_create(
                {"user_id": user_id, "role_id": role_id},
                user_id=user_id,
                role_id=role_id,
            )
            return None, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def bind_user_role(user_id: int, role_list):
        """
        批量绑定用户角色信息
        :param user_id:
        :param role_list:
        :return:
        """
        if not role_list:
            UserToRole.objects.filter(user_id=user_id).delete()
            # 没有传值则
            return None, None

        role_list = role_list.split(',') if isinstance(role_list, str) else role_list
        if not role_list:
            return None, "至少选择一个角色"

        sid = transaction.savepoint()
        try:
            UserToRole.objects.filter(user_id=user_id).delete()
            for i in role_list:
                data = {
                    "user_id": user_id,
                    "role_id": i
                }
                UserToRole.objects.create(**data)
            transaction.clean_savepoints()
            return None, None
        except Exception as e:
            transaction.savepoint_rollback(sid)
            return None, str(e)

    @staticmethod
    def get_user_role_info(user_id: int = None, user_id_list: list = None, field_list=None, **kwargs):
        """
        获取用户的角色信息
        :param user_id: 用户id
        :param user_id_list: 用户的ID列表
        :param field_list: 字段过滤列表
        :return: 用户的角色列表，err
        """
        # 找不到可检索的用户，则直接返回，可以使用单个ID检索也可以使用ID列表检索。
        if not user_id and not user_id_list:
            return [], None

        # 过滤字段合法性验证
        allow_field_list = ["user_id", 'role_id', 'role_name', 'role_value', 'description']
        field_list = format_list_handle(
            param_list=field_list or [],
            filter_filed_list=allow_field_list
        )
        field_list = allow_field_list if not field_list else field_list
        # query 对象
        user_role_obj = UserToRole.objects.annotate(
            role_name=F("role__role_name"),
            role_value=F("role__role"),
            description=F("role__description"),
        ).values(*field_list)
        # 分情况检索数据
        if user_id:
            user_role_list = user_role_obj.filter(user_id=user_id)
            return list(user_role_list), None  # 返回用户的部门（分组）列表
        else:
            user_role_list = UserToRole.objects.filter(user_id__in=user_id_list)
            user_role_map = {}  # 按照用户进行映射
            for item in list(user_role_list):
                if user_role_map.get(item['user_id']):
                    user_role_map[item['user_id']].append(item)
                else:
                    user_role_map[item['user_id']] = [item]
            return user_role_map, None  # 返回映射字典

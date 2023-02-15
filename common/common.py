"""
Created by Joseph Edradan
Github: https://github.com/josephedradan

Date created: 2/11/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Reference:

"""
from typing import List
from typing import TYPE_CHECKING

from pacman.agent import Agent
from pacman.agent import get_subclass_agent
from pacman.parser import ContainerObjectConstruct

if TYPE_CHECKING:
    pass


def get_list_agent_from_list_container_object_construct(
        list_container_object_construct: List[ContainerObjectConstruct]) -> List[Agent]:
    list_agent: List[Agent] = []

    for container_object_construct in list_container_object_construct:
        str_agent = container_object_construct.name_class
        args = container_object_construct.arguments
        kwargs = container_object_construct.keyword_arguments

        subclass_agent = get_subclass_agent(str_agent)

        agent = subclass_agent(*args, **kwargs)

        list_agent.append(agent)

    return list_agent

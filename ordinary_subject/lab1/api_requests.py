from ordinary_subject.config import VK_CONFIG as cfg
import requests


# import time


# "universe_of_f1", "f1_fun_club"

def get_group_members_count(community_id):
    query = f"{cfg['vk_api_domain']}/groups.getMembers?" \
            f"group_id={community_id}&" \
            f"access_token={cfg['access_token']}&v={cfg['api_version']}"

    response = requests.get(url=query).json()
    return response['response']


def get_user_ids_of_communities(community_id):
    members_count = get_group_members_count(community_id)
    all_users_ids = []

    # for n_iter in range(members_count // 1000 + 1):
    for n_iter in range(1):
        offset = n_iter * 1000

        query = f"{cfg['vk_api_domain']}/execute?" \
                f"access_token={cfg['access_token']}&" \
                f"v={cfg['api_version']}&code="

        code = f"return API.groups.getMembers({{'group_id': {community_id}, 'offset': {offset}}});"
        query += code

    response = requests.get(url=query).json()
    return response


if __name__ == "__main__":
    print(get_user_ids_of_communities("36759319"))

from ordinary_subject.config import VK_CONFIG as vk_cfg
import pickle
import requests
import time


def get_id_from_nickname(nickname="alexanderlakiza"):
    query = f"{vk_cfg['vk_api_domain']}/utils.resolveScreenName?screen_name={nickname}&" \
            f"access_token={vk_cfg['access_token']}&v={vk_cfg['api_version']}"

    response = requests.get(url=query).json()
    return response['response']['object_id']


def get_group_members_count(community_id):
    query = f"{vk_cfg['vk_api_domain']}/groups.getMembers?" \
            f"group_id={community_id}&" \
            f"access_token={vk_cfg['access_token']}&v={vk_cfg['api_version']}"

    response = requests.get(url=query).json()
    return response['response']['count']


def get_user_ids_of_communities(group_id):
    members_count = get_group_members_count(group_id)
    all_users_ids = []

    query_start = f"{vk_cfg['vk_api_domain']}/execute?" \
                  f"access_token={vk_cfg['access_token']}&" \
                  f"v={vk_cfg['api_version']}&code="

    for n_iter in range(members_count // 1000 + 1):
        # for n_iter in range(1):
        offset = n_iter * 1000

        code = f"return API.groups.getMembers({{'group_id': {group_id}, 'offset': {offset}}});"
        query = query_start + code

        response = requests.get(url=query).json()['response']['items']
        all_users_ids.extend(response)
        time.sleep(0.35)

    return all_users_ids


def get_posts_of_group(group_id):
    posts_infos = []

    for i in range(20):
        query = f"{vk_cfg['vk_api_domain']}/wall.get?" \
                f"owner_id=-{group_id}&offset={i * 100}&count=100&" \
                f"access_token={vk_cfg['access_token']}&v={vk_cfg['api_version']}"

        response = requests.get(url=query).json()['response']['items']
        posts_infos.extend(response)
        time.sleep(0.35)

    return posts_infos


def get_friends_of_members(list_of_members):
    result = {}
    for i in list_of_members:
        result[i] = []

        query = f"{vk_cfg['vk_api_domain']}/friends.get?" \
                f"user_id={i}&" \
                f"access_token={vk_cfg['access_token']}&v={vk_cfg['api_version']}"

        try:
            friends_list = requests.get(url=query).json()['response']['items']
            result[i].extend(friends_list)
        except KeyError:
            pass

        time.sleep(0.35)

    return result


if __name__ == "__main__":
    ids_of_groups = {"formula1.championat": get_id_from_nickname("formula1.championat"),
                     "grand_prixf1_ru": get_id_from_nickname("grand_prixf1_ru")}

    members_dict = {"formula1.championat": get_user_ids_of_communities(ids_of_groups["formula1.championat"]),
                    "grand_prixf1_ru": get_user_ids_of_communities(ids_of_groups["grand_prixf1_ru"])}

    print('Members are collected!')

    posts_dict = {"formula1.championat": get_posts_of_group(ids_of_groups["formula1.championat"]),
                  "grand_prixf1_ru": get_posts_of_group(ids_of_groups["grand_prixf1_ru"])}

    print('Posts are collected!')

    friends_dict = {"formula1.championat": get_friends_of_members(members_dict["formula1.championat"]),
                    "grand_prixf1_ru": get_friends_of_members(members_dict["grand_prixf1_ru"])}

    print('Friends of members are collected')

    with open('members_of_groups.pickle', 'wb') as handle:
        pickle.dump(members_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('posts_of_groups.pickle', 'wb') as handle:
        pickle.dump(posts_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('friends_of_members.pickle', 'wb') as handle:
        pickle.dump(friends_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print('All data is collected and saved!')

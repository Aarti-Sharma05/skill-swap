from .selectors import user_data

def calculate_match_score(user,teaching_match_count,learning_matching_count,interest_match):
    score = 0
    if teaching_match_count:
        score = score + teaching_match_count*1.0
    if learning_matching_count:
        score = score + learning_matching_count*0.5
    if interest_match:
        score = score + interest_match

    return score

def get_ranked_users(users):
    ranked = []
    queryset = user_data(users)
    users_learning_skills = list(users.learning_skill.values_list("skills__id", flat=True))
    users_teaching_skills = list(users.teaching_skill.values_list("skill__id", flat=True))
    users_area_of_interest = users.profile.interest
    for user in queryset:
        learning_skills = list(user.learning_skill.values_list("skills__id", flat=True))
        teaching_skills = list(user.teaching_skill.values_list("skill__id", flat=True))
        area_of_interest = user.profile.interest
        teaching_match_count = len(set(users_learning_skills)&set(teaching_skills))
        learning_match_count = len(set(users_teaching_skills)&set(learning_skills))
        interest_match = 1 if users_area_of_interest==area_of_interest else 0
        score = calculate_match_score(user,teaching_match_count,learning_match_count,interest_match)
        ranked.append({"user" : user,"score" : score})
    print(ranked)
    return sorted(ranked, key=lambda x: x["score"], reverse=True)



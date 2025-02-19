from match_app.models import Match, MatchParticipant


def insert_quick_play_record(winner_user_id):
    finish_date = None if winner_user_id is None else "2024-01-02"

    return Match.objects.create(
        winner_user_id=winner_user_id,
        mode="QuickPlay",
        start_date="2024-01-01",
        finish_date=finish_date,
    )


def insert_tournament_record(winner_user_id, tournament_id, parent_match_id, round):
    finish_date = None if winner_user_id is None else "2024-01-02"
    return Match.objects.create(
        winner_user_id=winner_user_id,
        mode="Tournament",
        start_date="2024-01-01",
        finish_date=finish_date,
        tournament_id=tournament_id,
        parent_match_id=parent_match_id,
        round=round,
    )


def insert_match_participants_record(match_id, user_id, score=None):
    MatchParticipant.objects.create(match_id=match_id, user_id=user_id, score=score)


def create_query_string(**params):
    """paramsに指定した変数がNone出ない場合、QueryStringに追加する"""
    query_params = [
        f"{key}={value}" for key, value in params.items() if value is not None
    ]
    if query_params == []:
        return ""
    return "?" + "&".join(query_params)

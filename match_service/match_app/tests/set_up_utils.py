import pytest

from match_app.models import Matches, MatchParticipants


@pytest.fixture
def set_up_records() -> int:
    # 試合が終了していないQuickPlay
    match1 = insert_quick_play_record(None)
    insert_match_participants_record(match1, 1)
    insert_match_participants_record(match1, 2)

    # 試合終了済みのQuickPlay
    match2 = insert_quick_play_record(3)
    insert_match_participants_record(match2, 3, 11)
    insert_match_participants_record(match2, 4, 5)

    # 終了していない４人の参加者がいるトーナメント
    tournament_id = 1
    match3 = insert_tournament_record(None, tournament_id, None, 3)

    match4 = insert_tournament_record(None, tournament_id, match3, 2)
    insert_match_participants_record(match4, 3)
    insert_match_participants_record(match4, 4)

    match5 = insert_tournament_record(None, tournament_id, match3, 1)
    insert_match_participants_record(match5, 1)
    insert_match_participants_record(match5, 2)

    # 終了済みの2人の参加者がいるトーナメント
    tournament_id = 2
    match6 = insert_tournament_record(1, tournament_id, None, 1)
    insert_match_participants_record(match6, 1, 11)
    insert_match_participants_record(match6, 2, 0)

    # 1ラウンドだけ終了済みの３人の参加者がいるトーナメント
    tournament_id = 3
    match7 = insert_tournament_record(None, tournament_id, None, 2)
    insert_match_participants_record(match7, 1)
    insert_match_participants_record(match7, 3)

    match8 = insert_tournament_record(1, tournament_id, match7, 1)
    insert_match_participants_record(match8, 1, 11)
    insert_match_participants_record(match8, 2, 0)

    return match8.match_id


def insert_quick_play_record(winner_user_id):
    finish_date = None if winner_user_id is None else "2024-01-02"

    return Matches.objects.create(
        winner_user_id=winner_user_id,
        mode="QuickPlay",
        start_date="2024-01-01",
        finish_date=finish_date,
    )


def insert_tournament_record(winner_user_id, tournament_id, parent_match_id, round):
    finish_date = None if winner_user_id is None else "2024-01-02"
    return Matches.objects.create(
        winner_user_id=winner_user_id,
        mode="Tournament",
        start_date="2024-01-01",
        finish_date=finish_date,
        tournament_id=tournament_id,
        parent_match_id=parent_match_id,
        round=round,
    )


def insert_match_participants_record(match_id, user_id, score=None):
    MatchParticipants.objects.create(match_id=match_id, user_id=user_id, score=score)

import pytest

from match_app.models import Matches

from .set_up_utils import (
    insert_match_participants_record,
    insert_quick_play_record,
    insert_tournament_record,
)


@pytest.fixture
def set_up_records() -> dict[str, int]:
    """
    WARN SetUp時により多くのレコードをinsertしてテストしたい場合、
         別のSetUp関数を作成してください
         このSetUp関数の変更は多数のテストに影響する可能性があります
    """
    match_id_dict = (
        __insert_finished_quick_play()
        | __insert_not_finished_quick_play()
        | __insert_not_finished_tournament()
        | __insert_finished_tournament()
        | __insert_only_one_round_finished_tournament()
    )

    return match_id_dict


def __insert_finished_quick_play() -> dict[str, int]:
    # 試合が終了しているQuickPlay
    match1 = insert_quick_play_record(3)
    insert_match_participants_record(match1, 3, 11)
    insert_match_participants_record(match1, 4, 5)
    return {"match1_id": match1.match_id}


def __insert_not_finished_quick_play() -> dict[str, int]:
    # 試合が終了していないQuickPlay
    match2 = insert_quick_play_record(None)
    insert_match_participants_record(match2, 1)
    insert_match_participants_record(match2, 2)
    return {"match2_id": match2.match_id}


def __insert_not_finished_tournament() -> dict[str, int]:
    # 終了していない４人の参加者がいるトーナメント
    tournament_id = 1
    match3 = insert_tournament_record(None, tournament_id, None, 3)

    match4 = insert_tournament_record(None, tournament_id, match3, 2)
    insert_match_participants_record(match4, 3)
    insert_match_participants_record(match4, 4)

    match5 = insert_tournament_record(None, tournament_id, match3, 1)
    insert_match_participants_record(match5, 1)
    insert_match_participants_record(match5, 2)
    return {
        "match3_id": match3.match_id,
        "match4_id": match4.match_id,
        "match5_id": match5.match_id,
    }


def __insert_finished_tournament() -> dict[str, int]:
    # 終了済みの2人の参加者がいるトーナメント
    tournament_id = 2
    match6 = insert_tournament_record(1, tournament_id, None, 1)
    insert_match_participants_record(match6, 1, 11)
    insert_match_participants_record(match6, 2, 0)
    return {"match6_id": match6.match_id}


def __insert_only_one_round_finished_tournament() -> dict[str, int]:
    # 1ラウンドだけ終了済みの３人の参加者がいるトーナメント
    tournament_id = 3
    match7 = insert_tournament_record(None, tournament_id, None, 2)
    insert_match_participants_record(match7, 1)
    insert_match_participants_record(match7, 3)

    match8 = insert_tournament_record(1, tournament_id, match7, 1)
    insert_match_participants_record(match8, 1, 11)
    insert_match_participants_record(match8, 2, 0)
    return {"match7_id": match7.match_id, "match8_id": match8.match_id}

import pytest

from tournament_app.utils.tournament_tree import TournamentTree


class TestTournamentTree:
    @pytest.mark.parametrize(
        "expect_return, lst, group_size",
        [
            (1, [1, 2], 2),
            (2, [1, 2, 3], 2),
            (2, [1, 2, 3, 4], 2),
            (4, [1, 2, 3, 4, 5], 2),
            (4, [1, 2, 3, 4, 5, 6, 7, 8], 2),
            (8, [1, 2, 3, 4, 5, 6, 7, 8, 9], 2),
            (1, [1, 2], 3),
            (1, [1, 2, 3], 3),
            (3, [1, 2, 3, 4], 3),
            (3, [1, 2, 3, 4, 5, 6, 7, 8, 9], 3),
            (9, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3),
            (-1, [1], 2),  # lstのサイズが1以下はエラー
            (-1, [1, 2], 0),  # group_sizeが1以下はエラー
        ],
    )
    @pytest.mark.django_db
    def test_calc_node_list_size(self, expect_return, lst, group_size):
        assert TournamentTree.calc_node_list_size(lst, group_size) == expect_return

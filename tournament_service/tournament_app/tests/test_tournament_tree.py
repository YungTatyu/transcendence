import pytest

from tournament_app.utils.tournament_tree import TournamentTree


class TestTournamentTree:
    @pytest.mark.parametrize(
        "lst, group_size, expect_dict_list",
        [
            (
                [1, 2],
                2,
                [{"value_list": [1, 2], "round": 1}],
            ),
            (
                [1, 2, 3],
                2,
                [{"value_list": [2], "round": 2}, {"value_list": [1, 3], "round": 1}],
            ),
            (
                [1, 2, 3, 4],
                2,
                [
                    {"value_list": [], "round": 3},
                    {"value_list": [1, 3], "round": 1},
                    {"value_list": [2, 4], "round": 2},
                ],
            ),
            (
                [1, 2, 3, 4, 5],
                2,
                [
                    {"value_list": [], "round": 4},
                    {"value_list": [2], "round": 2},
                    {"value_list": [3, 4], "round": 3},
                    {"value_list": [1, 5], "round": 1},
                ],
            ),
            (
                [1, 2, 3, 4],
                3,
                [
                    {"value_list": [2, 3], "round": 2},
                    {"value_list": [1, 4], "round": 1},
                ],
            ),
            (
                [1, 2, 3, 4, 5, 6, 7, 8, 9],
                3,
                [
                    {"value_list": [], "round": 4},
                    {"value_list": [1, 4, 7], "round": 1},
                    {"value_list": [2, 5, 8], "round": 2},
                    {"value_list": [3, 6, 9], "round": 3},
                ],
            ),
            (
                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                3,
                [
                    {"value_list": [], "round": 5},
                    {"value_list": [2, 3], "round": 2},
                    {"value_list": [4, 5, 6], "round": 3},
                    {"value_list": [7, 8, 9], "round": 4},
                    {"value_list": [1, 10], "round": 1},
                ],
            ),
        ],
    )
    def test_tournament_tree(self, lst, group_size, expect_dict_list):
        tree = TournamentTree(lst, group_size)
        root = tree.root

        for expect_dict, node in zip(expect_dict_list, tree.bfs_iterator(root)):
            assert expect_dict["value_list"] == node.value_list
            assert expect_dict["round"] == node.round

    @pytest.mark.parametrize(
        "lst, group_size",
        [
            ([0], 2),  # len(lst) == 0 なのでエラー
            ([1], 2),  # len(lst) == 1 なのでエラー
            ([1, 2], 1),  # group_size == 1 なのでエラー
            ([1, 2], -1),  # group_size == -1 なのでエラー
        ],
    )
    def test_tournament_tree_raise_value_error(self, lst, group_size):
        """ValueErrorが発生するかをテスト"""
        with pytest.raises(ValueError):
            TournamentTree(lst, group_size)

    @pytest.mark.parametrize(
        "lst, group_size, expect_id_list",
        [
            ([1, 2, 3], 2, [None, 1]),
            ([1, 2, 3, 4], 2, [None, 1, 1]),
            ([1, 2, 3, 4, 5], 2, [None, 1, 1, 2]),
            ([1, 2, 3, 4, 5, 6, 7, 8], 2, [None, 1, 1, 2, 2, 3, 3]),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9], 3, [None, 1, 1, 1]),
            ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3, [None, 1, 1, 1, 2]),
        ],
    )
    def test_get_parent_match_id(self, lst, group_size, expect_id_list):
        tree = TournamentTree(lst, group_size)

        for i, node in enumerate(tree.bfs_iterator(tree.root)):
            #  仮のmatch_idとして 1,2,3...を付与する
            node.match_id = i + 1

        for expect_id, node in zip(expect_id_list, tree.bfs_iterator(tree.root)):
            parent_node = node.parent_node
            parent_match_id = None if parent_node is None else parent_node.match_id
            assert expect_id == parent_match_id

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

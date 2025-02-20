from collections import deque
from typing import Any, Optional


class TournamentTree:
    class Node:
        def __init__(self, value_list, children):
            self.__value_list: list[Any] = value_list
            self.__children: list[TournamentTree.Node] = children
            self.__round: Optional[int] = None
            self.__parent_node: Optional[TournamentTree.Node] = None
            self.__match_id: Optional[int] = None

        @property
        def value_list(self):
            return self.__value_list

        @property
        def children(self):
            return self.__children

        @property
        def round(self):
            return self.__round

        @property
        def parent_node(self):
            return self.__parent_node

        @property
        def match_id(self):
            return self.__match_id

        @round.setter
        def round(self, value):
            self.__round = value

        @parent_node.setter
        def parent_node(self, value):
            self.__parent_node = value

        @match_id.setter
        def match_id(self, value):
            self.__match_id = value

        @property
        def is_leaf(self):
            return len(self.__children) == 0

        @property
        def has_single_value(self):
            return len(self.__value_list) == 1

        def __str__(self):
            value_list = f"value_list: {self.__value_list}"
            round = f"round: {self.__round}"
            parent = f"parent: {self.__parent_node}"
            match_id = f"match_id: {self.__match_id}"
            return f"({value_list}, {round}, {parent}, {match_id})"

    def __init__(self, lst: list, group_size: int = 2):
        """
        :param lst: TournamentTreeを作成するためのデータのリスト(要素数2以上)
        :param group_size: 1試合の最大人数(2以上)
        """
        if len(lst) < 2 or group_size < 2:
            raise ValueError(
                "Invalid parameters: list size must be at least 2, group_size must be 2 or greater."
            )
        self.__group_size = group_size
        node_list = self.__create_node_list(lst, group_size)
        self.__root = self.__create_tree(node_list, 1)

    @property
    def group_size(self):
        return self.__group_size

    @property
    def root(self) -> Node:
        return self.__root

    def __create_tree(self, node_list: list[Node], round_counter: int) -> Node:
        """
        TournamentTreeを作成
        [INFO] TournamentTree作成時、ノードをまとめる処理が入ります

        ex1) lst = [1, 2, 3, 4], group_size = 2

             Node([],3)
                    |
            +----------------+
            |                |
        Node([1,3],1)   Node([2,4],2)

        ex2) lst = [1, 2, 3, 4, 5], group_size = 2

                    Node([],4)
                        |
               +------------------+
               |                  |
            +------+          Node([3,4],3)
            |      |
            |    Node([2],2)
            |
        Node([1,5],1)
        """
        if len(node_list) == 1:  # nodeが１つに収束したら終了
            root = node_list[0]
            root.round = round_counter
            return root  # ルートノードだけを返す

        parent_node_list = []  # node_listからみて親となるノードのリスト
        # group_sizeごとに親ノードを作成する
        for group_start_index in range(0, len(node_list), self.__group_size):
            value_list, children = [], []
            group_end_index = group_start_index + self.__group_size
            for child in node_list[group_start_index:group_end_index]:
                if child.is_leaf and child.has_single_value:
                    # 親ノードが子ノードを吸収
                    value_list.extend(child.value_list)
                else:
                    # 子ノードを親ノードの子として追加
                    children.append(child)

            parent_node = TournamentTree.Node(value_list, children)
            parent_node_list.append(parent_node)

            for child in parent_node.children:  # 子ノードにroundとparent_nodeを付与
                child.round = round_counter
                round_counter += 1
                child.parent_node = parent_node

        return self.__create_tree(parent_node_list, round_counter)  # 再帰

    def __create_node_list(self, lst: list, group_size: int):
        """
        TournamentTreeの末端ノードリストを作成

        ex1) lst = [1, 2, 3, 4], group_size = 2

            [ ]
             |
          +-----+
        [1,3] [2,4] <- 末端ノードリスト = [[1,3], [2,4]]

        ex2) lst = [1, 2, 3, 4, 5], group_size = 2

                [ ]
                 |
            +--------+
           [ ]      [ ]
            |        |
          +----+   +---+
        [1,5] [2] [3] [4] <- 末端ノードリスト = [[1,5], [2], [3], [4]]
        """
        node_list_size = TournamentTree.calc_node_list_size(lst, group_size)
        node_list = []

        for node_index in range(node_list_size):
            value_list = []
            for group_index in range(group_size):
                idx = node_index + (group_index * node_list_size)
                if len(lst) <= idx:
                    break
                value_list.append(lst[idx])
            node_list.append(TournamentTree.Node(value_list, []))

        return node_list

    @staticmethod
    def calc_node_list_size(lst: list, group_size: int) -> int:
        """
        TournamentTreeの末端ノード数を算出
        [INFO] 詳細な挙動はテストを見て

        ex1) lst = [1, 2, 3, 4], group_size = 2

            [ ]
             |
          +-----+
        [1,3] [2,4] <- 末端ノード数 = 2

        ex2) lst = [1, 2, 3, 4, 5], group_size = 2

                [ ]
                 |
            +--------+
           [ ]      [ ]
            |        |
          +----+   +---+
        [1,5] [2] [3] [4] <- 末端ノード数 = 4
        """
        if len(lst) < 2 or group_size < 2:
            return -1

        node_list_size = 1
        while node_list_size * group_size < len(lst):
            node_list_size *= group_size
        return node_list_size

    @classmethod
    def bfs_iterator(cls, root: Node):
        queue = deque([root])

        while queue:
            node = queue.popleft()
            yield node
            queue.extend(node.children)  # 子ノードを追加

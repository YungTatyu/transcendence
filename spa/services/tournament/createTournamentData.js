export function createTournamentData(tournamentJsonData) {
  // https://www.aropupu.fi/bracket/ ライブラリの入力形式のDataを作成

  // INFO roundが昇順になるようにソートしておく
  const matchesData = tournamentJsonData.matches_data.sort(
    (a, b) => a.round - b.round,
  );
  return {
    teams: createTeams(matchesData),
    results: [createResults(matchesData)],
  };

  function createTeams(matchesData) {
    const teams = [];

    for (const matchData of matchesData) {
      const ids = [];
      // INFO 並び順が固定されるようにソートする
      sortParticipants(matchData.participants, teams);
      for (const participant of matchData.participants) {
        // INFO すでにteamsに登録したユーザーは登録しない
        if (teams.some((subArray) => subArray.includes(participant.id))) {
          continue;
        }
        ids.push(participant.id);
      }

      if (ids.length === 1) ids.push(null);
      if (ids.length) teams.push(ids);
    }
    return padTeamsWithNull(teams);
  }

  function createResults(matchesData) {
    const treeDepth = getTreeDepth(matchesData.length);
    let results = Array.from({ length: treeDepth }, () => []);
    // INFO アルゴリズムの都合上、降順でソートされていた方が都合が良い
    const reversedMatchesData = matchesData.reverse();

    let nodeIndex = 1;
    for (const matchData of reversedMatchesData) {
      let scores = [];
      for (const participant of matchData.participants) {
        scores.push(participant.score);
      }
      if (scores.length === 0) {
        scores = [null, null];
      }
      results[getTreeDepth(nodeIndex++) - 1].unshift(scores);
    }
    // 早いroundが先にくるように逆順にする(ライブラリの仕様上)
    results = results.reverse();
    // 末端ノードの数になるまで[null, null]で埋める(ライブラリの仕様上必要)
    while (results[0].length < getLeafNodeCount(treeDepth)) {
      results[0].push([null, null]);
    }
    return results;
  }

  function getLeafNodeCount(depth) {
    // 末端ノードの数を算出
    return 2 ** depth / 2;
  }

  function getTreeDepth(nodeCount) {
    // 木の深さを算出
    return Math.floor(Math.log2(nodeCount)) + 1;
  }

  function sortParticipants(participants, teams) {
    // トーナメント表でより早く登録された参加者を左に配置するようにソート
    const teamIds = teams.flat();

    participants.sort((a, b) => {
      const aIndex = teamIds.indexOf(a.id);
      const bIndex = teamIds.indexOf(b.id);

      // teamIdsに存在する場合、indexが-1ではないので優先順位をつける
      if (aIndex !== -1 && bIndex !== -1) {
        return aIndex - bIndex; // 既に登録されているidはteamIdsの順に並べる
      }
      if (aIndex !== -1) {
        return -1; // a.idが登録されていれば先に
      }
      if (bIndex !== -1) {
        return 1; // b.idが登録されていれば先に
      }
      return 0; // どちらも登録されていなければ元の順番を保つ
    });
  }

  function padTeamsWithNull(teams) {
    /*
     * teamsのサイズが2のN乗になるまで要素数2の配列を分割し、nullをパディング
     *
     * ex) [[1,2],[3,null],[4,5]] -> [[1,2],[3,null],[4,null],[5,null]]
     *     [[1,2],[3,4],[5,6]] -> [[1,2],[3,4],[5,null],[6,null]]
     *     [[1,2],[3,4],[5,6],[7,null]] -> [[1,2],[3,4],[5,6],[7,null]]
     */
    // teamsのサイズが2のN乗になるまで処理する
    while (!Number.isInteger(Math.log2(teams.length))) {
      for (let i = teams.length - 1; i >= 0; i--) {
        if (teams[i].length === 2) {
          const [a, b] = teams[i];
          // 元の配列の同じ位置に挿入
          teams.splice(i, 1, [a, null], [b, null]);
          break;
        }
      }
    }
    return teams;
  }
}

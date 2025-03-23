export function createTournamentData(tournamentJsonData) {
  // INFO roundが昇順になるようにソートしておく
  const matchesData = tournamentJsonData.matches_data.sort(
    (a, b) => a.round - b.round,
  );
  const tournamentData = {
    teams: createTeams(matchesData),
    results: [createResults(matchesData)],
  };
  return tournamentData;
}

function createTeams(matchesData) {
  const teams = [];
  let byeWinFlag = false;

  for (const matchData of matchesData) {
    const ids = [];
    for (const participant of matchData.participants) {
      // INFO すでにteamsに登録したユーザーは登録しない
      if (teams.some((subArray) => subArray.includes(participant.id))) {
        continue;
      }
      ids.push(participant.id);
    }

    if (ids.length === 0) continue;

    // INFO 1人の場合、不戦勝として扱い、これ以降のユーザーも不戦勝として扱う
    if (ids.length === 1) {
      teams.push([ids[0], null]);
      byeWinFlag = true;
      continue;
    }

    // 不戦勝フラグが立っている場合、残りのユーザーも不戦勝として扱う
    if (byeWinFlag) {
      teams.push(...ids.map((id) => [id, null]));
    } else {
      teams.push(ids);
    }
  }
  return teams;
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

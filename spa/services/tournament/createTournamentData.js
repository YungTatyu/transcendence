export function createTournamentData(tournamentJsonData) {
  const matchesData = tournamentJsonData.matches_data.sort(
    (a, b) => a.round - b.round,
  );
  const tournamentData = {
    teams: createTeams(matchesData),
    results: [createResults(matchesData)],
  };
  console.log(tournamentData);
  return tournamentData;
}

function createTeams(matchesData) {
  const teams = [];
  const registeredUser = [];

  for (const matchData of matchesData) {
    const ids = [];
    for (const participant of matchData.participants) {
      if (registeredUser.includes(participant.id)) {
        continue;
      }
      ids.push(participant.id);
      registeredUser.push(participant.id);
    }
    if (ids.length !== 0) {
      if (ids.length !== 2) {
        ids.push(null);
      }
      teams.push(ids);
    }
  }
  return teams;
}

function createResults(matchesData) {
  const resultsSize = getTreeDepth(matchesData.length);
  let results = Array.from({ length: resultsSize }, () => []);
  const reversedMatchesData = matchesData.reverse();

  let i = 1;
  for (const matchData of reversedMatchesData) {
    let scores = [];
    for (const participant of matchData.participants) {
      scores.push(participant.score);
    }
    if (scores.length === 0) {
      scores = [null, null];
    }
    results[getTreeDepth(i) - 1].unshift(scores);
    i++;
  }
  results = results.reverse();
  while (results[0].length < getLeafNodeCount(resultsSize)) {
    results[0].push([null, null]);
  }
  return results;
}

function getLeafNodeCount(depth) {
  // 末端ノードの数を算出
  return 2 ** depth;
}

function getTreeDepth(nodeCount) {
  // 木の深さを算出
  return Math.floor(Math.log2(nodeCount)) + 1;
}

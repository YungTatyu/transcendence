import TitileAndHomeButton from "../components/titleAndHomeButton.js";
import config from "../config.js";
import stateManager from "../stateManager.js";

export default function Profile() {
  function UserInfo(className, jsClass,text) {
    return `
      <div class="${className}">
        <p class="user-profile-text me-2 ${jsClass}">${text}</p>
        <img src="./assets/pencil.png" class="pencil-icon align-self-start mt-n1">
      </div>
        `;
  }

  function UserMatchHistory(idName) {
    //Loadingの部分はAPIから取得した値で上書きする
    return `
      <div id="row-data " class="row row-cols-3">
          <div class="col">loading...</div>
          <div class="col">loading...</div>
          <div class="col">loading...</div>
      </div>
      <div id="row-label " class="row row-cols-3">
          <div class="col">"Wins"</div>
          <div class="col">"Losses"</div>
          <div class="col">"Tournament Wins"</div>
      </div>
        `;
  }

  return `

    ${TitileAndHomeButton("PROFILE")}
    
    <div class="d-flex flex-column align-items-center">
      <div class="d-inline-flex align-items-center mt-5">
          <img src="./assets/42.png" class="square-img-user-avatar rounded-circle me-2 js-user-avatar" >
          <img src="./assets/pencil.png" class="pencil-icon align-self-start mt-n1">
      </div>

      ${UserInfo("d-inline-flex align-items-center mt-5", "js-username", "UserName")}
      ${UserInfo("d-inline-flex align-items-center", "js-password","Password")}
      ${UserInfo("d-inline-flex align-items-center", "js-mail","Mail")}

     
    </div>

    <div class="container text-center mt-4 match-record">
      ${UserMatchHistory()}
    </div>

    <div class="d-grid gap-2 col-4 mx-auto mt-5">
      <button class="match-history-button btn btn-primary rounded-pill js-match-history-button" type="button">Match History</button>
    </div>

    `;
}

export  async function setupProfile(){

  if(stateManager.state.username && stateManager.state.avatar_path){
    document.querySelector(".js-username").textContent = stateManager.state.username;
    document.querySelector(".js-user-avatar").src = stateManager.state.avatar_path;
  
  }else{
    const respose= await fetch(`${config.userService}/users?userid=${stateManager.state.userId}`);
    const status = respose.status;
    const data = await respose.json();
    
    if (status === null) {
      errorOutput.textContent = "Error Occured!";
      return;
    }
    if (status >= 400) {
      errorOutput.textContent = JSON.stringify(data.error, null, "\n");
      return;
    }
    document.querySelector(".js-username").textContent = data.username;
    document.querySelector(".js-user-avatar").src = data.avatar_path;


    stateManager.setState({username: data.username});
    stateManager.setState({avatar_path: data.avatar_path});
  }
  
  const matchHistoryButton = document.querySelector(".js-match-history-button");
  matchHistoryButton.addEventListener("click", async () => {
    SPA.navigate("/history/match");
  });

  
}
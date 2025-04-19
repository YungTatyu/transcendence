export default function TitleMatchingRoom(titleText) {
  return `
    <div class="container text-center">
      <div class="row">
        <div class="col align-self-start">
          <h1 class="title-matching-room">${titleText}</h1>
        </div>
          <div class="position-relative">
            <img src="/assets/home.png" class="home-icon position-absolute top-0 end-0" style="margin-top: 5%;" onclick="SPA.navigate('/home')">
          </div>
      </div>
    </div>
  `;
}

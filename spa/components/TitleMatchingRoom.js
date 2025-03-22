export default function TitleMatchingRoom(titleText) {
  return `
    <div class="container text-center">
      <div class="row">
        <div class="col align-self-start">
          <h1 class="title-matching-room mr-first">${titleText}</h1>
          <h1 class="title-matching-room mr-second">${titleText}</h1>
          <h1 class="title-matching-room mr-third">${titleText}</h1>
        </div>
          <div class="position-relative">
            <img src="/assets/home.png" class="home-icon position-absolute top-0 end-0" style="margin-top: 5%;">
          </div>
      </div>
    </div>
  `;
}

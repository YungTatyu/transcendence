export default function TitileAndHomeButton(titleText) {
  return `
        <div class="container text-center">
            <div class="row">
                <div class="col align-self-start">
                    <p class="title text-start">${titleText}</p>
                </div>
                <div class="col align-self-end">
                    <div class="position-relative">
                        <img src="./assets/home.png" class="home-icon position-absolute top-0 end-0" onclick="SPA.navigate('/')">
                    </div>
                </div>
            </div>
        </div>
        `;
}

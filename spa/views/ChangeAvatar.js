export default function ChangeAvatar() {
    const formHtml = `
        <div class="container d-flex justify-content-center align-items-center vh-100">
          <div class="card shadow-lg p-4 d-flex flex-column align-items-center justify-content-center" style="width: 100%; max-width: 400px;">
            <form class="d-flex flex-column align-items-center justify-content-center">
              <img id="user-avatar" src="./assets/42.png" alt="ロゴ" class="square-img-user-avatar rounded-circle mb-3" >
              
              <div class="d-flex justify-content-center gap-2">
                <button id="change-avatar" class="btn btn-primary btn-lg w-75" type="button">Edit</button>
                <button id="delete-avatar" class="btn btn-danger btn-lg w-75" type="button">Delete</button>
              </div>
            </form>
          </div>
        </div>
      `;
    return formHtml;
}

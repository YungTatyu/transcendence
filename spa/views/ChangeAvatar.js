export default function ChangeAvatar() {
  return `
        <div class="container d-flex justify-content-center align-items-center vh-100">
          <div class="card shadow-lg p-4 align-items-center" style="width: 100%; max-width: 400px;">
            <form>    
              <img id="user-avatar" src="/assets/user.png" class="square-img-user-avatar rounded-circle mb-3 js-new-avatar" >
               
              <!-- 隠しファイル入力 -->
              <input type="file" class="js-avatar-input d-none" accept="image/*">
          
              <div class="d-flex gap-2 mt-4">
                <button class="btn btn-primary w-50 js-edit-avatar" type="button">Edit</button>
                <button class="btn btn-danger w-50 js-delete-avatar" type="button">Delete</button>
              </div>
            </form>
          </div>
        </div>
      `;
}

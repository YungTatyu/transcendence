import { fetchData, deleteData, postData } from "./api.js";
import { fetchUsers } from "./users.js";

const TOKEN = "token"
const USER_ID = "userId"
const USER_NAME = "username"
const LOGIN_TOKEN = localStorage.getItem(TOKEN)
const LOGIN_USER_ID = localStorage.getItem(USER_ID)
const LOGIN_USER_NAME = localStorage.getItem(USER_NAME)


function transformTime(dateString) {
  const date = new Date(dateString);
  const now = new Date();

  const diffInSeconds = Math.floor((now - date) / 1000); // 経過時間（秒単位）
  const diffInMinutes = Math.floor(diffInSeconds / 60); // 経過時間（分単位）
  const diffInHours = Math.floor(diffInMinutes / 60); // 経過時間（時間単位）
  const diffInDays = Math.floor(diffInHours / 24); // 経過時間（日単位）

  const year = date.getFullYear();
  const month = date.getMonth() + 1; // 月（0始まりなので1を足す）
  const day = date.getDate();


  // 経過時間に基づく表示
  let timeText;
  if (diffInSeconds < 60) {
    timeText = `${diffInSeconds}秒前`;
  } else if (diffInMinutes < 60) {
    timeText = `${diffInMinutes}分前`;
  } else if (diffInHours < 24) {
    timeText = `${diffInHours}時間前`;
  } else if (diffInDays < 31) {
    timeText = `${diffInDays}日前`;
  } else {
    timeText = `${year}年${month}月${day}日`;
  }
  return timeText;
}

async function logout(event) {
  event.preventDefault()
  if (!confirm(`${LOGIN_USER_NAME}をログアウトしますか？`)) {
    return
  }
  const response = await postData("http://127.0.0.1:8000/users/logout/")
  if (response === null) {
    alert("logout失敗しました")
    return
  }
  localStorage.removeItem(TOKEN)
  localStorage.removeItem(USER_ID)
  localStorage.removeItem(USER_NAME)
  window.location.href = 'login.html';
}

function renderHeader() {
  const headerEle = document.querySelector(".js-index-header")
  const navEle = document.createElement("nav")
  console.log(LOGIN_TOKEN, LOGIN_USER_ID, LOGIN_USER_NAME)
  navEle.innerHTML = `
        <div class="d-flex">
          <div class="h3">
            <h3>notes</h3>
          </div>
          <div class="auth-buttons ms-auto">
            ${LOGIN_USER_ID === null ? `
            <a href="login.html" class="btn btn-primary">ログイン</a>` : `
            <button type="button" class="btn btn-danger js-logout">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-box-arrow-right" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0z"/>
                <path fill-rule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708z"/>
              </svg>
            </button>
            <a href="note.html" class="btn btn-primary btn-lg">
              new note
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                class="bi bi-plus-circle" viewBox="0 0 16 16">
                <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14m0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16" />
                <path
                  d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4" />
              </svg>
            </a>`}
          </div>
        </div>`
  headerEle.appendChild(navEle)
  const logoutEl = navEle.querySelector(".js-logout")
  if (logoutEl === null) {
    return
  }
  logoutEl.addEventListener("click", logout)
}

async function renderNoteList() {

  const [notes_data, users] = await Promise.all([
    fetchData("http://127.0.0.1:8000/"),
    fetchUsers()
  ]);
  if (notes_data === null) {
    console.error("Failed to fetch notes.");
    return
  }
  const notes = notes_data.results
  const noteContainer = document.querySelector(".js-note-container");
  notes.forEach(note => {
    const noteEle = document.createElement("section")
    noteEle.className = `js-note border p-3 mb-1`
    noteEle.innerHTML = `
        <div class="note-header d-flex">
          <div class="author pe-1">${users[note.author].username}</div>
          <div class="post-time">${transformTime(note.created_at)}</div>

          ${LOGIN_USER_ID === note.author.toString() ? `
          <div class="js-note-actions ms-auto p-2 d-flex gap-2">
            <a href=note.html?noteId=${note.id} class="btn btn-outline-warning btn-sm">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                class="bi bi-pencil-square" viewBox="0 0 16 16">
                <path
                  d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z" />
                <path fill-rule="evenodd"
                  d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z" />
              </svg>
            </a>
            <form class="js-note-delete" data-note-id=${note.id}>
              <button type="submit" class="btn btn-outline-danger btn-sm">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash"
                  viewBox="0 0 16 16">
                  <path
                    d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z" />
                  <path
                    d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z" />
                </svg>
              </button>
            </form>
          </div> ` : ''}

        </div>
        <h5 class="note-title">${note.title}</h5>
        <p class="note-content">${note.content}</p>
    `
    noteContainer.appendChild(noteEle)
    const deleteForm = noteEle.querySelector(".js-note-delete");
    if (deleteForm === null) {
      return
    }
    deleteForm.addEventListener("submit", (event) => deleteNote(deleteForm, event));
  });
}

async function deleteNote(form, event) {
  event.preventDefault()
  console.log("form", form)
  if (!confirm("本当にこのノートを削除しますか？")) {
    return
  }
  const noteId = form.getAttribute("data-note-id")
  const res = await deleteData(`http://127.0.0.1:8000/notes/delete/${noteId}/`)
  if (res === null) {
    alert("noteの削除に失敗しました")
    return
  }
  console.log("delete res=", res)
  const el = form.closest(".js-note")
  el.remove()
}

function renderPage() {
  renderHeader()
  renderNoteList()
}

renderPage()


import { fetchData, postData } from "./api.js";

const urlParams = new URLSearchParams(window.location.search);


async function renderNoteValue() {
  if (urlParams.size === 0) {
    return
  }
  const noteId = urlParams.get('noteId');
  const note = await fetchData(`http://127.0.0.1:8000/notes/${noteId}/`)
  const title = document.querySelector(".js-form-title")
  const content = document.querySelector(".js-form-content")
  title.value = note.title
  content.value = note.content
}

async function save(event) {
  event.preventDefault()
  console.log(event)
  const title = document.querySelector(".js-form-title")
  const content = document.querySelector(".js-form-content")
  const option = {
    title: title,
    content: content,
  }
  if (urlParams.size === 0) {
    postData("http://127.0.0.1:8000/notes/create/", option)
    return
  }
  postData(`http://127.0.0.1:8000/notes/${noteId}/`, option)
  window.location.href = "index.html"; // ログイン後のページ
}

renderNoteValue()
document.querySelector(".js-note-container").addEventListener("submit", save)

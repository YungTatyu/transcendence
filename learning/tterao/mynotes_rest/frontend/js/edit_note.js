import { fetchData, postData } from "./api.js";

const urlParams = new URLSearchParams(window.location.search);
const noteId = urlParams.get('noteId');

async function renderNoteValue() {
  if (urlParams.size === 0) {
    return
  }
  const note = await fetchData(`http://127.0.0.1:8000/notes/${noteId}/`)
  const title = document.querySelector(".js-form-title")
  const content = document.querySelector(".js-form-content")
  title.value = note.title
  content.value = note.content
}

function handleResponse(res) {
  if (res === null) {
    alert("ノートの保存に失敗しました。");
    return
  }
  console.log(res)
  window.location.href = "index.html";
}

async function save(event) {
  event.preventDefault()
  const title = document.querySelector(".js-form-title").value
  const content = document.querySelector(".js-form-content").value
  const option = {
    title: title,
    content: content,
  }
  if (urlParams.size === 0) {
    const res = await postData("http://127.0.0.1:8000/notes/create/", option)
    handleResponse(res)
    return
  }
  const res = await postData(`http://127.0.0.1:8000/notes/update/${noteId}/`, option, "PUT")
  handleResponse(res)
}

renderNoteValue()
document.querySelector(".js-note-container").addEventListener("submit", save)

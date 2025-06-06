export default function Form(fields, buttonId, submitText, title = null) {
  let formContent = "";

  if (title) {
    formContent += `<p class="text-center text-black  fw-bold fs-4">${title}</p>`;
  }

  fields.forEach((field, _) => {
    const placeholder = field.placeholder || "";
    formContent += `
          <div class="mb-3">
            <label class="form-label">${field.label}</label>
            <input type="${field.type}" class="form-control" id="field${field.label}" placeholder="${placeholder}" required>
          </div>
        `;
  });

  const formHtml = `
      <div class="container d-flex justify-content-center align-items-center vh-100">
        <div class="gradient-border-wrapper">
          <div class="form-wrapper">
            <form>
              ${formContent}
              <div class="text-end">
                <button id="${buttonId}" class="btn btn-primary btn-lg form-btn" type="button">
                  ${submitText}
                </button>
              </div>
                <div>
              <p id="errorOutput" class="text-center text-danger fw-bold fs-6"></p>
            </div>
            </form>
          </div>
        </div>
      </div>
	`;
  return formHtml;
}

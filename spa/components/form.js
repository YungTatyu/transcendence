export default function generateForm(fields, buttonId, submitText) {
  let formContent = "";
  fields.forEach((field, index) => {
    const placeholder = field.placeholder || "";
    const required = field.required ? "required" : "";
    formContent += `
			<div class="mb-3">
                <label for="field${index}" class="form-label">${field.label}</label>
                <input type="${field.type}" class="form-control" id="field${field.label}" placeholder="${placeholder}" ${required}>
            </div>
        `;
  });

  const formHtml = `
		<div class="container d-flex justify-content-center align-items-center vh-100">
			<div class="card shadow-lg p-4" style="width: 100%; max-width: 400px;">
				<form class="rounded-pill">
					${formContent}
					<div class="text-end">
						<button id="${buttonId}" class="btn btn-primary btn-lg" type="button">${submitText}</button>
					</div>
				</form>
			</div>
		</div>
	`;
  return formHtml;
}

import Form from "../components/Form.js";

export default function ChangeMail() {
  const ChangeMailFormField = [
    { label: "Mail", type: "email", placeholder: "sample@example.com" },
  ];
  return Form(ChangeMailFormField, "changeMail", "Submit", "Set Your Mail");
}

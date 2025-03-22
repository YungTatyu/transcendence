import Form from "../components/Form.js";

export default function ChangePassword() {
  const ChangePasswordFormField = [
    { label: "OLD", type: "Password", placeholder: "password123" },
    { label: "NEW", type: "Password", placeholder: "password123" },
  ];
  return Form(
    ChangePasswordFormField,
    "changePassword",
    "Submit",
    "Set Your Password",
  );
}

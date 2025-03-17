import Form from "../components/Form.js"

export default function ChangeUsername(){
    const ChangeNameFormField = [{label: "Username", type: "username", placeholder: "New Username"}];
    return Form(ChangeNameFormField, "ChangeName", "Submit");
}
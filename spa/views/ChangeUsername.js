import Form from "../components/Form.js";
import fetchApiWithBody from "../api/fetchApiWithBody.js";
import config from "../config.js";
import stateManager from "../stateManager.js";

export default function ChangeUsername(){
    const ChangeNameFormField = [{label: "Username", type: "username", placeholder: "New Username"}];
    return Form(ChangeNameFormField, "changeUsername", "Submit","Set Your Username");
}


export function setupChageUsername(){
    const submitButton = document.getElementById("chnageUsername");

    submitButton.addEventListener("click", async () => {
        const new_username = document.getElementById("fieldUsername").value;
        
        const requestBody = {
            username: new_username,
        };

        const {status, data} = await fetchApiWithBody(
            "PUT",
            config.userService,
            "/users/me/username",
            requestBody,
        );

        console.log(data);

        if (status === null) {
            errorOutput.textContent = "Error Occured!";
            return;
        }
        if (status >= 400) {
            errorOutput.textContent = JSON.stringify(data.error, null, "\n");
            return;
        }
    })
       
}
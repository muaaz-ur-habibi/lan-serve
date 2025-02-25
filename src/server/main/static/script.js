function getMessageRecipientName(button) {
    const text_field = document.getElementById("recipient-holder");

    text_field.value = button.innerText;
}
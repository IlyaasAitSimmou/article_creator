
document.addEventListener('DOMContentLoaded', () => {


    const editArticleButton = document.querySelectorAll('.editArticleButton')

    const editArticleForm = document.querySelectorAll('.editArticleForm')

    const deleteArticleButton = document.querySelectorAll('.deleteArticleButton')

    const deleteArticleForm = document.querySelectorAll('.deleteArticleForm')

    const displayNone = (elementList) => {elementList.forEach((element) => element.style.display = 'none')}

    displayNone(editArticleForm)
    displayNone(deleteArticleForm)

    editArticleButton.forEach((button) => {
        button.addEventListener('click', () => {
            const editArticleFormElement = Array.from(editArticleForm).find(
                (form) => {
                    return form.parentElement === button.parentElement
                });
            if (editArticleFormElement) {
                editArticleFormElement.style.display = 'block';
                displayNone(Array.from(editArticleForm).filter((form) => form !== editArticleFormElement))
            }
        });
    });



    deleteArticleButton.forEach((button) => {
        button.addEventListener('click', () => {
            const deleteArticleFormElement = Array.from(deleteArticleForm).find(
                (form) => {
                    return form.parentElement === button.parentElement
                });
            if (deleteArticleFormElement) {
                deleteArticleFormElement.style.display = 'block';
                const buttons = deleteArticleFormElement.getElementsByTagName('button')
                Array.from(buttons).forEach((button) => button.addEventListener('click', () => {
                    deleteArticleFormElement.style.display = 'none'
                }))
                displayNone(Array.from(deleteArticleForm).filter((form) => form !== deleteArticleFormElement))
            }
        });
    });


    const handleOutsideClickEvent = (event) => {
        if (!event.target.closest('.editArticleForm') && !event.target.closest('.editArticleButton')) {
            displayNone(editArticleForm)
        }
    }

    document.addEventListener('click', handleOutsideClickEvent);
})
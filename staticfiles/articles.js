
document.addEventListener('DOMContentLoaded', () => {
    const ArticleForm = document.getElementById('articleForm')
    const ProjectForm = document.getElementById('projectForm')

    const createArticleButton = document.getElementById('createArticleButton')
    const createProjectButton = document.getElementById('createProjectButton')

    const editArticleButton = document.querySelectorAll('.editArticleButton')
    const editProjectButton = document.querySelectorAll('.editProjectButton')

    const editArticleForm = document.querySelectorAll('.editArticleForm')
    const editProjectForm = document.querySelectorAll('.editProjectForm')

    const deleteArticleButton = document.querySelectorAll('.deleteArticleButton')
    const deleteProjectButton = document.querySelectorAll('.deleteProjectButton')

    const deleteArticleForm = document.querySelectorAll('.deleteArticleForm')
    const deleteProjectForm = document.querySelectorAll('.deleteProjectForm')

    const displayNone = (elementList) => {elementList.forEach((element) => element.style.display = 'none')}

    displayNone([ArticleForm, ProjectForm])
    displayNone(editArticleForm)
    displayNone(editProjectForm)
    displayNone(deleteArticleForm)
    displayNone(deleteProjectForm)

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

    editProjectButton.forEach((button) => {
        button.addEventListener('click', () => {
            const editProjectFormElement = Array.from(editProjectForm).find(
                (form) => form.parentElement === button.parentElement
            );
            if (editProjectFormElement) {
                editProjectFormElement.style.display = 'block';
                displayNone(Array.from(editProjectForm).filter((form) => form !== editProjectFormElement))
            }
        });
    });



    // editProjectButton.addEventListener('click', () => {
    //     editArticleForm.style.display = 'none'
    //     editProjectForm.style.display = 'block'
    // })




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

    deleteProjectButton.forEach((button) => {
        button.addEventListener('click', () => {
            const deleteProjectFormElement = Array.from(deleteProjectForm).find(
                (form) => {
                    return form.parentElement === button.parentElement
                });
            if (deleteProjectFormElement) {
                deleteProjectFormElement.style.display = 'block';
                const buttons = deleteProjectFormElement.getElementsByTagName('button')
                Array.from(buttons).forEach((button) => button.addEventListener('click', () => {
                    deleteProjectFormElement.style.display = 'none'
                }))
                displayNone(Array.from(deleteProjectForm).filter((form) => form !== deleteProjectFormElement))
            }
        });
    });


    // deleteArticleButton.addEventListener('click', () => {
    //     deleteArticleForm.style.display = 'block'
    //     deleteProjectForm.style.display = 'none'
    //     const deleteArticleFormButtons = deleteArticleForm.getElementsByTagName('button')
    //     deleteArticleFormButtons.foreach((button) => button.addEventListener('click', () => {
    //         deleteArticleForm.style.display = 'none'
    //     }))

    // })

    // deleteProjectButton.addEventListener('click', () => {
    //     deleteArticleForm.style.display = 'none'
    //     deleteProjectForm.style.display = 'block'
    //     const deleteProjectFormButtons = deleteProjectForm.getElementsByTagName('button')
    //     deleteProjectFormButtons.foreach((button) => button.addEventListener('click', () => {
    //         deleteProjectForm.style.display = 'none'
    //     }))

    // })


    const handleOutsideClickEvent = (event) => {
        if (!event.target.closest('#articleForm') && !event.target.closest('#createArticleButton')) {
            ArticleForm.style.display = 'none';
        }
        if (!event.target.closest('#projectForm') && !event.target.closest('#createProjectButton')) {
            ProjectForm.style.display = 'none';
        }
        if (!event.target.closest('.editArticleForm') && !event.target.closest('.editArticleButton')) {
            displayNone(editArticleForm)
        }
        if (!event.target.closest('.editProjectForm') && !event.target.closest('.editProjectButton')) {
            displayNone(editProjectForm)
        }
    }

    createArticleButton.addEventListener('click', () => {
        ProjectForm.style.display = 'none'
        ArticleForm.style.display = 'block'
    })
    createProjectButton.addEventListener('click', () => {
        ProjectForm.style.display = 'block'
        ArticleForm.style.display = 'none'
    })
    document.addEventListener('click', handleOutsideClickEvent);
})
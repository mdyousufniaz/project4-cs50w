document.addEventListener('DOMContentLoaded', () => {
    const likeIcon = document.querySelector('#like');
    
    likeIcon.onclick = () => {
        if(likeIcon.className.endsWith('-fill')){
            likeIcon.className = likeIcon.className.replace('-fill', '');
            likeIcon.style.color = 'black';
        }else{
            likeIcon.className = likeIcon.className.trim();
            likeIcon.className += '-fill';
            likeIcon.style.color = 'yellow';
            likeIcon.style.stroke = 'black';
        }
    }
    const editLink = document.querySelector('#edit');

    editLink.addEventListener('click', async () => {
        likeIcon.style.display = 'none';
        const postId = editLink.dataset.post_id;
        console.log(typeof postId);
        const contentDiv = document.querySelector('.lead');
        console.log(contentDiv);

        contentDiv.innerHTML = `<textarea class="form-control mr-5" name="content" rows="5" maxlength="1000"
                                required id="edit_content">${await loadContent(postId)}</textarea>`;


        const save_btn = document.createElement('button');
        save_btn.innerHTML = 'Save';
        save_btn.className = 'btn btn-sm btn-success';
        save_btn.onclick = async () => {
            const textarea = contentDiv.querySelector('textarea');
            const content = textarea.value.trim();

            if (!content) {
                alert('Content cannot be blank.');
                textarea.focus();
                return;
            }

            fetch(`/content/${postId}`, {
                method: 'PUT',
                body: JSON.stringify({
                    content: content
                })
            });

            console.log(contentDiv.querySelector('textarea').value);
            contentDiv.innerHTML = `<p>${await loadContent(postId)}</p>`
            save_btn.parentElement.replaceChild(editLink, save_btn);
            likeIcon.style.display = 'block';
        }
        editLink.parentElement.replaceChild(save_btn, editLink);


        
    })

    async function loadContent(post_id){
        try{
            const response = await fetch(`/content/${post_id}`);
            const data = await response.json();
            console.log(data);
            return data.content;
        }catch(error){
            console.error('Error loading content:', error);
        }
    }

    function likePost(post_id){
        
    }
    
});

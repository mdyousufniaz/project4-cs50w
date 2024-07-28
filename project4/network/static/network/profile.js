document.addEventListener('DOMContentLoaded', () => {

    const post_btn = document.querySelector('#post_btn');
    const post_form = post_btn.parentElement.querySelector('form');
    post_form.style.display = 'none';

    post_btn.onclick = () => {
        if(post_btn.innerHTML === 'New Post'){
            post_btn.innerHTML = 'Close';
            post_btn.className = post_btn.className.replace('primary', 'danger');
            post_form.style.display = 'block';
        }else{
            post_btn.innerHTML = 'New Post';
            post_btn.className = post_btn.className.replace('danger', 'primary');
            post_form.style.display = 'none';
        }

    };
});

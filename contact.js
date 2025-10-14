// 元素获取
const backToLoginFromContact = document.getElementById('back-to-login-from-contact');
const smiley = document.getElementById('smiley');
const smileyModal = document.getElementById('smiley-modal');
const smileyModalClose = document.getElementById('smiley-modal-close');

// 显示弹窗
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}

// 隐藏弹窗
function hideModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// 返回登录页
backToLoginFromContact.addEventListener('click', () => {
    window.location.href = 'login.html';
});

// 笑脸点击事件
smiley.addEventListener('click', () => {
    smiley.classList.add('yellow');
    showModal('smiley-modal');
});

// 弹窗关闭按钮事件
smileyModalClose.addEventListener('click', () => {
    hideModal('smiley-modal');
});
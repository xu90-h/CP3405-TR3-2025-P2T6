// 元素获取
const signinBtn = document.getElementById('signin-btn');
const contactBtn = document.getElementById('contact-btn');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const emailModal = document.getElementById('email-modal');
const passwordModal = document.getElementById('password-modal');
const emailModalClose = document.getElementById('email-modal-close');
const passwordModalClose = document.getElementById('password-modal-close');

// 显示弹窗
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}

// 隐藏弹窗
function hideModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// 登录按钮点击事件
signinBtn.addEventListener('click', () => {
    if (!emailInput.value) {
        showModal('email-modal');
        return;
    }
    if (!passwordInput.value) {
        showModal('password-modal');
        return;
    }
    // 跳转到建筑选择页（实际项目中可通过路由或页面跳转实现）
    window.location.href = 'building.html';
});

// 联系我们按钮点击事件
contactBtn.addEventListener('click', () => {
    window.location.href = 'contact.html';
});

// 弹窗关闭按钮事件
emailModalClose.addEventListener('click', () => {
    hideModal('email-modal');
});
passwordModalClose.addEventListener('click', () => {
    hideModal('password-modal');
});
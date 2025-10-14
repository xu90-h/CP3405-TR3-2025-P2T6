// 元素获取
const backToLogin = document.getElementById('back-to-login');
const buildingItems = document.querySelectorAll('.building-item');

// 返回登录页
backToLogin.addEventListener('click', () => {
    window.location.href = 'login.html';
});

// 建筑项点击事件（跳转到订座页）
buildingItems.forEach(item => {
    item.addEventListener('click', () => {
        window.location.href = 'room.html';
    });
});
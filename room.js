// 元素获取
const backToBuilding = document.getElementById('back-to-building');
const seatGrid = document.getElementById('seat-grid');
const timer = document.getElementById('timer');
const reserveBtn = document.getElementById('reserve-btn');
const reserveModal = document.getElementById('reserve-modal');
const confirmReserve = document.getElementById('confirm-reserve');
const cancelReserve = document.getElementById('cancel-reserve');
const reserveMessage = document.getElementById('reserve-message');

// 生成座位：按正确顺序（A-J排，每排11个座位）
function generateSeats() {
    const rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']; // 10排
    const cols = 11; // 每排11个座位
    const totalSeats = rows.length * cols;
    // 模拟占用座位索引（匹配参考图）
    const occupiedIndexes = new Set([
        0, 7, 12, 6, 18, 25, 26, 33, 34, 41, 48, 49, 56, 63, 64, 71, 78, 85, 92, 99, 106, 107
    ]);

    let seatIndex = 0;
    for (let row of rows) {
        for (let col = 1; col <= cols; col++) {
            const seatId = `${row}${col}`;
            const seat = document.createElement('div');
            
            if (occupiedIndexes.has(seatIndex)) {
                seat.className = 'seat occupied';
            } else {
                seat.className = 'seat available';
                seat.addEventListener('click', () => toggleSeat(seat));
            }
            
            seat.dataset.id = seatId;
            seat.textContent = seatId;
            seatGrid.appendChild(seat);
            seatIndex++;
        }
    }
}

// 座位点击交互
function toggleSeat(seat) {
    if (seat.classList.contains('available')) {
        seat.classList.remove('available');
        seat.classList.add('selected');
    } else if (seat.classList.contains('selected')) {
        seat.classList.remove('selected');
        seat.classList.add('available');
    }
}

// 实时计时器
function updateTimer() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    timer.textContent = `${hours}:${minutes}:${seconds}`;
}

// 弹窗控制
function showModal(modal) {
    modal.style.display = 'flex';
}
function hideModal(modal) {
    modal.style.display = 'none';
}

// 事件绑定
backToBuilding.addEventListener('click', () => {
    window.location.href = 'building.html';
    clearInterval(timerInterval);
});

reserveBtn.addEventListener('click', () => {
    const selectedSeats = document.querySelectorAll('.selected');
    if (selectedSeats.length === 0) return;

    const selectedIds = Array.from(selectedSeats).map(seat => seat.dataset.id).join(', ');
    reserveMessage.textContent = `You selected seats: ${selectedIds}\nPlease confirm.`;
    showModal(reserveModal);
});

confirmReserve.addEventListener('click', () => {
    hideModal(reserveModal);
    window.location.href = 'checkin.html';
    clearInterval(timerInterval);
});

cancelReserve.addEventListener('click', () => {
    hideModal(reserveModal);
});

// 页面加载初始化
let timerInterval;
window.onload = () => {
    generateSeats();
    updateTimer();
    timerInterval = setInterval(updateTimer, 1000);
};
// firebase.js

// Firebase SDKs (v8 compatible UMD)
document.write('<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-app.js"></script>');
document.write('<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-auth.js"></script>');
document.write('<script src="https://www.gstatic.com/firebasejs/8.10.1/firebase-firestore.js"></script>');

document.write(`
<script>
  const firebaseConfig = {
    apiKey: "AIzaSyAw_fd_BH_PvE-rSVC9ll19I6m6fwSzJ9E",
    authDomain: "smartseat-attendance.firebaseapp.com",
    projectId: "smartseat-attendance",
    storageBucket: "smartseat-attendance.firebasestorage.app",
    messagingSenderId: "31865983136",
    appId: "1:31865983136:web:2262bacbf841f9527839c5",
    measurementId: "G-XF69TREY2N"
  };

  firebase.initializeApp(firebaseConfig);
  const auth = firebase.auth();
  const db = firebase.firestore();
</script>
`);

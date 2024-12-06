document.addEventListener('DOMContentLoaded', () => {
    const intro = document.querySelector('.intro');
    const mainContent = document.querySelector('.main-content');
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');
    const loginBtn = document.querySelector('.login-btn');
    const signupBtn = document.querySelector('.signup-btn');
    const loginModal = document.getElementById('loginModal');
    const signupModal = document.getElementById('signupModal');
    const closeBtns = document.querySelectorAll('.close');
    const tabLinks = document.querySelectorAll('.sidebar-menu a');
    const tabContents = document.querySelectorAll('.tab-content');

    // Обработка начального экрана
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            intro.classList.add('hidden');
            mainContent.classList.add('visible');
        }
    });

    intro.addEventListener('click', () => {
        intro.classList.add('hidden');
        mainContent.classList.add('visible');
        window.scrollTo(0, 100);
    });

    // Обработка бокового меню
    menuToggle.addEventListener('click', () => {
        menuToggle.classList.toggle('active');
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    });

    // Закрытие меню при клике на overlay
    overlay.addEventListener('click', () => {
        menuToggle.classList.remove('active');
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    });

    // Открытие модального окна для входа
    loginBtn.addEventListener('click', () => {
        loginModal.style.display = 'block';
        overlay.style.display = 'block';
    });

    // Открытие модального окна для регистрации
    signupBtn.addEventListener('click', () => {
        signupModal.style.display = 'block';
        overlay.style.display = 'block';
    });

    // Закрытие модальных окон
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            loginModal.style.display = 'none';
            signupModal.style.display = 'none';
            overlay.style.display = 'none';
        });
    });

    // Закрытие модальных окон при клике на overlay
    overlay.addEventListener('click', () => {
        loginModal.style.display = 'none';
        signupModal.style.display = 'none';
        overlay.style.display = 'none';
    });

    // Обработка переключения вкладок
    tabLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetTab = e.target.getAttribute('data-tab');

            tabLinks.forEach(tab => tab.classList.remove('active'));
            e.target.classList.add('active');

            tabContents.forEach(content => content.style.display = 'none');
            document.getElementById(targetTab).style.display = 'block';
        });
    });
});
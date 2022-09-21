

const sideMenu = document.querySelector('aside');
const menuBtn = document.querySelector('#menu-btn');
const closeBtn = document.querySelector('#close-btn');
var sidebar = document.getElementById('sidebar');
const themeToggler = document.querySelector('.theme-toggler');
var activePage = window.location.pathname;
const navLinks = document.querySelectorAll('aside a').forEach(link => {
 if(link.href.includes(`${activePage}`)){
   link.classList.add('active');
    console.log(link.href);
  }
})



themeToggler.addEventListener('click', () => {
	document.body.classList.toggle('dark-theme-variables');
	themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
	themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');
	

})



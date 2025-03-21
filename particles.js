document.querySelector('.hamburger-menu').addEventListener('click', function() {
    document.querySelector('.below-logo').classList.toggle('active');
});
function toggleMenu() {
    const navButtons = document.querySelector('.nav-buttons');
    navButtons.classList.toggle('show');
}
function toggleMenu() {
    const menu = document.getElementById('mobile-menu');
    const icon = document.getElementById('hamburger-icon');
    menu.classList.toggle('show');
    
    // Toggle icon between bars and close
    if (menu.classList.contains('show')) {
        icon.classList.replace('fa-bars', 'fa-times');
    } else {
        icon.classList.replace('fa-times', 'fa-bars');
    }
}
if (video.style.opacity == 0) {
    document.querySelector('.content').classList.add('show');
    slideshow.style.display = 'block';  // Corrected variable name
    showSlide(slideIndex); // Show the first slide
} else {
    document.querySelector('.content').classList.remove('show');
    slideshow.style.display = 'none';  // Corrected variable name
}
// Select the video and slide show elements
const video = document.getElementById('background-video');
const slideshow = document.getElementById('slideshow-container');
const content = document.querySelector('.slide');
let slideIndex = 0; // Initialize slide index

let lastScrollTop = 0 // Initialize scroll position tracker

// Add a scroll event listener to move the video
window.addEventListener('scroll', function () {
    // Get the scroll position
    let scrollPosition = window.scrollY;

    // If scrolling down, show the video and fade it out
    if (scrollPosition > lastScrollTop) {
        // Scroll Down
        video.style.opacity = Math.max(1 - scrollPosition * 0.003, 0); // Fade out the video
    } else {
        // Scroll Up
        video.style.opacity = Math.min(1 - scrollPosition * 0.003, 1); // Fade in the video
    }

    // If the video is fully faded, show the content and slideshow
    if (video.style.opacity == 0) {
        document.querySelector('.content').classList.add('show');
        slideshow.style.display = 'block';
        showSlide(slideIndex); // Show the first slide
    } else {
        document.querySelector('.content').classList.remove('show');
        slideshow.style.display = 'none';
    }

    // Update the last scroll position to the current one
    lastScrollTop = scrollPosition <= 0 ? 0 : scrollPosition; // Prevent negative values  
});

// Show the slide at the given index
function showSlide(index) {
    const slides = document.querySelectorAll('.slide');  // Define slides array
    slides.forEach((slide, i) => {
        slide.classList.remove('active');
        if (i === index) {
            slide.classList.add('active');
        }
    });

    // Move to the next slide after 3 seconds
    slideIndex = (slideIndex + 1) % slides.length;  // Fixed typo
    setTimeout(() => showSlide(slideIndex), 3000); // Change slide every 3 seconds
}

// Toggle menu visibility for mobile
function toggleMenu() {
    const menu = document.getElementById('mobile-menu');
    menu.style.display = (menu.style.display === 'block') ? 'none' : 'block';
}
window.addEventListener('scroll', function () {
    let scrollPosition = window.scrollY;

    // If scrolling down, fade out the video
    if (scrollPosition > lastScrollTop) {
        video.style.opacity = Math.max(1 - scrollPosition * 0.003, 0);
    } else {
        // If scrolling up, fade in the video
        video.style.opacity = Math.min(1 - scrollPosition * 0.003, 1);
    }

    // When the video is fully faded, show the content and slideshow
    if (video.style.opacity == 0) {
        document.querySelector('.content').classList.add('show');
        
        // Add 'show' class to the slideshow to trigger fade-in
        slideshow.classList.add('show');
        showSlide(slideIndex); // Show the first slide
    } else {
        document.querySelector('.content').classList.remove('show');
        
        // Remove 'show' class from slideshow to hide it
        slideshow.classList.remove('show');
    }

    lastScrollTop = scrollPosition <= 0 ? 0 : scrollPosition;
});

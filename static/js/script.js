class Ball {
    constructor() {
        this.element = document.querySelector('.ball');
        this.x = 0;
        this.y = 0;
        this.targetX = 0;
        this.targetY = 0;
        
        document.addEventListener('mousemove', (e) => this.followCursor(e));
    }

    followCursor(event) {
        this.targetX = event.clientX;
        this.targetY = event.clientY;
        
        gsap.to(this.element, {
            x: this.targetX,
            y: this.targetY,
            duration: 1.5,
            ease: "power1.out", 
            delay: 0.1 
        });
    }
}

// Initialize Features Section Animations
function initFeaturesAnimations() {
    // Set initial states
    gsap.set('.features-header', { y: 50, opacity: 0 });
    gsap.set('.section-title', { scale: 0.8, opacity: 0 });
    gsap.set('.section-description', { y: 30, opacity: 0 });
    gsap.set('.feature-card', { y: 50, opacity: 0 });

    // Create a timeline for the features section
    const tl = gsap.timeline({
        scrollTrigger: {
            trigger: '.features',
            start: 'top 80%',
            end: 'top 20%',
            toggleActions: 'play none none reverse',
            markers: false
        }
    });

    // Add animations to the timeline
    tl.to('.features-header', {
        y: 0,
        opacity: 1,
        duration: 0.8,
        ease: 'power2.out'
    })
    .to('.section-title', {
        scale: 1,
        opacity: 1,
        duration: 0.8,
        ease: 'back.out(1.7)'
    }, '-=0.4')
    .to('.section-description', {
        y: 0,
        opacity: 1,
        duration: 0.8,
        ease: 'power2.out'
    }, '-=0.4')
    .to('.feature-card', {
        y: 0,
        opacity: 1,
        duration: 0.8,
        stagger: 0.2,
        ease: 'power2.out'
    }, '-=0.4');

    // Add hover animations for feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card, {
                scale: 1.05,
                duration: 0.5,
                ease: 'power2.out'
            });
        });
        
        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                scale: 1,
                duration: 0.5,
                ease: 'power2.out'
            });
        });
    });
}

// Create a new ball and initialize animations when the page loads
window.addEventListener('load', () => {
    const ball = new Ball();
    initFeaturesAnimations();
});

// Form switching functionality
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('#login-form');
    const signupForm = document.querySelector('#signup-form');
    const loginLink = document.querySelector('#login-form a[href="#signup"]');
    const signupLink = document.querySelector('#signup-form a[href="#login"]');
    const loginRoleButtons = document.querySelectorAll('#login .role-btn');
    const signupRoleButtons = document.querySelectorAll('#signup .role-btn');

    // Function to check if screen is small
    const isSmallScreen = () => window.innerWidth <= 768;

    // Handle role selection for login form
    loginRoleButtons.forEach(button => {
        button.addEventListener('click', () => {
            loginRoleButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
        });
    });

    // Handle role selection for signup form
    signupRoleButtons.forEach(button => {
        button.addEventListener('click', () => {
            signupRoleButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
        });
    });

    // Handle login form submission
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get the selected role
        const selectedRole = loginForm.querySelector('.role-btn.active').getAttribute('data-role');
        
        // Get form data
        const formData = {
            email: loginForm.querySelector('#login-email').value,
            password: loginForm.querySelector('#login-password').value,
            role: selectedRole
        };
        
        // Send data to backend
        sendLoginData(formData);
    });

    // Handle signup form submission
    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get the selected role
        const selectedRole = signupForm.querySelector('.role-btn.active').getAttribute('data-role');
        
        // Get form data
        const formData = {
            email: signupForm.querySelector('#signup-email').value,
            password: signupForm.querySelector('#signup-password').value,
            role: selectedRole
        };
        
        // Send data to backend
        sendSignupData(formData);
    });

    // Function to send login data to backend
    function sendLoginData(data) {
        // Replace with your actual backend API endpoint
        fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Login successful:', data);
            // Handle successful login (e.g., redirect to dashboard)
            if (data.role === 'teacher') {
                window.location.href = '/teacher-dashboard';
            } else {
                window.location.href = '/student-dashboard';
            }
        })
        .catch(error => {
            console.error('Login error:', error);
            // Handle login error (e.g., show error message)
            alert('Login failed. Please try again.');
        });
    }

    // Function to send signup data to backend
    function sendSignupData(data) {
        // Replace with your actual backend API endpoint
        fetch('/api/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Signup successful:', data);
            // Handle successful signup (e.g., redirect to login)
            alert('Signup successful! Please login.');
            // Switch to login form
            if (isSmallScreen()) {
                document.querySelector('#signup').style.display = 'none';
                document.querySelector('#login').style.display = 'block';
            }
        })
        .catch(error => {
            console.error('Signup error:', error);
            // Handle signup error (e.g., show error message)
            alert('Signup failed. Please try again.');
        });
    }

    // Switch to signup form
    loginLink.addEventListener('click', (e) => {
        e.preventDefault();
        if (isSmallScreen()) {
            document.querySelector('#login').style.display = 'none';
            document.querySelector('#signup').style.display = 'block';
        }
    });

    // Switch to login form
    signupLink.addEventListener('click', (e) => {
        e.preventDefault();
        if (isSmallScreen()) {
            document.querySelector('#signup').style.display = 'none';
            document.querySelector('#login').style.display = 'block';
        }
    });

    // Update form visibility on window resize
    window.addEventListener('resize', () => {
        if (!isSmallScreen()) {
            document.querySelector('#login').style.display = 'block';
            document.querySelector('#signup').style.display = 'block';
        }
    });
});

document.querySelector('#login-form a[href="#signup"]').addEventListener('click', (e) => {
    e.preventDefault();
    
    // Animate the move_container to the right
    gsap.to('#move_container', {
        x: '-100%', 
        duration: 1.2,
        ease: "bounce.out"
    });


    gsap.to('#login', {
        opacity: 0,
        duration: 0.6
    });
    
    gsap.to('#signup', {
        opacity: 1,
        duration: 0.6,
        delay: 0.6
    });
});

// Add click handler for login link in signup form to reverse the animation
document.querySelector('#signup-form a[href="#login"]').addEventListener('click', (e) => {
    e.preventDefault();
    
    // Animate the move_container back to the left
    gsap.to('#move_container', {
        x: '0%',
        duration: 1.2,
        ease: "bounce.out"
    });

    // Optional: Animate the forms for smoother transition
    gsap.to('#signup', {
        opacity: 0,
        duration: 0.6
    });
    
    gsap.to('#login', {
        opacity: 1,
        duration: 0.6,
        delay: 0.6
    });

    // Change the background color and text content when clicking login link
    gsap.to('#move_container', {
        backgroundColor: 'rgb(195,251,241)',
        duration: 0.6
    });

    // Change the text content
    gsap.to('#move_container h1, #move_container p', {
        color: 'rgb(195,251,241)',
        duration: 0.6
    });

    document.querySelector('#move_container h1').textContent = "Think You're Smart?";
    document.querySelector('#move_container p').textContent = "Prove It!";
    // Wait for the text color change to complete before updating content
    setTimeout(() => {
        document.querySelector('#move_container h1').textContent = "Think You're Smart?";
        document.querySelector('#move_container p').textContent = "Prove It!";
        
        // Fade the text back in
        gsap.to('#move_container h1, #move_container p', {
            color: 'white',
            duration: 0.6
        });
    }, 600);
});

// Initialize all event listeners when the document is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Login form submission handler
    const loginForm = document.querySelector('#login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            console.log('Login form submitted'); // Debug log
            
            // Animate the move_container to slide up
            gsap.to('#move_container', {
                y: '-100%',
                duration: 1,
                ease: "power2.inOut",
                onComplete: () => {
                    console.log('Animation completed'); // Debug log
                }
            });

            // Animate the login form to fade out
            gsap.to('#login', {
                opacity: 0,
                duration: 0.5,
                ease: "power2.inOut"
            });
        });
    }

    // Role button click handlers
    const roleButtons = document.querySelectorAll('.role-btn');
    roleButtons.forEach(button => {
        button.addEventListener('click', () => {
            roleButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
        });
    });
});

